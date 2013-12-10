import numpy as np

####### test vs averaged training vectors mahabolnis distance function ########
# finds m_distance between testTiming and realTiming(typically vector of averages)
# uses covariance matrix S in calculation
# returns boolean if distance is below a certain threshold
def checkTimings(testTiming, realTiming, S):
	np_test = np.array(testTiming)
	np_real = np.array(realTiming)
	n = len(testTiming)

	# check if S has inverse
	if np.linalg.det(S) != 0:
		S = np.linalg.inv(S)

	# calculate mahabolonis distance
	mh_distance = np.dot(np.dot(np.transpose(np_test - np_real), S),(np_test - np_real)) ** 0.5

	# currently using static threshold, may need to make this dynamic but not sure right now
	threshold = n * 0.5
	if mh_distance < threshold:
		return True
	return False

####### K nearest mahabolnis distance function ########
# finds k closest m_distances between testTiming and each vector in realTimings
# uses covariance matrix S in computation of m_distances
# returns true if all of k closest m_distances is below threshold
def checkTimings(testTiming, realTimings, S, k):
	np_test = np.array(testTiming)
	n = len(testTiming)

	# check if S has inverse
	if np.linalg.det(S) != 0:
		S = np.linalg.inv(S)

	# Find k closest vectors in training data
	k_closest_distances = []
	for vector in realTimings:
		np_vector = np.array(vector)
		mh_distance = np.dot(np.dot(np.transpose(np_test - vector), S),(np_test - vector)) ** 0.5
		if len(k_closest_distances) < k:
			k_closest_distances.append(mh_distance)
		elif max(k_closest_distances) > mh_distance:
			k_closest_distances.remove(max(k_closest_distances))
			k_closest_distances.append(mh_distance)

	k_furthest_distance = max(k_closest_distances)
	threshold = n * 0.5
	if k_furthest_distance <= threshold:
		return True
	return False


# takes in initial timing data
# returns array with mean times of keystrokes
def getMedianTiming(timings):
	elements = len(timings)
	n = len(timings[0])
	out = np.zeros(n)
	for data in timings:
		out += np.array(data)
	out /= elements
	return out.tolist()

# takes in initial timing data
# computes covariance matrix and returns it
def computeCovarianceMatrix(timings):
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