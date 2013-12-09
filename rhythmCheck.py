import numpy as np

def checkTimings(testTiming, realTiming, S):
	np_test = np.array(testTiming)
	np_real = np.array(realTiming)
	n = len(testTiming)

	# calculate mahabolonis distance
	#inverse_S = np.linalg.inv(S)
	temp = np.dot(np.dot(np.transpose(np_test - np_real), S),(np_test - np_real))
	mh_distance = temp ** 0.5

	# currently using static threshold, may need to make this dynamic but not sure right now
	if mh_distance < 5:
		return True
	return False

# takes in initial timing data
# returns array with mean times of keystrokes
def get_median_timing(timings):
	elements = len(timings)
	n = len(timings[0])
	out = np.zeros(n)
	for data in timings:
		out += np.array(data)
	out /= elements
	return out.tolist()

# takes in initial timing data
# computes covariance matrix and returns it
def compute_covariance_matrix(timings):
	n = len(timings)
	np_temp = np.array(timings)
	covariance_matrix = np.cov(np_temp.T)
	return covariance_matrix


# testing
# array1 = [1,10,15,20]
# timings = [[2,11,14,21],[2,11,15,21],[2,12,14,21]]
# S = compute_covariance_matrix(timings)
# array2 = get_median_timing(timings)
# checkTimings(array1,array2,S)