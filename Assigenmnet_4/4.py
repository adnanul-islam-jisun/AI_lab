import numpy as np
import random


data_path = 'AI_lab\Assigenmnet_4\jain_feats.txt'
data = np.genfromtxt(data_path, delimiter=' ')

# Function for K-Means Clustering
def k_means_clustering(data, k):
    # Initialize cluster centers
    center = []
    for i in range(k):
        rand = [random.randint(-3, 15), random.randint(-3, 15)]
        center.append(rand)
    print(f"Initial Centers for K={k}:", center)

    # K-Means Algorithm
    Clusters = [[] for i in range(k)]
    iteration = 0

    while True:
        Temp_Clusters = [[] for i in range(k)]
        data_index = 0

        for S in data:
            min_dist = float('inf')
            min_index = -1

            for index, C in enumerate(center):
                dist = np.linalg.norm(S - C)
                if dist < min_dist:
                    min_dist = dist
                    min_index = index

            Temp_Clusters[min_index].append(data_index)
            data_index += 1

        for L in range(len(Temp_Clusters)):
            avg = np.zeros(2)
            for x in Temp_Clusters[L]:
                avg += data[x] / len(Temp_Clusters[L])
            center[L] = avg

        iteration += 1

        if iteration > 1:
            Shift = 0
            for S in range(len(data)):
                cluster_index = None
                temp_index = None
                for i, x in enumerate(Temp_Clusters):
                    if S in x:
                        temp_index = i
                for i, x in enumerate(Clusters):
                    if S in x:
                        cluster_index = i
                if cluster_index != temp_index:
                    Shift += 1

            Shift_Percentage = (Shift / len(data)) * 100

            if Shift_Percentage < 10:
                Clusters = Temp_Clusters
                break

        Clusters = Temp_Clusters

    return Clusters, center

# Train the K-Means model
k_value = 4  # You can choose the desired number of clusters
clusters, centers = k_means_clustering(data, k_value)

# Function to find the cluster for a given data point
def find_cluster(data_point, centers):
    min_dist = float('inf')
    min_index = -1

    for index, center in enumerate(centers):
        dist = np.linalg.norm(data_point - center)
        if dist < min_dist:
            min_dist = dist
            min_index = index

    return min_index

# User input to find cluster based on student ID
user_student_id = int(input("Enter your student ID: "))
random.seed(user_student_id)  # Using the entered student ID for random seed
user_data_point = np.random.rand(2)  # Replace this with actual data for the user

user_cluster = find_cluster(user_data_point, centers)
print(f"Student with ID {user_student_id} belongs to Cluster {user_cluster + 1}")
