# kmeans.py
import numpy as np
import cv2
import random

def init_centroids(k, image):
    
    indices = np.random.choice(image.shape[0], k, replace=False)
    return image[indices].copy()  # shape (K, 3), float32

def compute_distances_and_assign(image, centroids):
    
    diff = image[:, None, :] - centroids[None, :, :]  # (N, K, 3) float32
    distances = np.sum(diff ** 2, axis=2)              # (N, K)
    assignments = np.argmin(distances, axis=1)
    return assignments

def update_centroids(image, K, assignments):
    new_centroids = np.zeros((K, 3), dtype=np.float32)  # float32 explicitly
    for k in range(K):
        mask = assignments == k
        if mask.any():
            new_centroids[k] = image[mask].mean(axis=0)
        else:
            new_centroids[k] = image[np.random.randint(0, image.shape[0])]
    return new_centroids

def k_means(K, image, tol=0.5, max_iters=20):
    
    centroids = init_centroids(K, image)
    for _ in range(max_iters):
        old_centroids = centroids.copy()
        assignments = compute_distances_and_assign(image, centroids)
        centroids = update_centroids(image, K, assignments)
        shift = np.linalg.norm(centroids - old_centroids, axis=1).max()
        if shift < tol:
            break
    return centroids, assignments

def assign_full_batched(X, centroids, batch_size=5000):
    N = X.shape[0]
    assignments = np.empty(N, dtype=np.int32)
    for i in range(0, N, batch_size):
        batch = X[i:i + batch_size]
        diff = batch[:, None, :] - centroids[None, :, :]
        distances = np.sum(diff ** 2, axis=2)
        assignments[i:i + batch_size] = np.argmin(distances, axis=1)
        
    return assignments

def compress_image_kmeans(original_image, K=16):
    import gc
    H, W = original_image.shape[:2]

    X_full = original_image.reshape(-1, 3).astype(np.float32)

    sample_size = min(2000, X_full.shape[0])
    indices = np.random.choice(X_full.shape[0], sample_size, replace=False)
    X_sample = X_full[indices]

    centroids, _ = k_means(K, X_sample, tol=0.5, max_iters=30)

    del X_sample
    gc.collect()

    assignments_full = assign_full_batched(X_full, centroids, batch_size=10000)

    del X_full
    gc.collect()

    X_compressed = centroids[assignments_full].clip(0, 255).astype(np.uint8)

    del assignments_full
    gc.collect()

    return X_compressed.reshape(H, W, 3), centroids