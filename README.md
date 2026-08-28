<div align="center">

# 🪨 GeoSigLIP

### Fine-Tuned Vision Model for Lithology Classification

**Domain-adapted geological image classification with SigLIP + LoRA**

<p>
<img src="https://img.shields.io/badge/Model-SigLIP-5C6BC0" alt="SigLIP">
<img src="https://img.shields.io/badge/Fine--Tuning-LoRA-7E57C2" alt="LoRA">
<img src="https://img.shields.io/badge/Task-7--Class%20Classification-2E7D32" alt="Task">
<img src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi" alt="FastAPI">
<img src="https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black" alt="React">
</p>

<p>
<img src="https://img.shields.io/badge/Test%20Accuracy-99.886%25-success" alt="Accuracy">
<img src="https://img.shields.io/badge/Macro%20F1-99.886%25-success" alt="F1">
<img src="https://img.shields.io/badge/Test%20Images-1%2C750-blue" alt="Test images">
<img src="https://img.shields.io/badge/Zero--Shot%20Accuracy-55.257%25-orange" alt="Zero shot">
</p>

</div>

---

## 🧠 Overview

**GeoSigLIP** is an end-to-end geological image classification system that adapts Google's pretrained **SigLIP** vision-language model to lithology recognition using **parameter-efficient LoRA fine-tuning**.

The project is built as a complete ML workflow:

**dataset preparation → EDA → zero-shot baseline → LoRA fine-tuning → held-out evaluation → robustness analysis → API inference → web application**

The final application accepts a geological rock image and returns a predicted lithology, confidence score, and top-3 alternatives.

---

## ⭐ Key Highlights

- Fine-tuned `google/siglip-base-patch16-224`
- LoRA-based parameter-efficient fine-tuning
- 7-class geological lithology classification
- 2,450 training images
- 1,050 validation images
- 1,750 held-out test images
- Zero-shot baseline for direct comparison
- Accuracy, Macro F1, per-class metrics, and confusion matrix
- SHA-256 exact-duplicate checks
- Visual-similarity screening across splits
- FastAPI inference backend
- React + Vite interactive frontend

---

## 📈 Results

### Held-out test performance

| Model | Accuracy | Macro F1 |
|:--|--:|--:|
| SigLIP Zero-Shot | 55.257% | 47.762% |
| **SigLIP + LoRA** | **99.886%** | **99.886%** |

### Improvement

| Metric | Gain |
|:--|--:|
| Accuracy | **+44.629 percentage points** |
| Macro F1 | **+52.124 percentage points** |

> The strong fine-tuned result was followed by a dedicated robustness and split-integrity analysis.

---

## 🧪 Robustness & Data Integrity

### Split overlap

```text
Train ∩ Validation = 0
Train ∩ Test       = 0
Validation ∩ Test  = 0
```

### Exact duplicates

SHA-256 analysis found:

```text
Cross-split exact duplicates = 0
Conflicting duplicate labels = 0
```

### Visual similarity screening

```text
Train → Validation = 0
Train → Test       = 4
Validation → Test  = 0
```

The four train-test pairs were flagged for inspection rather than automatically being treated as leakage.

---

## 🧠 Fine-Tuning Configuration

### Base model

```text
google/siglip-base-patch16-224
```

### LoRA

```text
Rank:            16
Alpha:           32
Dropout:         0.05
Target modules:  q_proj, v_proj
```

LoRA adapts selected transformer projections through low-rank trainable updates while keeping the pretrained backbone largely frozen.

---

## 🪨 Lithology Classes

| ID | Class |
|---:|:--|
| 1 | Red sandstone |
| 2 | Light sandstone |
| 3 | Gray siltstone |
| 4 | Mudstone |
| 5 | Granite |
| 6 | Basalt |
| 7 | Marble |

---

## 🔄 ML Pipeline

```text
DCID-7 Geological Images
          │
          ▼
Exploratory Data Analysis
          │
          ▼
SigLIP Zero-Shot Baseline
          │
          ▼
LoRA Fine-Tuning
          │
          ▼
Validation / Checkpoint
          │
          ▼
Held-Out Test Evaluation
          │
          ▼
Robustness Analysis
          │
          ▼
Trained Checkpoint
          │
          ▼
FastAPI Inference
          │
          ▼
React Application
```

---

## 🖥️ Application

The application provides an interactive geological-image inference workflow.

### User flow

```text
Upload / Drop Rock Image
          ↓
Image Preview
          ↓
Analyze Lithology
          ↓
FastAPI /predict
          ↓
GeoSigLIP + LoRA
          ↓
Prediction
          ↓
Confidence + Top-3
```

### Application preview

<p align="center">
  <img src="docs/images/api-preview.png" alt="GeoSigLIP application preview" width="1000">
</p>

---

## 🔌 API

The backend exposes:

```http
POST /predict
```

The endpoint accepts an image and returns:

- predicted lithology
- confidence
- top-3 predictions
- original filename

### API endpoint

<p align="center">
  <img src="docs/images/api-endpoint.png" alt="GeoSigLIP FastAPI endpoint" width="1000">
</p>

### Prediction response

<p align="center">
  <img src="docs/images/api-result.png" alt="GeoSigLIP API prediction response" width="1000">
</p>

### Example response

