import numpy as np
# import more_data as data

####### test vs averaged training vectors mahabolnis distance function ########
# finds m_distance between testTiming and realTiming(typically vector of averages)
# uses covariance matrix S in calculation
# returns boolean if distance is below a certain threshold
def checkTimings(testTiming, realTiming, S, threshold=None):
	# convert ms data to seconds before computing m_distance
	np_test = .01 * np.array(testTiming) 
	np_real = .01 * np.array(realTiming)
	n = len(testTiming)

	# check if S has inverse
	if np.linalg.det(S) != 0:
		S = np.linalg.inv(S)

	# calculate mahabolonis distance
	mh_distance = np.dot(np.dot(np.transpose(np_test - np_real), S),(np_test - np_real)) ** 0.5
	print "MH_Distance: " + str(mh_distance)

	# currently using static threshold, may need to make this dynamic but not sure right now
	if (threshold == None):
		threshold = (n**1.7)*.1
	if mh_distance < threshold:
		return True
	return False

####### K nearest mahabolnis distance function ########
# finds k closest m_distances between testTiming and each vector in realTimings
# uses covariance matrix S in computation of m_distances
# returns true if all of k closest m_distances is below threshold
def checkTimingsK(testTiming, realTimings, S, k, threshold=None):
	np_test = .01 * np.array(testTiming)
	n = len(testTiming)

	# check if S has inverse
	if np.linalg.det(S) != 0:
		S = np.linalg.inv(S)

	# Find k closest vectors in training data
	k_closest_distances = [100000] * k
	for vector in realTimings:
		np_vector = .01 * np.array(vector)
		mh_distance = np.dot(np.dot(np.transpose(np_test - np_vector), S),(np_test - np_vector)) ** 0.5
		print "MH_Distance: " + str(mh_distance)
		if max(k_closest_distances) > mh_distance:
			k_closest_distances.remove(max(k_closest_distances))
			k_closest_distances.append(mh_distance)

	print "K closest Distance: " + str(k_closest_distances)
	k_furthest_distance = max(k_closest_distances)
	if (threshold == None):
		threshold = (n**1.7)*0.1
	if k_furthest_distance < threshold:
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
	np_temp = .01 * np.array(timings)
	covariance_matrix = np.cov(np_temp.T)
	return covariance_matrix


# take in data for key strokes
# return an array of vectors that contain the down times of the keystrokes
def textToVectors(data):
	out_vectors = []
	for vector in data:
		out_vector = []
		offset = len('"down":')
		marker = vector.find('"down":')
		while marker != -1:
			end_marker = vector.find(',',marker+offset)
			if end_marker == -1:
				end_marker = vector.find('}', marker+offset)
			out_vector.append(int(vector[marker+offset:end_marker]))
			marker = vector.find('"down":', end_marker+1)
		out_vectors.append(out_vector)
	return out_vectors

# testing
# array1 = [1,10,15,20]
# timings = [[2,11,14,21],[2,11,15,21],[2,12,14,21]]
# S = compute_covariance_matrix(timings)
# array2 = get_median_timing(timings)
# checkTimings(array1,array2,S)
# tuan_data = textToVectors(data.tuan)[12:]
# print tuan_data
# tuan_mean = getMedianTiming(tuan_data)
# tuan_S = computeCovarianceMatrix(tuan_data)
# print tuan_mean
# print tuan_S
# print checkTimings(tuan_data[0],tuan_mean,tuan_S)
# print checkTimingsK(tuan_data[0],tuan_data,tuan_S,3)


