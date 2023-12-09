import random
import matplotlib.pyplot as plt

# Set the seed with your student ID
seed_value = 123456789
random.seed(seed_value)

# Step 2: Load dataset into 2D list "Data"
# Assume 'data' is your dataset in the form of a 2D list
# Replace this with your actual dataset
# Example: data = [[x1, y1], [x2, y2], ...]
data = ...

# Step 3: Randomly select K different data points from "Data"
K = 4
centers = random.sample(data, K)

# Step 4: Initialize Clusters
clusters = [[] for _ in range(K)]

# Step 5-24: K-means algorithm
itr = 1
shift = 0

while True:
    # Assign data points to clusters
    temp_clusters = [[] for _ in range(K)]
    for point in data:
        distances = [sum((point[i] - center[i]) ** 2 for i in range(len(point))) for center in centers]
        closest_center = distances.index(min(distances))
        temp_clusters[closest_center].append(point)

    # Check for convergence
    if itr > 1 and shift < 50:
        break

    shift = 0

    # Update centers
    for i, cluster in enumerate(temp_clusters):
        if cluster:
            new_center = [sum(point[j] for point in cluster) / len(cluster) for j in range(len(point))]
            centers[i] = new_center

    # Check for shifting data points between clusters
    for i in range(K):
        for j in range(K):
            if i != j:
                for point in clusters[i]:
                    if point in temp_clusters[j]:
                        shift += 1

    # Assign temp_clusters to clusters
    clusters = temp_clusters

    itr += 1

# Step 25: Plot clusters with appropriate colors
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
for i, cluster in enumerate(clusters):
    x_vals = [point[0] for point in cluster]
    y_vals = [point[1] for point in cluster]
    plt.scatter(x_vals, y_vals, c=colors[i], label=f'Cluster {i+1}')

# Step 26-28: Calculate inertia
inertia = 0
for i, cluster in enumerate(clusters):
    center = centers[i]
    inertia += sum(sum((point[j] - center[j]) ** 2 for j in range(len(point))) for point in cluster)

plt.scatter([center[0] for center in centers], [center[1] for center in centers], marker='x', c='k', label='Centers')
plt.legend()
plt.show()

print("Inertia:", inertia)
