import { useState } from "react";

export default function App() {
  const [output, setOutput] = useState(null);
  const [file, setFile] = useState(null);
  const [k, setK] = useState(16);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [centroids, setCentroids] = useState([]);

  const handleCompress = async () => {
    if (!file) {
      alert("Please select a file first");
      return;
    }

    setLoading(true);

    

    const formData = new FormData();
    formData.append("file", file);
    formData.append("k", parseInt(k));

    const response = await fetch("https://kmeans-image-compressor-backend.onrender.com/compress",  {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    const imageUrl = `data:image/jpeg;base64,${data.image}`;
    setCentroids(data.centroids);
    setOutput(imageUrl);

    setOutput(imageUrl);
    setLoading(false);
  };

  return (
    <div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "30px",
          fontFamily: "'DM Mono', monospace",
        }}
      >
        <h1
          style={{
            fontWeight: 400,
            letterSpacing: "-0.5px",
            borderBottom: "1px solid #ccc",
            paddingBottom: "12px",
            marginBottom: "32px",
          }}
        >
          Image Compressor(K-Means)
        </h1>

        <input
          type="file"
          onChange={(e) => {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);
            setPreview(URL.createObjectURL(selectedFile));
          }}
          style={{ marginBottom: "20px" }}
        />
        <br />
        <br />

        <input
          type="number"
          value={k}
          onChange={(e) => setK(e.target.value)}
          style={{
            padding: "8px",
            width: "100px",
            marginBottom: "20px",
            border: "1px solid #ccc",
            borderRadius: "0",
            fontFamily: "inherit",
          }}
        />
        <br />
        <br />

        <button
          onClick={handleCompress}
          disabled={loading}
          style={{
            padding: "10px 24px",
            fontSize: "13px",
            cursor: "pointer",
            border: "1px solid #111",
            background: "transparent",
            letterSpacing: "2px",
            textTransform: "uppercase",
          }}
        >
          {loading ? "Processing..." : "Compress"}
        </button>

        
        {centroids.length > 0 && (
          <div style={{ marginTop: "24px" }}>
            <p style={{ fontSize: "12px", marginBottom: "10px" }}>
              Colour palette found by K-means
            </p>
            <div style={{ display: "flex", flexWrap: "wrap", gap: "6px" }}>
              {centroids.map((c, i) => (
                <div
                  key={i}
                  title={`RGB(${Math.round(c[2])}, ${Math.round(c[1])}, ${Math.round(c[0])})`}
                  style={{
                    width: "32px",
                    height: "32px",
                    background: `rgb(${Math.round(c[2])}, ${Math.round(c[1])}, ${Math.round(c[0])})`,
                    borderRadius: "4px",
                  }}
                />
              ))}
            </div>
          </div>
        )}

        <br />
        <br />

        {loading && <p>Processing...</p>}

        <div
          style={{
            display: "flex",
            gap: "40px",
            marginTop: "30px",
            flexWrap: "wrap",
            justifyContent: "center",
          }}
        >
          {preview && (
            <div>
              <h3>Original</h3>
              <img
                src={preview}
                alt="Preview"
                style={{
                  maxWidth: "400px",
                  borderRadius: "10px",
                }}
              />
            </div>
          )}

          {output && (
            <div>
              <h3>Compressed</h3>
              <img
                src={output}
                alt="Compressed"
                style={{
                  maxWidth: "400px",
                  borderRadius: "10px",
                }}
              />
            </div>
          )}
        </div>
        <div
          style={{
            maxWidth: "860px",
            margin: "60px auto 0",
            borderTop: "1px solid #ccc",
            paddingTop: "40px",
            fontFamily: "'DM Mono', monospace",
          }}
        >
          <h2
            style={{
              fontWeight: 400,
              fontSize: "1.4rem",
              marginBottom: "24px",
            }}
          >
            How this works
          </h2>

          <p
            style={{
              fontSize: "13px",
              lineHeight: "2",
              color: "#444",
              maxWidth: "640px",
            }}
          >
            K-means clustering is applied to the pixel colours of an image. Each
            pixel is a point in 3D colour space (R, G, B). The algorithm finds K
            cluster centres — called centroids — that best represent the colour
            distribution of the image. Every pixel is then replaced by its
            nearest centroid colour, reducing the palette to exactly K colours.
          </p>

          <p
            style={{
              fontSize: "13px",
              lineHeight: "2",
              color: "#444",
              maxWidth: "640px",
              marginTop: "16px",
            }}
          >
            Running K-means on millions of pixels is expensive, so instead of
            using the full image, a random sample of 50,000 pixels is used to
            learn the centroids. Once the centroids converge, every pixel in the
            full image is assigned to its nearest centroid in batches — this is
            the same result with a fraction of the compute.
          </p>

          <div
            style={{
              display: "flex",
              gap: "8px",
              alignItems: "center",
              flexWrap: "wrap",
              margin: "32px 0",
              fontSize: "12px",
              color: "#888",
            }}
          >
            {[
              "Sample pixels",
              "Init centroids",
              "Assign clusters",
              "Update centroids",
              "Converge",
              "Apply to full image",
            ].map((step, i, arr) => (
              <span
                key={i}
                style={{ display: "flex", alignItems: "center", gap: "8px" }}
              >
                <span
                  style={{
                    padding: "6px 12px",
                    border: "1px solid #ccc",
                    fontSize: "11px",
                    letterSpacing: "1px",
                  }}
                >
                  {step}
                </span>
                {i < arr.length - 1 && <span style={{ color: "#bbb" }}>→</span>}
              </span>
            ))}
          </div>

          <a
            href="https://medium.com/data-science/clear-and-visual-explanation-of-the-k-means-algorithm-applied-to-image-compression-b7fdc547e410"
            target="_blank"
            rel="noreferrer"
            style={{
              fontSize: "12px",
              color: "#111",
              textDecoration: "none",
              borderBottom: "1px solid #ccc",
              paddingBottom: "2px",
              letterSpacing: "1px",
            }}
          >
            Read: K-Means applied to image compression ↗
          </a>
        </div>
        <footer
          style={{
            marginTop: "60px",
            borderTop: "1px solid #ccc",
            padding: "24px 0",
            textAlign: "center",
            fontSize: "11px",
            letterSpacing: "2px",
            color: "#888",
            textTransform: "uppercase",
          }}
        >
          Built by Mehak Priyadarshi 2026
        </footer>
      </div>
    </div>
  );
}
