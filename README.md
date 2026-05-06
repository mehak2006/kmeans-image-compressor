# K-Means Image Compression Web App

A full-stack machine learning web application that compresses images using the K-Means clustering algorithm.

Built while studying the K-Means section of the Andrew Ng / DeepLearning.AI Machine Learning Specialization course on Coursera. While exploring applications of K-Means, I came across a Medium article on K-Means image compression and decided to implement and deploy the idea as a complete full-stack project.

---

# Live Demo

Frontend (Vercel):  
https://kmeans-image-compressor.vercel.app/

Backend API (Render):  
https://kmeans-image-compressor-backend.onrender.com/docs


---

# Features

- Upload and compress images using K-Means clustering
- Adjustable number of colour clusters (K)
- Real-time centroid colour palette visualization
- Memory-optimized K-Means implementation
- Batch assignment for large images
- FastAPI backend + React frontend
- Fully deployed using Render and Vercel

---

# How It Works

K-means clustering is applied to the pixel colours of an image.  
Each pixel is treated as a point in 3D RGB colour space.

The algorithm:
1. Initializes K centroids
2. Assigns each pixel to its nearest centroid
3. Updates centroid positions
4. Repeats until convergence

Finally, every pixel is replaced by its nearest centroid colour, reducing the image palette to exactly K colours.

---

# Optimization Techniques Used

Running K-Means directly on millions of pixels is computationally expensive, so several optimizations were implemented:

- Random pixel sampling for centroid learning
- Batched full-image assignment to avoid memory overflow
- Float32 memory optimization
- Image resizing for deployment stability
- Reduced batch/sample sizes for cloud deployment

These optimizations significantly reduced RAM usage and allowed deployment on free cloud infrastructure.

---

# Tech Stack

## Frontend
- React
- JavaScript
- CSS

## Backend
- FastAPI
- NumPy
- OpenCV

## Deployment
- Vercel (Frontend)
- Render (Backend)

---

# Challenges Faced

- Optimizing memory usage for large images
- Handling cloud deployment RAM limits
- Sending image data efficiently between frontend and backend
- Debugging multipart/form-data issues in FastAPI
- Managing frontend/backend integration during deployment

---

# Future Improvements

- Drag-and-drop uploads
- Better UI/UX and animations
- Download compressed image
- GPU acceleration
- Support for additional compression algorithms
- Compression statistics dashboard

---

# Project Structure

```text
project/
│
├── frontend/
│   ├── src/
│   ├── public/
│
├── main.py
├── kmeans.py
├── requirements.txt
```

---

# Running Locally

## Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm start
```

---
# Note

The backend is deployed on Render's free tier, which automatically sleeps after inactivity.  
Because of this, the **first upload/request may take around 30–60 seconds** while the backend wakes up. Subsequent requests are much faster.

---
```
# References

- Andrew Ng Machine Learning Specialization (Coursera)
- https://medium.com/data-science/clear-and-visual-explanation-of-the-k-means-algorithm-applied-to-image-compression-b7fdc547e410

---

# Author

Built by Mehak Priyadarshi (2026)