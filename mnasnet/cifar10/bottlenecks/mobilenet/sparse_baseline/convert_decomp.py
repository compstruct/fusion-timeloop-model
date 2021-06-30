import numpy as np
def decomp1(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(2): # (Spatial-X)
				for Q1 in range(4): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(2): # (Spatial-Y)
							for C0 in range(4): # (Spatial-Y)
								x = Q1*1 + M0*4
								y = C0*1 + M1*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(4): 
										# psum_spad
										for M2 in range(24): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*4
											P = P0*1
											M = M2*1 + M1*24 + M0*48
											C = C1*1 + C0*4
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp2(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		for M0 in range(4): 
			# shared_glb
			for P0 in range(32): 
				for M1 in range(2): # (Spatial-X)
					for Q1 in range(4): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for M2 in range(3): # (Spatial-Y)
								for C0 in range(3): # (Spatial-Y)
									x = Q1*1 + M1*4
									y = C0*1 + M2*3
									worktile = []
									# ifmap_spad
									for Q3 in range(1): 
										# weights_spad
										for C1 in range(8): 
											# psum_spad
											for M3 in range(6): 
												Q = Q3*1 + Q2*1 + Q1*1 + Q0*4
												M = M3*1 + M2*6 + M1*18 + M0*36
												P = P0*1
												C = C1*1 + C0*8
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp3(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		for M0 in range(4): 
			# shared_glb
			for P0 in range(32): 
				for M1 in range(2): # (Spatial-X)
					for Q1 in range(4): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for M2 in range(3): # (Spatial-Y)
								for C0 in range(3): # (Spatial-Y)
									x = Q1*1 + M1*4
									y = C0*1 + M2*3
									worktile = []
									# ifmap_spad
									for Q3 in range(1): 
										# weights_spad
										for C1 in range(8): 
											# psum_spad
											for M3 in range(6): 
												Q = Q3*1 + Q2*1 + Q1*1 + Q0*4
												M = M3*1 + M2*6 + M1*18 + M0*36
												P = P0*1
												C = C1*1 + C0*8
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp4(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(4): 
		for M0 in range(6): 
			# shared_glb
			for P0 in range(32): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(2): # (Spatial-Y)
							for C0 in range(4): # (Spatial-Y)
								x = Q1*1
								y = C0*1 + M1*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(16): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*16 + M0*32
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp5(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(4): 
		for M0 in range(6): 
			# shared_glb
			for P0 in range(32): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(2): # (Spatial-Y)
							for C0 in range(4): # (Spatial-Y)
								x = Q1*1
								y = C0*1 + M1*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(16): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*16 + M0*32
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp6(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(4): 
		for M0 in range(6): 
			# shared_glb
			for P0 in range(32): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(2): # (Spatial-Y)
							for C0 in range(4): # (Spatial-Y)
								x = Q1*1
								y = C0*1 + M1*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(16): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*16 + M0*32
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp7(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			# shared_glb
			for M1 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C0 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C0*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(24): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*24 + M0*192
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp8(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			# shared_glb
			for M1 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C0 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C0*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(24): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*24 + M0*192
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp9(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			# shared_glb
			for M1 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C0 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C0*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(24): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*24 + M0*192
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp10(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			# shared_glb
			for M1 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C0 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C0*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C1 in range(8): 
										# psum_spad
										for M2 in range(24): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											M = M2*1 + M1*24 + M0*192
											P = P0*1
											C = C1*1 + C0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp11(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			for C0 in range(2): 
				# shared_glb
				for M1 in range(16): 
					for P0 in range(16): 
						for Q1 in range(8): # (Spatial-X)
							# DummyBuffer
							for Q2 in range(1): 
								for M2 in range(3): # (Spatial-Y)
									for C1 in range(3): # (Spatial-Y)
										x = Q1*1
										y = C1*1 + M2*3
										worktile = []
										# ifmap_spad
										for Q3 in range(1): 
											# weights_spad
											for C2 in range(16): 
												# psum_spad
												for M3 in range(6): 
													Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
													M = M3*1 + M2*6 + M1*18 + M0*288
													C = C2*1 + C1*16 + C0*48
													P = P0*1
													R = 0
													S = 0
													worktile.append(tensor[R,S,C,M])
										if (x,y) in worktiles.keys():
											worktiles[(x,y)].append(np.array(worktile))
										else:
											worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp12(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			for C0 in range(2): 
				# shared_glb
				for M1 in range(16): 
					for P0 in range(16): 
						for Q1 in range(8): # (Spatial-X)
							# DummyBuffer
							for Q2 in range(1): 
								for M2 in range(3): # (Spatial-Y)
									for C1 in range(3): # (Spatial-Y)
										x = Q1*1
										y = C1*1 + M2*3
										worktile = []
										# ifmap_spad
										for Q3 in range(1): 
											# weights_spad
											for C2 in range(16): 
												# psum_spad
												for M3 in range(6): 
													Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
													M = M3*1 + M2*6 + M1*18 + M0*288
													C = C2*1 + C1*16 + C0*48
													P = P0*1
													R = 0
													S = 0
													worktile.append(tensor[R,S,C,M])
										if (x,y) in worktiles.keys():
											worktiles[(x,y)].append(np.array(worktile))
										else:
											worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp13(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(2): 
		for C0 in range(2): 
			# shared_glb
			for M1 in range(24): 
				for P0 in range(8): 
					for Q0 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q1 in range(1): 
							for M2 in range(3): # (Spatial-Y)
								for C1 in range(3): # (Spatial-Y)
									x = Q0*1
									y = C1*1 + M2*3
									worktile = []
									# ifmap_spad
									for Q2 in range(1): 
										# weights_spad
										for C2 in range(16): 
											# psum_spad
											for M3 in range(4): 
												M = M3*1 + M2*4 + M1*12 + M0*288
												C = C2*1 + C1*16 + C0*48
												P = P0*1
												Q = Q2*1 + Q1*1 + Q0*1
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp14(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(4): 
		for C0 in range(5): 
			# shared_glb
			for M1 in range(6): 
				for P0 in range(8): 
					for Q0 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q1 in range(1): 
							for M2 in range(2): # (Spatial-Y)
								for C1 in range(4): # (Spatial-Y)
									x = Q0*1
									y = C1*1 + M2*4
									worktile = []
									# ifmap_spad
									for Q2 in range(1): 
										# weights_spad
										for C2 in range(8): 
											# psum_spad
											for M3 in range(20): 
												M = M3*1 + M2*20 + M1*40 + M0*240
												C = C2*1 + C1*8 + C0*32
												P = P0*1
												Q = Q2*1 + Q1*1 + Q0*1
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp15(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(4): 
		for C0 in range(5): 
			# shared_glb
			for M1 in range(6): 
				for P0 in range(8): 
					for Q0 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q1 in range(1): 
							for M2 in range(2): # (Spatial-Y)
								for C1 in range(4): # (Spatial-Y)
									x = Q0*1
									y = C1*1 + M2*4
									worktile = []
									# ifmap_spad
									for Q2 in range(1): 
										# weights_spad
										for C2 in range(8): 
											# psum_spad
											for M3 in range(20): 
												M = M3*1 + M2*20 + M1*40 + M0*240
												C = C2*1 + C1*8 + C0*32
												P = P0*1
												Q = Q2*1 + Q1*1 + Q0*1
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def decomp16(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(4): 
		for C0 in range(5): 
			# shared_glb
			for M1 in range(6): 
				for P0 in range(8): 
					for Q0 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q1 in range(1): 
							for M2 in range(2): # (Spatial-Y)
								for C1 in range(4): # (Spatial-Y)
									x = Q0*1
									y = C1*1 + M2*4
									worktile = []
									# ifmap_spad
									for Q2 in range(1): 
										# weights_spad
										for C2 in range(8): 
											# psum_spad
											for M3 in range(20): 
												M = M3*1 + M2*20 + M1*40 + M0*240
												C = C2*1 + C1*8 + C0*32
												P = P0*1
												Q = Q2*1 + Q1*1 + Q0*1
												R = 0
												S = 0
												worktile.append(tensor[R,S,C,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

0
def decomp_worktiles(tensor, b):
	if b == 1:
		print('Running decomp1()')
		return decomp1(tensor)
	elif b == 2:
		print('Running decomp2()')
		return decomp2(tensor)
	elif b == 3:
		print('Running decomp3()')
		return decomp3(tensor)
	elif b == 4:
		print('Running decomp4()')
		return decomp4(tensor)
	elif b == 5:
		print('Running decomp5()')
		return decomp5(tensor)
	elif b == 6:
		print('Running decomp6()')
		return decomp6(tensor)
	elif b == 7:
		print('Running decomp7()')
		return decomp7(tensor)
	elif b == 8:
		print('Running decomp8()')
		return decomp8(tensor)
	elif b == 9:
		print('Running decomp9()')
		return decomp9(tensor)
	elif b == 10:
		print('Running decomp10()')
		return decomp10(tensor)
	elif b == 11:
		print('Running decomp11()')
		return decomp11(tensor)
	elif b == 12:
		print('Running decomp12()')
		return decomp12(tensor)
	elif b == 13:
		print('Running decomp13()')
		return decomp13(tensor)
	elif b == 14:
		print('Running decomp14()')
		return decomp14(tensor)
	elif b == 15:
		print('Running decomp15()')
		return decomp15(tensor)
	elif b == 16:
		print('Running decomp16()')
		return decomp16(tensor)
