def get_near(letters, numbers, range):
	"""
			A1	A2	A3	A4
			B1	B2	B3	B4
			C1	C2	C3	C4
			D1	D2	D3	D4
			E1	E2	E3	E4
			
			Number of locations close to a location: (9 * range) - 1
	"""
	directions = [(-1, -1), (-1, 0), (-1, 1)]
	
