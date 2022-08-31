from ast import literal_eval
from random import sample
import numpy as np

#constants 
n_rows = 11
n_cols = 11
n_anchors = 6
samples_per_anchor = 5
dory_rssi =  [-57,-63,-58,-64,-63,-66]

#paths for coap and mqtt entry sets
dataset_file = open('input.txt', 'r')
output_file = open('output.txt','w')

#function that computes the average anchor rssi dataset by given two near positions
def compute_average_rssi2(v1, v2):
    res = np.zeros((samples_per_anchor))
    for i in range(0,samples_per_anchor):
        res[i] = (v1[i]+v2[i])/2
    return res

#function that computes the average anchor rssi dataset by given four near positions
def compute_average_rssi4(v1, v2, v3, v4):
    res = np.zeros((samples_per_anchor))
    for i in range(0,samples_per_anchor):
        res[i] = (v1[i]+v2[i]+v3[i]+v4[i])/4
    return res

def euclidean_distance(vector_a, vector_b):
    # calculating the sum of squares
    sum_vectors = np.sum(np.square(vector_a-vector_b))
    # calculating the square root and retrieving the euclidean distance
    return np.sqrt(sum_vectors)

#initializing 4d array (with all zeros)
print("Initializing positions array...", end='')
positions = np.zeros((
    n_rows,                 # number of rows in the grid
    n_cols,                 # number of columns in the grid
    n_anchors,              # number of known anchors
    samples_per_anchor      # number of samples per vector at each position
))
print("done!")

#reading from entry sets file
print("Reading from entry sets file (dataset.txt)...", end='')
for line in dataset_file:
    lines = line.split('||')
    x_pos = int(lines[0].split(',')[0].split('.')[0])   # compute the X position
    y_pos = int(lines[0].split(',')[1].split('.')[0])   # compute the Y position
    for i in range(1,len(lines)):
        positions[x_pos][y_pos][i-1] = lines[i].split(',')  # put the values of RSSI in the matrix at the given position
print("done!")

# #printing all given positions (only even should be different from ZERO)
# for i in range(0,n_rows):
#     for j in range(0, n_cols):
#         print("--- POS: (" + str(i) + "," + str(j) + ") ---")
#         print(positions[i][j])

# #checking if all entry sets have been successfully read (odd should be N, even should be S)
# for i in range(0,n_rows):
#     for j in range(0, n_cols):
#         if(positions[i][j][0][0] == 0):
#             print('N', end=' ')
#         else:
#             print('S', end=' ')
#     print()

print("Calculating the average RSSIs of odd positions...", end='')
#calculating the average RSSIs of odd positions given all the even positions
for i in range(0,n_rows):
    for j in range(0, n_cols):
        #if at least one index is odd then we need to calculate the possible RSSIs for each anchor
        if i%2!=0 or j%2!=0:
            if i%2!=0 and j%2!=0:
                #case 1: all the (i,j) indexes are odd
                for k in range(0,n_anchors):
                    positions[i][j][k] = compute_average_rssi4(positions[i-1][j-1][k], positions[i+1][j+1][k], positions[i+1][j-1][k], positions[i-1][j+1][k])
            elif i%2!=0 and j%2==0:
                #case 2: row position is odd, column position is even
                for k in range(0,n_anchors):
                    positions[i][j][k] = compute_average_rssi2(positions[i-1][j][k], positions[i+1][j][k])
            elif i%2==0 and j%2!=0:
                #case 3: row position is even, column position is odd
                for k in range(0,n_anchors):
                    positions[i][j][k] = compute_average_rssi2(positions[i][j-1][k], positions[i][j+1][k])
print("done!")

print("Saving all positions in output.txt file...", end='')
#printing all positions and saving it in output.txt file
for i in range(0,n_rows):
    for j in range(0, n_cols):
        # print("--- POS: (" + str(i) + "," + str(j) + ") ---")
        output_file.write(str(i)+".0," + str(j)+".0")
        # print(positions[i][j])
        for position in positions[i][j]:
            output_file.write(" || ")
            for index in range(0,len(position)):
                output_file.write(" " + str(int(position[index])))
                if(index < len(position) - 1):
                    output_file.write(",")
        output_file.write("\n")
print("done!")

# OBTAIN DORY'S POSITION USING EUCLIDEAN DISTANCE

curr_i = 0  # current X position (used to iterate)
curr_j = 0  # current Y position (used to iterate)
dory_i = 0  # Dory's probable X position
dory_j = 0  # Dory's probable Y position
curr_k = 0  # Current (best) K value found

print("Calculating Dory's position...", end='')
# iterating for each row of the grid
for curr_i in range (0,n_rows):
    # iterating for each column of the grid
    for curr_j in range(0,n_cols):
        # transpose the RSSIs matrix corresponding to a (i,j) grid position
        # this is done in order to find the euclidean distance for each sample at a given position
        rssi_transpose = np.transpose(positions[curr_i][curr_j])

        # calculate the K (euclidean distance) between the first sample and Dory's RSSIs array
        best_sample_k = euclidean_distance(rssi_transpose[0], dory_rssi)
        # calculating the K (euclidean distance) between other samples and Dory's RSSIs array iterating between samples
        for curr_sample in range(1,samples_per_anchor):
            curr_sample_k = euclidean_distance(rssi_transpose[curr_sample], dory_rssi)
            # if the K of the current sample is lower to the best found so far, then updates that value
            if(curr_sample_k < best_sample_k):
                best_sample_k = curr_sample_k
    
        # after finding the best K for a (i,j) position check if its value is lower than the best found so far
        if(curr_i == 0 and curr_j == 0):
            # in case it is the first K found, then directly replace the default value without any check
            curr_k = best_sample_k
        elif(best_sample_k < curr_k):
            # otherwise, check if the K just found is lower then the best one so far
            # if so, update the best K value with the one just found
            curr_k = best_sample_k
            # updates also Dory's X and Y position
            dory_i = curr_i
            dory_j = curr_j
        print("[" + str(curr_i) + "," + str(curr_j) + "] K=" + str(best_sample_k) + " -- Best so far: K_best=" + str(curr_k) + " at " + str(dory_i) + "," + str(dory_j))

print("done!\n")
print("DORY'S POSITION (according to Euclidean distance): " + str("(" + str(dory_i) + "," + str(dory_j) + ")"))