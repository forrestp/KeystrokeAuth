import numpy as np

def checkTimings(testTiming, realTiming):
	np_test = np.array(testTiming)
	np_real = np.array(realTiming)
	n = len(testTiming)

	# Currenly the identity matrix
	S = np.identity(n)

	# calculate mahabolonis distance
	temp = np.dot(np.dot(np.transpose(np_test - np_real), np.linalg.inv(S)),(np_test - np_real))
	print temp
	mh_distance = temp ** 0.5

	print mh_distance
	return True


array1 = [1,10,15,20]
array2 = [2,12,18,22]
checkTimings(array1,array2)
