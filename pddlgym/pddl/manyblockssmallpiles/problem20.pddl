
(define (problem manyblockssmallpiles) (:domain blocks)
  (:objects
        b0 - block
	b1 - block
	b10 - block
	b11 - block
	b12 - block
	b13 - block
	b14 - block
	b15 - block
	b16 - block
	b17 - block
	b18 - block
	b19 - block
	b2 - block
	b3 - block
	b4 - block
	b5 - block
	b6 - block
	b7 - block
	b8 - block
	b9 - block
  )
  (:init 
	(clear b0)
	(clear b11)
	(clear b13)
	(clear b16)
	(clear b17)
	(clear b2)
	(clear b3)
	(clear b6)
	(clear b8)
	(handempty )
	(on b0 b1)
	(on b11 b12)
	(on b13 b14)
	(on b14 b15)
	(on b17 b18)
	(on b18 b19)
	(on b3 b4)
	(on b4 b5)
	(on b6 b7)
	(on b8 b9)
	(on b9 b10)
	(ontable b10)
	(ontable b12)
	(ontable b15)
	(ontable b16)
	(ontable b19)
	(ontable b1)
	(ontable b2)
	(ontable b5)
	(ontable b7)
  )
  (:goal (and
	(on b3 b12)
	(on b12 b7)
	(on b7 b1)
	(on b1 b13)
	(ontable b13)))
)
