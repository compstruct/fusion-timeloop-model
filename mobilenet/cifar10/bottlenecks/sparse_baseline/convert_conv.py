import numpy as np
def conv1(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(32): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(4): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*4 + M0*12
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv2(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(4): # (Spatial-X)
				for Q1 in range(2): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(3): # (Spatial-Y)
							for S0 in range(3): # (Spatial-Y)
								x = Q1*1 + M0*2
								y = S0*1 + M1*3
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for R0 in range(3): 
										# psum_spad
										for M2 in range(12): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*2
											P = P0*1
											M = M2*1 + M1*12 + M0*36
											S = S0*1
											R = R0*1
											worktile.append(tensor[R,S,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv3(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(4): # (Spatial-X)
				for Q1 in range(2): # (Spatial-X)
					# DummyBuffer
					for Q2 in range(1): 
						for M1 in range(3): # (Spatial-Y)
							for S0 in range(3): # (Spatial-Y)
								x = Q1*1 + M0*2
								y = S0*1 + M1*3
								worktile = []
								# ifmap_spad
								for Q3 in range(1): 
									# weights_spad
									for R0 in range(3): 
										# psum_spad
										for M2 in range(12): 
											Q = Q3*1 + Q2*1 + Q1*1 + Q0*2
											P = P0*1
											M = M2*1 + M1*12 + M0*36
											S = S0*1
											R = R0*1
											worktile.append(tensor[R,S,M])
								if (x,y) in worktiles.keys():
									worktiles[(x,y)].append(np.array(worktile))
								else:
									worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv4(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(32): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(8): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*8 + M0*24
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv5(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(32): 
		# shared_glb
		for P0 in range(32): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(8): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*8 + M0*24
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv6(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(8): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*8 + M0*24
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv7(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(16): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*16 + M0*48
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv8(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(16): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*16 + M0*48
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv9(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(16): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*16 + M0*48
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv10(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(16): 
		# shared_glb
		for P0 in range(16): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(16): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*16 + M0*48
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv11(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(2): 
		for M0 in range(4): 
			# shared_glb
			for M1 in range(2): 
				for P0 in range(16): 
					for Q1 in range(8): # (Spatial-X)
						# DummyBuffer
						for Q2 in range(1): 
							for M2 in range(3): # (Spatial-Y)
								for S0 in range(3): # (Spatial-Y)
									x = Q1*1
									y = S0*1 + M2*3
									worktile = []
									# ifmap_spad
									for Q3 in range(1): 
										# weights_spad
										for R0 in range(3): 
											# psum_spad
											for M3 in range(24): 
												Q = Q3*1 + Q2*1 + Q1*1 + Q0*8
												M = M3*1 + M2*24 + M1*72 + M0*144
												P = P0*1
												S = S0*1
												R = R0*1
												worktile.append(tensor[R,S,M])
									if (x,y) in worktiles.keys():
										worktiles[(x,y)].append(np.array(worktile))
									else:
										worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv12(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		# shared_glb
		for P0 in range(8): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(24): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*24 + M0*72
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv13(tensor):
	worktiles = {}
	# DRAM
	for Q0 in range(8): 
		# shared_glb
		for P0 in range(8): 
			for M0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = M0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(24): 
										Q = Q2*1 + Q1*1 + Q0*1
										P = P0*1
										M = M2*1 + M1*24 + M0*72
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv14(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(16): 
		# shared_glb
		for P0 in range(8): 
			for Q0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = Q0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(20): 
										M = M2*1 + M1*20 + M0*60
										P = P0*1
										Q = Q2*1 + Q1*1 + Q0*1
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv15(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(16): 
		# shared_glb
		for P0 in range(8): 
			for Q0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = Q0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(20): 
										M = M2*1 + M1*20 + M0*60
										P = P0*1
										Q = Q2*1 + Q1*1 + Q0*1
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

def conv16(tensor):
	worktiles = {}
	# DRAM
	for M0 in range(16): 
		# shared_glb
		for P0 in range(8): 
			for Q0 in range(8): # (Spatial-X)
				# DummyBuffer
				for Q1 in range(1): 
					for M1 in range(3): # (Spatial-Y)
						for S0 in range(3): # (Spatial-Y)
							x = Q0*1
							y = S0*1 + M1*3
							worktile = []
							# ifmap_spad
							for Q2 in range(1): 
								# weights_spad
								for R0 in range(3): 
									# psum_spad
									for M2 in range(20): 
										M = M2*1 + M1*20 + M0*60
										P = P0*1
										Q = Q2*1 + Q1*1 + Q0*1
										S = S0*1
										R = R0*1
										worktile.append(tensor[R,S,M])
							if (x,y) in worktiles.keys():
								worktiles[(x,y)].append(np.array(worktile))
							else:
								worktiles[(x,y)] = [np.array(worktile)]
	return worktiles

2
def conv_worktiles(tensor, b):
	if b == 1:
		print('Running conv1()')
		return conv1(tensor)
	elif b == 2:
		print('Running conv2()')
		return conv2(tensor)
	elif b == 3:
		print('Running conv3()')
		return conv3(tensor)
	elif b == 4:
		print('Running conv4()')
		return conv4(tensor)
	elif b == 5:
		print('Running conv5()')
		return conv5(tensor)
	elif b == 6:
		print('Running conv6()')
		return conv6(tensor)
	elif b == 7:
		print('Running conv7()')
		return conv7(tensor)
	elif b == 8:
		print('Running conv8()')
		return conv8(tensor)
	elif b == 9:
		print('Running conv9()')
		return conv9(tensor)
	elif b == 10:
		print('Running conv10()')
		return conv10(tensor)
	elif b == 11:
		print('Running conv11()')
		return conv11(tensor)
	elif b == 12:
		print('Running conv12()')
		return conv12(tensor)
	elif b == 13:
		print('Running conv13()')
		return conv13(tensor)
	elif b == 14:
		print('Running conv14()')
		return conv14(tensor)
	elif b == 15:
		print('Running conv15()')
		return conv15(tensor)
	elif b == 16:
		print('Running conv16()')
		return conv16(tensor)
