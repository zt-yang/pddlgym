
(define (problem logistics-04-0) (:domain logistics)
  (:objects
        apn1 - thing
	apn2 - thing
	apt1 - location
	apt2 - location
	cit1 - location
	cit2 - location
	obj11 - thing
	obj12 - thing
	obj13 - thing
	obj21 - thing
	obj22 - thing
	obj23 - thing
	pos11 - location
	pos12 - location
	pos13 - location
	pos21 - location
	pos22 - location
	pos23 - location
	tru1 - thing
	tru2 - thing
  )
  (:goal (and
	(at obj11 pos21)
	(at obj23 pos11)))
  (:init 
	(at apn1 apt2)
	(at apn2 apt1)
	(at obj11 pos11)
	(at obj12 pos12)
	(at obj13 pos13)
	(at obj21 pos21)
	(at obj22 pos22)
	(at obj23 pos23)
	(at tru1 pos11)
	(at tru2 pos22)
	(drivetruck apn1 apt1)
	(drivetruck apn1 apt2)
	(drivetruck apn1 cit1)
	(drivetruck apn1 cit2)
	(drivetruck apn1 pos11)
	(drivetruck apn1 pos12)
	(drivetruck apn1 pos13)
	(drivetruck apn1 pos21)
	(drivetruck apn1 pos22)
	(drivetruck apn1 pos23)
	(drivetruck apn2 apt1)
	(drivetruck apn2 apt2)
	(drivetruck apn2 cit1)
	(drivetruck apn2 cit2)
	(drivetruck apn2 pos11)
	(drivetruck apn2 pos12)
	(drivetruck apn2 pos13)
	(drivetruck apn2 pos21)
	(drivetruck apn2 pos22)
	(drivetruck apn2 pos23)
	(drivetruck obj11 apt1)
	(drivetruck obj11 apt2)
	(drivetruck obj11 cit1)
	(drivetruck obj11 cit2)
	(drivetruck obj11 pos11)
	(drivetruck obj11 pos12)
	(drivetruck obj11 pos13)
	(drivetruck obj11 pos21)
	(drivetruck obj11 pos22)
	(drivetruck obj11 pos23)
	(drivetruck obj12 apt1)
	(drivetruck obj12 apt2)
	(drivetruck obj12 cit1)
	(drivetruck obj12 cit2)
	(drivetruck obj12 pos11)
	(drivetruck obj12 pos12)
	(drivetruck obj12 pos13)
	(drivetruck obj12 pos21)
	(drivetruck obj12 pos22)
	(drivetruck obj12 pos23)
	(drivetruck obj13 apt1)
	(drivetruck obj13 apt2)
	(drivetruck obj13 cit1)
	(drivetruck obj13 cit2)
	(drivetruck obj13 pos11)
	(drivetruck obj13 pos12)
	(drivetruck obj13 pos13)
	(drivetruck obj13 pos21)
	(drivetruck obj13 pos22)
	(drivetruck obj13 pos23)
	(drivetruck obj21 apt1)
	(drivetruck obj21 apt2)
	(drivetruck obj21 cit1)
	(drivetruck obj21 cit2)
	(drivetruck obj21 pos11)
	(drivetruck obj21 pos12)
	(drivetruck obj21 pos13)
	(drivetruck obj21 pos21)
	(drivetruck obj21 pos22)
	(drivetruck obj21 pos23)
	(drivetruck obj22 apt1)
	(drivetruck obj22 apt2)
	(drivetruck obj22 cit1)
	(drivetruck obj22 cit2)
	(drivetruck obj22 pos11)
	(drivetruck obj22 pos12)
	(drivetruck obj22 pos13)
	(drivetruck obj22 pos21)
	(drivetruck obj22 pos22)
	(drivetruck obj22 pos23)
	(drivetruck obj23 apt1)
	(drivetruck obj23 apt2)
	(drivetruck obj23 cit1)
	(drivetruck obj23 cit2)
	(drivetruck obj23 pos11)
	(drivetruck obj23 pos12)
	(drivetruck obj23 pos13)
	(drivetruck obj23 pos21)
	(drivetruck obj23 pos22)
	(drivetruck obj23 pos23)
	(drivetruck tru1 apt1)
	(drivetruck tru1 apt2)
	(drivetruck tru1 cit1)
	(drivetruck tru1 cit2)
	(drivetruck tru1 pos11)
	(drivetruck tru1 pos12)
	(drivetruck tru1 pos13)
	(drivetruck tru1 pos21)
	(drivetruck tru1 pos22)
	(drivetruck tru1 pos23)
	(drivetruck tru2 apt1)
	(drivetruck tru2 apt2)
	(drivetruck tru2 cit1)
	(drivetruck tru2 cit2)
	(drivetruck tru2 pos11)
	(drivetruck tru2 pos12)
	(drivetruck tru2 pos13)
	(drivetruck tru2 pos21)
	(drivetruck tru2 pos22)
	(drivetruck tru2 pos23)
	(flyairplane apn1 apt1)
	(flyairplane apn1 apt2)
	(flyairplane apn1 cit1)
	(flyairplane apn1 cit2)
	(flyairplane apn1 pos11)
	(flyairplane apn1 pos12)
	(flyairplane apn1 pos13)
	(flyairplane apn1 pos21)
	(flyairplane apn1 pos22)
	(flyairplane apn1 pos23)
	(flyairplane apn2 apt1)
	(flyairplane apn2 apt2)
	(flyairplane apn2 cit1)
	(flyairplane apn2 cit2)
	(flyairplane apn2 pos11)
	(flyairplane apn2 pos12)
	(flyairplane apn2 pos13)
	(flyairplane apn2 pos21)
	(flyairplane apn2 pos22)
	(flyairplane apn2 pos23)
	(flyairplane obj11 apt1)
	(flyairplane obj11 apt2)
	(flyairplane obj11 cit1)
	(flyairplane obj11 cit2)
	(flyairplane obj11 pos11)
	(flyairplane obj11 pos12)
	(flyairplane obj11 pos13)
	(flyairplane obj11 pos21)
	(flyairplane obj11 pos22)
	(flyairplane obj11 pos23)
	(flyairplane obj12 apt1)
	(flyairplane obj12 apt2)
	(flyairplane obj12 cit1)
	(flyairplane obj12 cit2)
	(flyairplane obj12 pos11)
	(flyairplane obj12 pos12)
	(flyairplane obj12 pos13)
	(flyairplane obj12 pos21)
	(flyairplane obj12 pos22)
	(flyairplane obj12 pos23)
	(flyairplane obj13 apt1)
	(flyairplane obj13 apt2)
	(flyairplane obj13 cit1)
	(flyairplane obj13 cit2)
	(flyairplane obj13 pos11)
	(flyairplane obj13 pos12)
	(flyairplane obj13 pos13)
	(flyairplane obj13 pos21)
	(flyairplane obj13 pos22)
	(flyairplane obj13 pos23)
	(flyairplane obj21 apt1)
	(flyairplane obj21 apt2)
	(flyairplane obj21 cit1)
	(flyairplane obj21 cit2)
	(flyairplane obj21 pos11)
	(flyairplane obj21 pos12)
	(flyairplane obj21 pos13)
	(flyairplane obj21 pos21)
	(flyairplane obj21 pos22)
	(flyairplane obj21 pos23)
	(flyairplane obj22 apt1)
	(flyairplane obj22 apt2)
	(flyairplane obj22 cit1)
	(flyairplane obj22 cit2)
	(flyairplane obj22 pos11)
	(flyairplane obj22 pos12)
	(flyairplane obj22 pos13)
	(flyairplane obj22 pos21)
	(flyairplane obj22 pos22)
	(flyairplane obj22 pos23)
	(flyairplane obj23 apt1)
	(flyairplane obj23 apt2)
	(flyairplane obj23 cit1)
	(flyairplane obj23 cit2)
	(flyairplane obj23 pos11)
	(flyairplane obj23 pos12)
	(flyairplane obj23 pos13)
	(flyairplane obj23 pos21)
	(flyairplane obj23 pos22)
	(flyairplane obj23 pos23)
	(flyairplane tru1 apt1)
	(flyairplane tru1 apt2)
	(flyairplane tru1 cit1)
	(flyairplane tru1 cit2)
	(flyairplane tru1 pos11)
	(flyairplane tru1 pos12)
	(flyairplane tru1 pos13)
	(flyairplane tru1 pos21)
	(flyairplane tru1 pos22)
	(flyairplane tru1 pos23)
	(flyairplane tru2 apt1)
	(flyairplane tru2 apt2)
	(flyairplane tru2 cit1)
	(flyairplane tru2 cit2)
	(flyairplane tru2 pos11)
	(flyairplane tru2 pos12)
	(flyairplane tru2 pos13)
	(flyairplane tru2 pos21)
	(flyairplane tru2 pos22)
	(flyairplane tru2 pos23)
	(in-city apt1 cit1)
	(in-city apt2 cit2)
	(in-city pos11 cit1)
	(in-city pos12 cit1)
	(in-city pos13 cit1)
	(in-city pos21 cit2)
	(in-city pos22 cit2)
	(in-city pos23 cit2)
	(isairplane apn1)
	(isairplane apn2)
	(isairport apt1)
	(isairport apt2)
	(iscity cit1)
	(iscity cit2)
	(islocation pos11)
	(islocation pos12)
	(islocation pos13)
	(islocation pos21)
	(islocation pos22)
	(islocation pos23)
	(ispackage obj11)
	(ispackage obj12)
	(ispackage obj13)
	(ispackage obj21)
	(ispackage obj22)
	(ispackage obj23)
	(isplace apt1)
	(isplace apt2)
	(isplace pos11)
	(isplace pos12)
	(isplace pos13)
	(isplace pos21)
	(isplace pos22)
	(isplace pos23)
	(istruck tru1)
	(istruck tru2)
	(loadairplane apn1 apn1)
	(loadairplane apn1 apn2)
	(loadairplane apn1 obj11)
	(loadairplane apn1 obj12)
	(loadairplane apn1 obj13)
	(loadairplane apn1 obj21)
	(loadairplane apn1 obj22)
	(loadairplane apn1 obj23)
	(loadairplane apn1 tru1)
	(loadairplane apn1 tru2)
	(loadairplane apn2 apn1)
	(loadairplane apn2 apn2)
	(loadairplane apn2 obj11)
	(loadairplane apn2 obj12)
	(loadairplane apn2 obj13)
	(loadairplane apn2 obj21)
	(loadairplane apn2 obj22)
	(loadairplane apn2 obj23)
	(loadairplane apn2 tru1)
	(loadairplane apn2 tru2)
	(loadairplane obj11 apn1)
	(loadairplane obj11 apn2)
	(loadairplane obj11 obj11)
	(loadairplane obj11 obj12)
	(loadairplane obj11 obj13)
	(loadairplane obj11 obj21)
	(loadairplane obj11 obj22)
	(loadairplane obj11 obj23)
	(loadairplane obj11 tru1)
	(loadairplane obj11 tru2)
	(loadairplane obj12 apn1)
	(loadairplane obj12 apn2)
	(loadairplane obj12 obj11)
	(loadairplane obj12 obj12)
	(loadairplane obj12 obj13)
	(loadairplane obj12 obj21)
	(loadairplane obj12 obj22)
	(loadairplane obj12 obj23)
	(loadairplane obj12 tru1)
	(loadairplane obj12 tru2)
	(loadairplane obj13 apn1)
	(loadairplane obj13 apn2)
	(loadairplane obj13 obj11)
	(loadairplane obj13 obj12)
	(loadairplane obj13 obj13)
	(loadairplane obj13 obj21)
	(loadairplane obj13 obj22)
	(loadairplane obj13 obj23)
	(loadairplane obj13 tru1)
	(loadairplane obj13 tru2)
	(loadairplane obj21 apn1)
	(loadairplane obj21 apn2)
	(loadairplane obj21 obj11)
	(loadairplane obj21 obj12)
	(loadairplane obj21 obj13)
	(loadairplane obj21 obj21)
	(loadairplane obj21 obj22)
	(loadairplane obj21 obj23)
	(loadairplane obj21 tru1)
	(loadairplane obj21 tru2)
	(loadairplane obj22 apn1)
	(loadairplane obj22 apn2)
	(loadairplane obj22 obj11)
	(loadairplane obj22 obj12)
	(loadairplane obj22 obj13)
	(loadairplane obj22 obj21)
	(loadairplane obj22 obj22)
	(loadairplane obj22 obj23)
	(loadairplane obj22 tru1)
	(loadairplane obj22 tru2)
	(loadairplane obj23 apn1)
	(loadairplane obj23 apn2)
	(loadairplane obj23 obj11)
	(loadairplane obj23 obj12)
	(loadairplane obj23 obj13)
	(loadairplane obj23 obj21)
	(loadairplane obj23 obj22)
	(loadairplane obj23 obj23)
	(loadairplane obj23 tru1)
	(loadairplane obj23 tru2)
	(loadairplane tru1 apn1)
	(loadairplane tru1 apn2)
	(loadairplane tru1 obj11)
	(loadairplane tru1 obj12)
	(loadairplane tru1 obj13)
	(loadairplane tru1 obj21)
	(loadairplane tru1 obj22)
	(loadairplane tru1 obj23)
	(loadairplane tru1 tru1)
	(loadairplane tru1 tru2)
	(loadairplane tru2 apn1)
	(loadairplane tru2 apn2)
	(loadairplane tru2 obj11)
	(loadairplane tru2 obj12)
	(loadairplane tru2 obj13)
	(loadairplane tru2 obj21)
	(loadairplane tru2 obj22)
	(loadairplane tru2 obj23)
	(loadairplane tru2 tru1)
	(loadairplane tru2 tru2)
	(loadtruck apn1 apn1)
	(loadtruck apn1 apn2)
	(loadtruck apn1 obj11)
	(loadtruck apn1 obj12)
	(loadtruck apn1 obj13)
	(loadtruck apn1 obj21)
	(loadtruck apn1 obj22)
	(loadtruck apn1 obj23)
	(loadtruck apn1 tru1)
	(loadtruck apn1 tru2)
	(loadtruck apn2 apn1)
	(loadtruck apn2 apn2)
	(loadtruck apn2 obj11)
	(loadtruck apn2 obj12)
	(loadtruck apn2 obj13)
	(loadtruck apn2 obj21)
	(loadtruck apn2 obj22)
	(loadtruck apn2 obj23)
	(loadtruck apn2 tru1)
	(loadtruck apn2 tru2)
	(loadtruck obj11 apn1)
	(loadtruck obj11 apn2)
	(loadtruck obj11 obj11)
	(loadtruck obj11 obj12)
	(loadtruck obj11 obj13)
	(loadtruck obj11 obj21)
	(loadtruck obj11 obj22)
	(loadtruck obj11 obj23)
	(loadtruck obj11 tru1)
	(loadtruck obj11 tru2)
	(loadtruck obj12 apn1)
	(loadtruck obj12 apn2)
	(loadtruck obj12 obj11)
	(loadtruck obj12 obj12)
	(loadtruck obj12 obj13)
	(loadtruck obj12 obj21)
	(loadtruck obj12 obj22)
	(loadtruck obj12 obj23)
	(loadtruck obj12 tru1)
	(loadtruck obj12 tru2)
	(loadtruck obj13 apn1)
	(loadtruck obj13 apn2)
	(loadtruck obj13 obj11)
	(loadtruck obj13 obj12)
	(loadtruck obj13 obj13)
	(loadtruck obj13 obj21)
	(loadtruck obj13 obj22)
	(loadtruck obj13 obj23)
	(loadtruck obj13 tru1)
	(loadtruck obj13 tru2)
	(loadtruck obj21 apn1)
	(loadtruck obj21 apn2)
	(loadtruck obj21 obj11)
	(loadtruck obj21 obj12)
	(loadtruck obj21 obj13)
	(loadtruck obj21 obj21)
	(loadtruck obj21 obj22)
	(loadtruck obj21 obj23)
	(loadtruck obj21 tru1)
	(loadtruck obj21 tru2)
	(loadtruck obj22 apn1)
	(loadtruck obj22 apn2)
	(loadtruck obj22 obj11)
	(loadtruck obj22 obj12)
	(loadtruck obj22 obj13)
	(loadtruck obj22 obj21)
	(loadtruck obj22 obj22)
	(loadtruck obj22 obj23)
	(loadtruck obj22 tru1)
	(loadtruck obj22 tru2)
	(loadtruck obj23 apn1)
	(loadtruck obj23 apn2)
	(loadtruck obj23 obj11)
	(loadtruck obj23 obj12)
	(loadtruck obj23 obj13)
	(loadtruck obj23 obj21)
	(loadtruck obj23 obj22)
	(loadtruck obj23 obj23)
	(loadtruck obj23 tru1)
	(loadtruck obj23 tru2)
	(loadtruck tru1 apn1)
	(loadtruck tru1 apn2)
	(loadtruck tru1 obj11)
	(loadtruck tru1 obj12)
	(loadtruck tru1 obj13)
	(loadtruck tru1 obj21)
	(loadtruck tru1 obj22)
	(loadtruck tru1 obj23)
	(loadtruck tru1 tru1)
	(loadtruck tru1 tru2)
	(loadtruck tru2 apn1)
	(loadtruck tru2 apn2)
	(loadtruck tru2 obj11)
	(loadtruck tru2 obj12)
	(loadtruck tru2 obj13)
	(loadtruck tru2 obj21)
	(loadtruck tru2 obj22)
	(loadtruck tru2 obj23)
	(loadtruck tru2 tru1)
	(loadtruck tru2 tru2)
	(unloadairplane apn1)
	(unloadairplane apn2)
	(unloadairplane obj11)
	(unloadairplane obj12)
	(unloadairplane obj13)
	(unloadairplane obj21)
	(unloadairplane obj22)
	(unloadairplane obj23)
	(unloadairplane tru1)
	(unloadairplane tru2)
	(unloadtruck apn1)
	(unloadtruck apn2)
	(unloadtruck obj11)
	(unloadtruck obj12)
	(unloadtruck obj13)
	(unloadtruck obj21)
	(unloadtruck obj22)
	(unloadtruck obj23)
	(unloadtruck tru1)
	(unloadtruck tru2)
))
        