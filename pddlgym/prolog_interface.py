from pddlgym.structs import Predicate, Literal, LiteralConjunction, LiteralDisjunction, ForAll, Exists, Not
from pddlgym.utils import get_object_combinations
import random
from collections import defaultdict
import subprocess
import sys
import tempfile
import copy

MINUS = '1111111'
AT = ''

def get_type(var):
    if '=' in var: var = var[:var.index('=')]
    var = ''.join([i for i in var if not i.isdigit() and i != '?'])
    return var

class PrologInterface:
    """
    """
    def __init__(self, kb, conds, max_assignment_count=2, timeout=2, 
                 allow_redundant_variables=True, constants=None,
                 pred=None, verbose=False, INFER_TYPING=False):

        ## ------ YANG added INFERTYPING to reduce inference time ----
        if pred != None:
            variables = copy.deepcopy(pred.param_names)
            if hasattr(pred.body, 'variables'):  ## if Exist in structure
                variables += [n.name for n in pred.body.variables]
            self._types = set([get_type(var) for var in variables])
        else:
            self._types = set([])
            INFER_TYPING = False

        def DISCARD_ATOM(atom):
            if INFER_TYPING and '=' in atom and get_type(atom) not in self._types:
                return True
            return False
        self.DISCARD_ATOM = DISCARD_ATOM
        ## ------------------------------------------------------------

        if not isinstance(conds, list):
            conds = [conds]
        # Preprocess negative literals into renamed positive literals
        kb, conds = self._preprocess_negative_literals(kb, conds,
                            verbose=verbose, DISCARD_ATOM=self.DISCARD_ATOM)
        self._kb = kb
        self._conds = conds
        self._cond_lits = self._get_lits_from_conds(conds)
        self._max_assignment_count = max_assignment_count
        self._allow_redundant_variables = allow_redundant_variables
        self._timeout = timeout

        ## YANG added INFERTYPING to reduce inference time
        self._varnames_to_var = self._create_varname_to_var(self._cond_lits, 
            lambda x : self._clean_variable_name(x).lower(), self.DISCARD_ATOM)
        self._atomname_to_atom = self._create_varname_to_var(\
            self._kb, self._clean_atom_name, self.DISCARD_ATOM)

        self._type_to_atomnames = defaultdict(list)
        for atom_name, atom in self._atomname_to_atom.items():
            self._type_to_atomnames[atom.var_type].append(atom_name)
        self._prolog_str = self._create_prolog_str()
        self._constants = constants # unused now because variables begin with ? by convention
        # print(self._prolog_str)
        # import ipdb; ipdb.set_trace()

        self._pred = pred  ## added by Yang for naming the .pl file in /temp/ folder
        self.verbose = verbose


    @classmethod
    def _preprocess_negative_literals(cls, kb, conds, verbose=False, DISCARD_ATOM=None):
        # Check for negated quantifiers, which we do not handle
        if any((isinstance(c, Exists) or isinstance(c, ForAll)) and c.is_negative \
                for c in conds):
            raise NotImplementedError("We do not yet handle negated quantifiers")
        # Find all predicates with a negated literal in the conds
        negated_predicates = set()
        for cond in cls._get_lits_from_conds(conds):
            if cond.is_negative:
                negated_predicates.add(cond.predicate)
        if len(negated_predicates) == 0:
            return kb, conds
        else:  ## YANG: ignore them
            # print('_preprocess_negative_literals | ignore negated predicates', negated_predicates)
            return kb, [l for l in cls._get_lits_from_conds(conds) if not l.is_negative]

        # Start the new kb and conds
        kb = [lit for lit in kb]
        conds = [c for c in conds]
        # Sanity check
        assert all(str(p).startswith("Not") for p in negated_predicates)
        # Create positive predicates for the negated predicates
        negated_pred_to_pos_pred = {}
        for p in negated_predicates:
            # Prolog hands = specially
            if p.name == "=":
                pos_pred = Predicate(f"neg-eq", p.arity, p.var_types)
            else:
                pos_pred = Predicate(f"neg-{p.name}", p.arity, p.var_types)
            negated_pred_to_pos_pred[p] = pos_pred
        # TODO pass in objects separately
        objects = { o for lit in kb for o in lit.variables }

        ## --------- Hack added by YANG to resolve the existential crisis -------------
        if len(conds) == 1 and isinstance(conds[0], Exists):  ## for unsafe...
            objects = [o for o in objects if not DISCARD_ATOM(o.name)]
        ## ----------------------------------------------------------------------------

        # Get all instantiations of the new positive predicates
        for negated_pred, pos_pred in negated_pred_to_pos_pred.items():
            original_positive_pred = negated_pred.positive
            # Get all combinations of objects
            for objs in get_object_combinations(objects,
                arity=pos_pred.arity,
                var_types=pos_pred.var_types,
                allow_duplicates=True):
                ## --------- added by YANG to resolve the existential crisis ----------
                # if verbose:
                #     print('_preprocess_negative_literals', conds, objs)
                ## --------------------------------------------------------------------
                # Check whether the positive version is in the kb
                if original_positive_pred(*objs) in kb:
                    continue
                # Add the new positive literal to the kb
                kb.append(pos_pred(*objs))
            # Update the conds to include the positive pred instead of the negative pred
            conds = cls._replace_predicate(conds, negated_pred, pos_pred)
        return kb, conds

    @classmethod
    def _replace_predicate(cls, conds, from_pred, to_pred):
        if isinstance(conds, list):
            return [cls._replace_predicate(c, from_pred, to_pred) for c in conds]
        if isinstance(conds, Literal):
            if conds.predicate == from_pred:
                return to_pred(*conds.variables)
            return conds
        if isinstance(conds, LiteralConjunction):
            return LiteralConjunction(cls._replace_predicate(conds.literals, from_pred, to_pred))
        if isinstance(conds, LiteralDisjunction):
            return LiteralDisjunction(cls._replace_predicate(conds.literals, from_pred, to_pred))
        if isinstance(conds, ForAll):
            assert not conds.is_negative, "Negative universal quantification not implemented (use Exists instead)"
            return ForAll(cls._replace_predicate(conds.body, from_pred, to_pred), conds.variables, 
                          is_negative=conds.is_negative)
        if isinstance(conds, Exists):
            assert not conds.is_negative, "Negative exisential quantification not implemented (use ForAll instead)"
            return Exists(conds.variables,cls._replace_predicate(conds.body, from_pred, to_pred),
                          is_negative=conds.is_negative)
        import ipdb; ipdb.set_trace()
        raise NotImplementedError()

    @staticmethod
    def _get_lits_from_conds(conds):
        if isinstance(conds, list):
            return [lit for c in conds for lit in PrologInterface._get_lits_from_conds(c)]
        if isinstance(conds, Literal):
            return [conds]
        if hasattr(conds, 'literals'):
            return PrologInterface._get_lits_from_conds(conds.literals)
        if hasattr(conds, 'body'):
            return PrologInterface._get_lits_from_conds(conds.body)
        import ipdb; ipdb.set_trace()
        raise NotImplementedError()

    @classmethod
    def _clean_atom_name(cls, atom_name):  ## changed by YANG because _ cause problems for numbers
        return atom_name.lower().replace("-", MINUS).replace("@", AT)

    @classmethod
    def _clean_variable_name(cls, var_name):
        var_name = var_name.replace("-", MINUS).replace("@", AT)
        if var_name.startswith("?"):
            return var_name.replace("?", "").capitalize()
        return var_name

    @classmethod
    def _clean_predicate_name(cls, predicate_name):
        if predicate_name == "=":
            return "predeq"
        return "pred"+predicate_name.lower().replace("-", MINUS).replace("@", AT)

    @staticmethod
    def _create_varname_to_var(lits, transformer, DISCARD_ATOM):
        """
        """
        vname_to_v = {}
        for lit in lits:
            for v in lit.variables:
                vname = transformer(v.name)

                ## ignore those not in the saved types
                if DISCARD_ATOM(vname):
                    # print('ignored variable', vname)
                    continue

                ## otherwise “Syntax error: Operator expected” in Prolog
                # if ' ' in v:
                #     from pddlgym.structs import TypedEntity
                #     v = TypedEntity(v.name.replace(' ', ''), v.var_type)
                #     vname = vname.replace(' ', '')

                if vname in vname_to_v:
                    assert vname_to_v[vname] == v
                else:
                    vname_to_v[vname] = v
                    if ',' in vname:
                        ## there may be '[12,p0=(0.7,4.9,0.845,0.948),(10,none,3)]'
                        vname_to_v[vname.replace(', ', '*').replace('t(', '(')] = v
                        ## there may be 'c648=t(6*4)'
                        vname_to_v[vname.replace(', ', '*')] = v
        return vname_to_v

    def _create_prolog_str(self):
        """
        """
        preamble = self._prolog_preamble(self._conds)
        type_str = self._prolog_type_str(self._kb, self.DISCARD_ATOM)
        self._kb_str = self._prolog_kb_str(self._kb)  # can be changed by prolog_goal
        goal_str, variables = self._prolog_goal(self._conds, self._allow_redundant_variables)
        end = self._prolog_end(variables, self._max_assignment_count)
        return '\n'.join([preamble, self._kb_str, type_str, goal_str, end])

    @classmethod
    def _prolog_kb_str(cls, kb):
        """
        """
        kb_str = ""
        for lit in sorted(kb):
            if lit.is_negative: continue  ## YANG added for notmarker(1) bug
            pred_name = cls._clean_predicate_name(lit.predicate.name)
            atoms = ",".join([cls._clean_atom_name(a) for a in lit.variables])
            kb_str += "\n{}({}).".format(pred_name, atoms)
        return kb_str

    @classmethod
    def _prolog_type_str(cls, kb, DISCARD_ATOM):
        """
        """
        all_atoms = sorted({ v for lit in kb for v in lit.variables })
        type_str = ""
        for v in sorted(all_atoms, key=lambda v:v.var_type):
            vname = cls._clean_atom_name(v.name)
            ## ignore those not in the saved types
            if DISCARD_ATOM(vname):
                continue
            type_str += "\nistype{}({}).".format(v.var_type, vname)
        return type_str

    def _prolog_goal(self, conds, allow_redundant_variables):
        """
        """
        all_vars = sorted({ v for lit in conds
                            for v in self._get_variables(lit, set()) if v.startswith("?") })
        all_vars_cleaned = [self._clean_variable_name(v) for v in all_vars]
        main_cond_str = ""
        for lit in conds:
            pred_str = "\n\t" + self._prolog_goal_line(lit) + ","
            main_cond_str += pred_str
        type_cond_str = ""
        for v in sorted(all_vars, key=lambda v:v.var_type):
            type_cond_str += "\n\tistype{}({}),".format(v.var_type, self._clean_variable_name(v.name))
        if not allow_redundant_variables:
            all_different_str = "\n\tall_different([{}]).".format(",".join(all_vars_cleaned))
        else:
            type_cond_str = type_cond_str[:-1]
            all_different_str = "."
        head_str = "\ngoal({}) :-".format(",".join(all_vars_cleaned))
        final_str = head_str + main_cond_str + type_cond_str + all_different_str
        if final_str.endswith(",."):
            final_str = final_str[:-2] + "."
        return final_str, all_vars

    def _get_variables(self, lit, free_vars):
        if isinstance(lit, Literal):
            return {v for v in lit.variables
                    if v not in free_vars}
        if isinstance(lit, (LiteralConjunction, LiteralDisjunction)):
            return {v for nested_lit in lit.literals
                    for v in self._get_variables(nested_lit, free_vars)}
        if isinstance(lit, (ForAll, Exists)):
            for var in lit.variables:
                assert var not in free_vars
                free_vars.add(var)
            result = self._get_variables(lit.body, free_vars)
            for var in lit.variables:
                assert var in free_vars
                free_vars.remove(var)
            return result
        raise Exception("Unsupported lit: {}".format(lit))

    def _prolog_goal_line(self, lit):
        """
        """
        if isinstance(lit, LiteralConjunction):
            inner_str = ",".join(self._prolog_goal_line(l) for l in lit.literals)
            return "({})".format(inner_str)
        if isinstance(lit, LiteralDisjunction):
            inner_str = ";".join(self._prolog_goal_line(l) for l in lit.literals)
            return "({})".format(inner_str)
        if lit.is_negative:
            raise NotImplementedError("Prolog behaves unexpectedly with negative literals")
            # pos_pred_str = self._prolog_goal_line(lit.positive)
            # pred_str = "\\+({})".format(pos_pred_str)
            # return pred_str
        if isinstance(lit, Literal):
            pred_name = self._clean_predicate_name(lit.predicate.name)
            variables = ",".join([self._clean_variable_name(a.name) for a in lit.variables])
            pred_str = "{}({})".format(pred_name, variables)
            return pred_str
        if isinstance(lit, ForAll):
            variables = ",".join([self._clean_variable_name(a.name) for a in lit.variables])
            assert len(variables) == 1, "TODO: support ForAlls over multiple variables"
            variable = variables[0]
            var_type = lit.variables[0].var_type
            objects_of_type = self._type_to_atomnames[var_type]
            objects_str = "[" + ",".join(objects_of_type) + "]"
            pred_str_body = self._prolog_goal_line(lit.body)
            pred_str = "forall(member({}, {}), {})".format(variable, objects_str, pred_str_body)
            return pred_str
        if isinstance(lit, Exists):
            variables = ",".join([self._clean_variable_name(a.name)
                                  for a in self._get_variables(lit, set())])
            rand_num = random.randint(0, 1e6)
            body = self._prolog_goal_line(lit.body)
            self._kb_str += "\nhelper{}({}) :- {}.".format(rand_num, variables, body)
            pred_str = "helper{}({})".format(rand_num, variables)
            return pred_str
        raise NotImplementedError(lit)

    @classmethod
    def _prolog_preamble(cls, conds):
        cond_lits = cls._get_lits_from_conds(conds)
        pred_definitions = ""
        preds = set()
        for lit in cond_lits:
            preds.update(cls._get_predicates_from_literal(lit))
        preds = sorted(preds)
        for pred in preds:
            pred_name = cls._clean_predicate_name(pred.name)
            pred_definitions += "\n:- multifile({}/{}).".format(pred_name, pred.arity)

        return """print_solutions([]).
print_solutions([H|T]) :- write(H), nl, print_solutions(T).
:- style_check(-singleton).
{}
""".format(pred_definitions)

    @classmethod
    def _get_predicates_from_literal(cls, lit):
        if isinstance(lit, Literal):
            return { lit.predicate.positive }
        if isinstance(lit, LiteralConjunction):
            return { p for l in lit.literals for p in cls._get_predicates_from_literal(l) }
        if isinstance(lit, ForAll) or isinstance(lit, Exists):
            return cls._get_predicates_from_literal(lit.body)
        raise NotImplementedError()
    
    @classmethod
    def _prolog_end(cls, variables, max_assignment_count):
        lowercase_vars = ",".join([cls._clean_variable_name(v).lower() for v in variables])
        uppercase_vars = ",".join([cls._clean_variable_name(v).capitalize() for v in variables])
        return """
:- use_module(library(bounds)).
:- initialization (
    write([{0}]),
    nl,
    findnsols({1}, [{2}], goal({3}), L),
    print_solutions(L), 
    halt).
""".format(lowercase_vars, max_assignment_count, uppercase_vars, uppercase_vars)

    def _parse_output_line(self, output_line):
        """
        """
        line = output_line[1:-1]
        if line == '':
            return []

        ## e.g. output_line = '12,(10,none,3)', '[12,p0=(0.7,4.9,0.845,0.948),(10,none,3)]'
        if '(' in line and ')' in line:
            # found_matched = {}
            for k in self._atomname_to_atom:
                if '(' in k and ')' in k and k.replace(' ', '') in line:
                    tmp = k.replace('t(', '(').replace(', ', '*')
                    # found_matched[tmp] = k
                    line = line.replace(k.replace(' ', ''), tmp)

        return line.split(',')

    def run(self, debug=False):
        """
        """
        file = tempfile.NamedTemporaryFile(suffix=".pl")
        tmp_name = file.name
        with open(tmp_name, 'w') as f:
            f.write(self._prolog_str)

        timeout_str = "gtimeout" if sys.platform == 'darwin' else "timeout"
        cmd_str = "{} {} swipl {}".format(timeout_str, self._timeout, tmp_name)

        # if self._pred.name in ['on']:
        #     debug = True

        ## -----------------------
        if debug or self.verbose:
            import shutil
            import os
            from os.path import join, abspath, dirname, isdir
            from datetime import datetime

            now = datetime.now().strftime("%H%M%S")
            ROOT_DIR = join(dirname(__file__), os.pardir)

            if self._pred is not None:  ## find facts
                name = self._pred.name
            else:  ## find primitive actions
                name = self._conds[0].predicate.name
            name = f'{now}_{name}.pl'  ## tmp_name[tmp_name.rfind('/')+1:]
            tmp_dir = abspath(join(ROOT_DIR, '..', 'bullet', 'leap', 'temp'))
            if not isdir(tmp_dir):
                os.mkdir(tmp_dir)
            save_file = join(tmp_dir, name)
            shutil.copy(tmp_name, save_file)
            print(cmd_str.replace(tmp_name, save_file))
        ## -----------------------

        output = subprocess.getoutput(cmd_str)
        if "ERROR" in output or "Warning" in output:
            # import ipdb; ipdb.set_trace() ## YANG
            raise Exception("Prolog terminated with an error: \n{}".format(output))
        if debug: print('finished', name)
        lines = output.split('\n')
        varnames = self._parse_output_line(lines.pop(0))
        vs = [self._varnames_to_var[v] for v in varnames]
        bindings = lines
        if len(bindings) == 0:
            return []
        assignments = []
        for binding in bindings: # Recover original (typed) atoms
            atomnames = self._parse_output_line(binding)
            # # debug
            for v in atomnames:
                if v not in self._atomname_to_atom:
                    atomnames = self._parse_output_line(binding)
            atoms = [self._atomname_to_atom[v] for v in atomnames]
            assignment = dict(zip(vs, atoms))
            assignments.append(assignment)
        return assignments
