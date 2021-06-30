import numpy as np
def comp1(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(4): 
		for C0 in range(4): 
			# shared_glb
			for P0 in range(32): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M0 in range(3): # (Spatial-Y)
							for C1 in range(3): # (Spatial-Y)
								x = Q1*1
								y = C1*1 + M0*3
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(8): 
										# psum_spad
										for M1 in range(8): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*8 + C0*24
											P = P0*1
											M = M1*1 + M0*8
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp2(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(2): # (Spatial-X)
				for Q1 in range(4): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for C0 in range(9): # (Spatial-Y)
							x = Q1*1 + M0*4
							y = C0*1
							worktile = []
							# ifmap_spad
							for Q3 in range(1): 
								# weights_spad
								for C1 in range(16): 
									# psum_spad
									for M1 in range(12): 
										Q = Q3*1 + Q2*1 + Q1*1 + Q0*4
										P = P0*1
										M = M1*1 + M0*12
										C = C1*1 + C0*16
										R = 0
										S = 0
										worktile.append(tensor[R,S,C,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp3(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for C0 in range(9): # (Spatial-Y)
						x = M0*1
						y = C0*1
						worktile = []
						# ifmap_spad
						for Q2 in range(1): 
							# weights_spad
							for C1 in range(8): 
								# psum_spad
								for M1 in range(5): 
									Q = Q2*1 + Q1*1 + Q0*1
									P = P0*1
									M = M1*1 + M0*5
									C = C1*1 + C0*8
									R = 0
									S = 0
									worktile.append(tensor[R,S,C,M])
						if (x,y) in worktiles.keys():
							worktiles[(x,y)].append(np.array(worktile))
						else:
							worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp4(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for P0 in range(16): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M0 in range(2): # (Spatial-Y)
							for C1 in range(4): # (Spatial-Y)
								x = Q1*1
								y = C1*1 + M0*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(6): 
										# psum_spad
										for M1 in range(20): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*6 + C0*24
											P = P0*1
											M = M1*1 + M0*20
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp5(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for P0 in range(16): 
				for Q1 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M0 in range(2): # (Spatial-Y)
							for C1 in range(4): # (Spatial-Y)
								x = Q1*1
								y = C1*1 + M0*4
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(6): 
										# psum_spad
										for M1 in range(20): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*6 + C0*24
											P = P0*1
											M = M1*1 + M0*20
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp6(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for M0 in range(4): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C1 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C1*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(6): 
										# psum_spad
										for M1 in range(20): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*6 + C0*48
											M = M1*1 + M0*20
											P = P0*1
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp7(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for M0 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C1 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C1*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(12): 
										# psum_spad
										for M1 in range(10): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*12 + C0*96
											M = M1*1 + M0*10
											P = P0*1
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp8(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for M0 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C1 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C1*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(12): 
										# psum_spad
										for M1 in range(10): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*12 + C0*96
											M = M1*1 + M0*10
											P = P0*1
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp9(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for M0 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C1 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C1*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(12): 
										# psum_spad
										for M1 in range(10): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*12 + C0*96
											M = M1*1 + M0*10
											P = P0*1
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp10(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for C0 in range(5): 
			# shared_glb
			for M0 in range(8): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for C1 in range(8): # (Spatial-Y)
								x = Q1*1
								y = C1*1
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for C2 in range(12): 
										# psum_spad
										for M1 in range(14): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
											C = C2*1 + C1*12 + C0*96
											M = M1*1 + M0*14
											P = P0*1
											R = 0
											S = 0
											worktile.append(tensor[R,S,C,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp11(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(2): 
			for C0 in range(12): 
				# shared_glb
				for M1 in range(2): 
					for P0 in range(16): 
						for Q1 in range(8): # (Spatial-X)
							# DummyBuffer
							for Q2 in range(1): 
								for M2 in range(2): # (Spatial-Y)
									for C1 in range(4): # (Spatial-Y)
										x = Q1*1
										y = C1*1 + M2*4
										worktile = []
										# ifmap_spad
										for Q3 in range(1): 
											# weights_spad
											for C2 in range(14): 
												# psum_spad
												for M3 in range(14): 
													Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
													M = M3*1 + M2*14 + M1*28 + M0*56
													C = C2*1 + C1*14 + C0*56
													P = P0*1
													R = 0
													S = 0
													worktile.append(tensor[R,S,C,M])
										if (x,y) in worktiles.keys():
											worktiles[(x,y)].append(np.array(worktile))
										else:
											worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def comp12(tensor):
	worktiles = {}
	# DRAM
	for C0 in range(28): 
		# shared_glb
		for M0 in range(5): 
			for P0 in range(8): 
				for Q0 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q1 in range(1): 
						for M1 in range(4): # (Spatial-Y)
							for C1 in range(2): # (Spatial-Y)
								x = Q0*1
								y = C1*1 + M1*2
								worktile = []
								# ifmap_spad
								for Q2 in range(1): 
									# weights_spad
									for C2 in range(12): 
										# psum_spad
										for M2 in range(8): 
											C = C2*1 + C1*12 + C0*24
											M = M2*1 + M1*8 + M0*32
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

def comp13(tensor):
	worktiles = {}
	# DRAM
	for C0 in range(30): 
		# shared_glb
		for M0 in range(5): 
			for P0 in range(8): 
				for Q0 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q1 in range(1): 
						for M1 in range(4): # (Spatial-Y)
							for C1 in range(2): # (Spatial-Y)
								x = Q0*1
								y = C1*1 + M1*2
								worktile = []
								# ifmap_spad
								for Q2 in range(1): 
									# weights_spad
									for C2 in range(16): 
										# psum_spad
										for M2 in range(8): 
											C = C2*1 + C1*16 + C0*32
											M = M2*1 + M1*8 + M0*32
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

def comp14(tensor):
	worktiles = {}
	# DRAM
	for C0 in range(30): 
		# shared_glb
		for M0 in range(5): 
			for P0 in range(8): 
				for Q0 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q1 in range(1): 
						for M1 in range(4): # (Spatial-Y)
							for C1 in range(2): # (Spatial-Y)
								x = Q0*1
								y = C1*1 + M1*2
								worktile = []
								# ifmap_spad
								for Q2 in range(1): 
									# weights_spad
									for C2 in range(16): 
										# psum_spad
										for M2 in range(8): 
											C = C2*1 + C1*16 + C0*32
											M = M2*1 + M1*8 + M0*32
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

def comp15(tensor):
	worktiles = {}
	# DRAM
	for C0 in range(30): 
		# shared_glb
		for M0 in range(16): 
			for P0 in range(8): 
				for Q0 in range(8): # (Spatial-X)
					# DummyBuffer
					for Q1 in range(1): 
						for M1 in range(2): # (Spatial-Y)
							for C1 in range(4): # (Spatial-Y)
								x = Q0*1
								y = C1*1 + M1*4
								worktile = []
								# ifmap_spad
								for Q2 in range(1): 
									# weights_spad
									for C2 in range(8): 
										# psum_spad
										for M2 in range(10): 
											C = C2*1 + C1*8 + C0*32
											M = M2*1 + M1*10 + M0*20
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

1
def comp_worktiles(tensor, b):
	if b == 1:
		print('Running comp1()')
		return comp1(tensor)
	elif b == 2:
		print('Running comp2()')
		return comp2(tensor)
	elif b == 3:
		print('Running comp3()')
		return comp3(tensor)
	elif b == 4:
		print('Running comp4()')
		return comp4(tensor)
	elif b == 5:
		print('Running comp5()')
		return comp5(tensor)
	elif b == 6:
		print('Running comp6()')
		return comp6(tensor)
	elif b == 7:
		print('Running comp7()')
		return comp7(tensor)
	elif b == 8:
		print('Running comp8()')
		return comp8(tensor)
	elif b == 9:
		print('Running comp9()')
		return comp9(tensor)
	elif b == 10:
		print('Running comp10()')
		return comp10(tensor)
	elif b == 11:
		print('Running comp11()')
		return comp11(tensor)
	elif b == 12:
		print('Running comp12()')
		return comp12(tensor)
	elif b == 13:
		print('Running comp13()')
		return comp13(tensor)
	elif b == 14:
		print('Running comp14()')
		return comp14(tensor)
	elif b == 15:
		print('Running comp15()')
		return comp15(tensor)
	elif b == 16:
		print('Running comp16()')
		return comp16(tensor)