```json
{
  "filename": "rock.jpg",
  "predicted_lithology": "Granite",
  "confidence": 0.9988,
  "confidence_percent": 99.88,
  "top_k_predictions": [
    {
      "label": "Granite",
      "confidence": 0.9988,
      "confidence_percent": 99.88
    }
  ]
}
```

---

## 📓 Experiment Notebooks

| Notebook | Purpose |
|:--|:--|
| `00_prepare_kaggle.ipynb` | Dataset preparation |
| `01_eda.ipynb` | Exploratory data analysis |
| `02_baseline.ipynb` | Zero-shot baseline |
| `03_finetuning.ipynb` | LoRA fine-tuning |
| `04_final_evaluation.ipynb` | Final held-out evaluation |
| `05_robustness_analysis.ipynb` | Duplicate / leakage analysis |
| `06_deployment.ipynb` | Inference and deployment workflow |

Experiments were executed on Kaggle; notebook copies are preserved in this repository.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────┐
│                    GeoSigLIP                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  DATA                                               │
│   └── DCID-7                                        │
│          │                                          │
│          ▼                                          │
│  EXPERIMENTATION                                    │
│   ├── EDA                                           │
│   ├── Zero-Shot Baseline                            │
│   └── LoRA Fine-Tuning                              │
│          │                                          │
│          ▼                                          │
│  EVALUATION                                         │
│   ├── Accuracy                                      │
│   ├── Macro F1                                      │
│   ├── Per-Class Metrics                             │
│   └── Confusion Matrix                              │
│          │                                          │
│          ▼                                          │
│  ROBUSTNESS                                         │
│   ├── Split Overlap                                 │
│   ├── SHA-256 Duplicate Checks                      │
│   └── Visual Similarity Screening                   │
│          │                                          │
│          ▼                                          │
│  SERVING                                            │
│   └── FastAPI                                       │
│          │                                          │
│          ▼                                          │
│  UI                                                 │
│   └── React + Vite                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```text
GeoSigLIP/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── package-lock.json
│
├── model/
│   └── README.md
│
├── data/
│   └── processed/
│
├── notebooks/
│   ├── 00_prepare_kaggle.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_baseline.ipynb
│   ├── 03_finetuning.ipynb
│   ├── 04_final_evaluation.ipynb
│   ├── 05_robustness_analysis.ipynb
│   └── 06_deployment.ipynb
│
├── docs/
│   └── images/
│       ├── api-preview.png
│       ├── api-endpoint.png
│       └── api-result.png
│
├── .gitignore
└── README.md
```

---

## ⚙️ Local Setup

### Clone

```bash
git clone https://github.com/UtkarshRode/GeoSigLIP-Fine-Tuned-Vision-Model-for-Lithology-Classification.git
cd GeoSigLIP-Fine-Tuned-Vision-Model-for-Lithology-Classification
```

### Backend

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scriptsctivate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Place the trained checkpoint at:

```text
model/best_model.pt
```

Start the API:

```bash
uvicorn backend.main:app --reload
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open a second terminal:

```bash
cd frontend
npm install
npm install lucide-react
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 🔐 Model Weights

The trained checkpoint is intentionally **not committed to Git history** because of its size.

Expected local path:

```text
model/best_model.pt
```

The model weights are maintained separately from the source repository.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|:--|:--|
| **Model** | PyTorch, Hugging Face Transformers, SigLIP, LoRA |
| **Data** | NumPy, Pandas, Pillow |
| **Experimentation** | Kaggle, Jupyter |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | React, Vite, JavaScript, CSS |

---

## 💡 Engineering Decisions

### Parameter-efficient domain adaptation
LoRA was used instead of full-model fine-tuning to adapt selected transformer projections efficiently.

### Meaningful baseline
A true zero-shot SigLIP baseline was evaluated before task-specific adaptation.

### Held-out benchmarking
A dedicated 1,750-image test set was reserved for the final benchmark.

### Data-integrity verification
Split overlap, exact duplicates, label conflicts, and visual similarity were explicitly checked.

### API-first serving
Model inference is isolated behind `/predict`, allowing the frontend to remain independent of model internals.

### Separation of concerns
Kaggle notebooks document experimentation, the backend handles reusable inference, and the frontend handles presentation.

---

## 🎥 Demo

> **Public live deployment:** Not currently hosted.

The complete application has been tested end-to-end locally.

The repository contains screenshots of:

1. The React application
2. The FastAPI `/predict` endpoint
3. The successful prediction response

---

## 🗺️ Roadmap

- [x] Dataset preparation
- [x] Exploratory data analysis
- [x] Zero-shot baseline
- [x] LoRA fine-tuning
- [x] Validation and checkpointing
- [x] Held-out test evaluation
- [x] Per-class analysis
- [x] Confusion-matrix analysis
- [x] Robustness analysis
- [x] FastAPI inference
- [x] React frontend
- [x] GitHub repository
- [x] Project documentation
- [ ] Public deployment

---

## ⚠️ Limitations

GeoSigLIP predicts only the seven lithology classes represented in the project dataset.

Performance on images outside the training distribution may differ from the reported benchmark. The system is intended as an AI-assisted classification tool and not as a replacement for professional geological interpretation.

---

## 👤 Author

**Utkarsh Rode**  
IIT Kharagpur

<p align="center">
  <strong>GeoSigLIP</strong><br>
  <em>Fine-tuned vision intelligence for geological lithology classification.</em>
</p>
