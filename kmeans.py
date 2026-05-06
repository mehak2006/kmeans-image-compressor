

import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import random

# now let's initialize centroids

def init_centroids(k, image):
    dimensions = image.shape
    L = dimensions[0]
    centroids = []
    for i in range(k):
        coordinate = random.randint(0, L - 1)
        centroids.append(image[coordinate])
    return np.array(centroids)


# assign clusters to each point,, for this let us first compute distance of each point from centroid of that cluster

# however first lets create a distance array of(N, K) which stores the distance of a point from all k centroids

def compute_distancesANDassign(image, centroids):
    # now let's use vectorization to make this optimized
    diff = image[:, None, :] - centroids[None, : , :]
    # this gives us an np array of size(N, K, 3)
    # now we need to square each term of R, G, B and add to form array of size(N, K)
    distances = np.sum(diff**2, axis = 2)
    assignments = np.argmin(distances, axis = 1)

    return assignments


# Assignment of clusters


def update_centroids(image, K, assignments):
    
    new_centroids = np.zeros((K, 3))
    for k in range(K):
        points = image[assignments == k] # boolean mask : selects all pixels in cluster k

        if len(points) > 0 :
            new_centroids[k] = np.mean(points, axis = 0)
        else:
            new_centroids[k] = image[np.random.randint(0, image.shape[0])]
    return new_centroids



# now we'll write the k_means function but instead of stopping after fixed number of iterations we'll do a convergence check
# we'll do this by measuring shifts in old_centroid to new_centroid


def k_means(K, image, tol, max_iters = 100):

    centroids = init_centroids(K, image)
    for iter in range(max_iters):
        old_centroids = centroids.copy()
        assignments = compute_distancesANDassign(image, centroids)
        centroids = update_centroids(image, K, assignments)
        shift = np.linalg.norm(centroids - old_centroids, axis=1).max()
        if(shift < tol):
            break

    return centroids, assignments



def sample_pixels(X, sample_size):
    indices = np.random.choice(X.shape[0], sample_size, replace=False)
    return X[indices]

def assign_full_batched(X, centroids, batch_size=100000):
    N = X.shape[0]
    assignments = np.empty(N, dtype=np.int32)

    for i in range(0, N, batch_size):
        batch = X[i:i+batch_size]

        diff = batch[:, None, :] - centroids[None, :, :]
        distances = np.sum(diff**2, axis=2)

        assignments[i:i+batch_size] = np.argmin(distances, axis=1)

    return assignments


def compress_image_kmeans(original_image, K = 16):
    H, W = original_image.shape[:2]

    # Flatten full image
    
    X_full = original_image.reshape(-1, 3).astype(np.float32)

   
    sample_size = min(50000, X_full.shape[0])# try 50k–200k depending on RAM
    X_sample = sample_pixels(X_full, sample_size)

   
    centroids, _ = k_means(K, X_sample, tol=0.01)
    assignments_full = assign_full_batched(X_full, centroids)

    
    X_compressed = centroids[assignments_full]

   
    X_compressed = np.clip(X_compressed, 0, 255).astype(np.uint8)

    image_compressed = X_compressed.reshape(H, W, 3)

    return image_compressed, centroids










