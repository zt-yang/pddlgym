
(define (problem manyblockssmallpiles) (:domain blocks)
  (:objects
        b0 - block
	b1 - block
	b10 - block
	b11 - block
	b12 - block
	b13 - block
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
	(clear b10)
	(clear b11)
	(clear b1)
	(clear b3)
	(clear b4)
	(clear b6)
	(clear b7)
	(handempty )
	(on b11 b12)
	(on b12 b13)
	(on b1 b2)
	(on b4 b5)
	(on b7 b8)
	(on b8 b9)
	(ontable b0)
	(ontable b10)
	(ontable b13)
	(ontable b2)
	(ontable b3)
	(ontable b5)
	(ontable b6)
	(ontable b9)
  )
  (:goal (and
	(on b0 b3)
	(on b3 b13)
	(on b13 b1)
	(on b1 b5)
	(on b5 b9)
	(ontable b9)
	(on b10 b12)
	(on b12 b11)
	(on b11 b8)
	(on b8 b2)
	(on b2 b6)
	(ontable b6)))
)
