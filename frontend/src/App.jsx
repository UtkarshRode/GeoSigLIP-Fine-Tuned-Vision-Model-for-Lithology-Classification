import { useRef, useState } from "react";
import {
  CheckCircle2,
  ChevronRight,
  Image as ImageIcon,
  Loader2,
  RotateCcw,
  Sparkles,
  Upload,
} from "lucide-react";

import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFile = (file) => {
    if (!file) return;

    if (!file.type.startsWith("image/")) {
      setError("Please select a valid image file.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("Image size must be below 10 MB.");
      return;
    }

    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setError("");
  };

  const handleInputChange = (event) => {
    handleFile(event.target.files?.[0]);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    handleFile(event.dataTransfer.files?.[0]);
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError("Please select a rock image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Prediction failed."
        );
      }

      setResult(data);
    } catch (err) {
      setError(
        err.message ||
          "Could not connect to the prediction server."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }

    setSelectedFile(null);
    setPreviewUrl("");
    setResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="brand-mark">
            <Sparkles size={18} />
          </div>

          <div>
            <div className="brand-name">
              GeoSigLIP
            </div>

            <div className="brand-description">
              Geological Lithology Classifier
            </div>
          </div>
        </div>

        <div className="header-right">
          <div className="status-pill">
            <span className="status-dot" />
            Model ready
          </div>

          <div className="model-pill">
            SigLIP · LoRA
          </div>
        </div>
      </header>

      <main className="container">
        <section className="hero">
          <div className="eyebrow">
            <Sparkles size={14} />
            AI-POWERED GEOLOGICAL ANALYSIS
          </div>

          <h1>
            Identify lithology
            <br />
            from a rock image.
          </h1>

          <p>
            GeoSigLIP analyzes geological imagery and
            predicts the most likely lithology using
            a SigLIP vision model fine-tuned with LoRA
            on the DCID-7 dataset.
          </p>
        </section>

        <section className="workspace">
          <div className="panel upload-panel">
            <div className="panel-header">
              <div>
                <div className="panel-kicker">
                  STEP 01
                </div>

                <h2>Upload sample</h2>

                <p>
                  Add a clear geological rock image.
                </p>
              </div>

              {selectedFile && (
                <button
                  className="reset-button"
                  type="button"
                  onClick={resetApp}
                >
                  <RotateCcw size={14} />
                  Reset
                </button>
              )}
            </div>

            {!previewUrl ? (
              <div
                className="drop-zone"
                onDragOver={(event) =>
                  event.preventDefault()
                }
                onDrop={handleDrop}
                onClick={() =>
                  fileInputRef.current?.click()
                }
              >
                <div className="upload-mark">
                  <Upload size={25} />
                </div>

                <h3>
                  Drop your rock image here
                </h3>

                <p>
                  or browse files from your computer
                </p>

                <button
                  className="browse-button"
                  type="button"
                  onClick={(event) => {
                    event.stopPropagation();
                    fileInputRef.current?.click();
                  }}
                >
                  Choose image
                  <ChevronRight size={15} />
                </button>

                <div className="upload-hint">
                  JPG, JPEG or PNG · Max 10 MB
                </div>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/png,image/jpeg,image/jpg"
                  onChange={handleInputChange}
                  hidden
                />
              </div>
            ) : (
              <div className="preview-card">
                <img
                  src={previewUrl}
                  alt="Uploaded geological sample"
                  className="preview-image"
                />

                <div className="file-row">
                  <div className="file-icon">
                    <ImageIcon size={16} />
                  </div>

                  <div className="file-details">
                    <span className="file-name">
                      {selectedFile.name}
                    </span>

                    <span className="file-meta">
                      {(
                        selectedFile.size /
                        (1024 * 1024)
                      ).toFixed(2)}
                      {" MB"}
                    </span>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="error-box">
                {error}
              </div>
            )}

            <button
              className="predict-button"
              disabled={!selectedFile || loading}
              onClick={handlePredict}
              type="button"
            >
              {loading ? (
                <>
                  <Loader2
                    size={17}
                    className="spinner"
                  />
                  Analyzing sample...
                </>
              ) : (
                <>
                  <Sparkles size={17} />
                  Analyze lithology
                </>
              )}
            </button>
          </div>

          <div className="panel results-panel">
            <div className="panel-header">
              <div>
                <div className="panel-kicker">
                  STEP 02
                </div>

                <h2>Analysis</h2>

                <p>
                  Model inference and confidence scores.
                </p>
              </div>
            </div>

            {!result ? (
              <div className="empty-state">
                <div className="empty-mark">
                  <Sparkles size={24} />
                </div>

                <h3>
                  Awaiting image analysis
                </h3>

                <p>
                  Your predicted lithology and top
                  alternatives will appear here.
                </p>
              </div>
            ) : (
              <div className="result-content">
                <div className="primary-result">
                  <div className="result-label">
                    Predicted lithology
                  </div>

                  <div className="result-title">
                    {result.predicted_lithology}
                  </div>

                  <div className="result-confidence">
                    <CheckCircle2 size={16} />

                    <span>
                      {result.confidence_percent}%
                      confidence
                    </span>
                  </div>
                </div>

                <div className="confidence-track">
                  <div
                    className="confidence-progress"
                    style={{
                      width: `${Math.min(
                        result.confidence_percent,
                        100
                      )}%`,
                    }}
                  />
                </div>

                <div className="alternatives">
                  <div className="alternatives-heading">
                    <span>
                      Top predictions
                    </span>

                    <span>
                      Confidence
                    </span>
                  </div>

                  <div className="prediction-list">
                    {result.top_k_predictions.map(
                      (item, index) => (
                        <div
                          className={`prediction-row ${
                            index === 0
                              ? "top-row"
                              : ""
                          }`}
                          key={`${item.label}-${index}`}
                        >
                          <div className="rank-badge">
                            {index + 1}
                          </div>

                          <div className="prediction-name">
                            {item.label}
                          </div>

                          <div className="prediction-value">
                            {
                              item.confidence_percent
                            }
                            %
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>

                <div className="result-note">
                  <Sparkles size={15} />

                  <span>
                    Prediction generated by the
                    fine-tuned GeoSigLIP model.
                  </span>
                </div>
              </div>
            )}
          </div>
        </section>

        <section className="metrics-section">
          <div className="metric-card">
            <div className="metric-value">
              99.886%
            </div>

            <div className="metric-label">
              Test accuracy
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-value">
              99.886%
            </div>

            <div className="metric-label">
              Macro F1
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-value">
              1,750
            </div>

            <div className="metric-label">
              Test images
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-value">
              7
            </div>

            <div className="metric-label">
              Lithology classes
            </div>
          </div>
        </section>

        <section className="model-info">
          <div className="model-info-left">
            <div className="info-icon">
              <Sparkles size={17} />
            </div>

            <div>
              <h3>
                Domain-adapted vision model
              </h3>

              <p>
                SigLIP base model fine-tuned with
                parameter-efficient LoRA adaptation
                for geological image classification.
              </p>
            </div>
          </div>

          <div className="model-info-tags">
            <span>SigLIP</span>
            <span>LoRA</span>
            <span>DCID-7</span>
          </div>
        </section>
      </main>

      <footer className="footer">
        <span>
          GeoSigLIP
        </span>

        <span>
          Geological AI · DCID-7
        </span>
      </footer>
    </div>
  );
}

export default App;
