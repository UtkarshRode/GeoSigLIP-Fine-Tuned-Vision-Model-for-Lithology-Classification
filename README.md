<div align="center">

# GeoSigLIP

### Fine-Tuned Vision Model for Lithology Classification

<p>
  <strong>Domain-adapted geological image classification with SigLIP + LoRA</strong>
</p>

<p>
  <a href="https://github.com/UtkarshRode/GeoSigLIP-Fine-Tuned-Vision-Model-for-Lithology-Classification">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?logo=github" alt="GitHub">
  </a>
  <img src="https://img.shields.io/badge/Model-SigLIP-5C6BC0" alt="SigLIP">
  <img src="https://img.shields.io/badge/Fine--Tuning-LoRA-7E57C2" alt="LoRA">
  <img src="https://img.shields.io/badge/Task-7--Class%20Classification-2E7D32" alt="Task">
  <img src="https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Frontend-React-61DAFB?logo=react&logoColor=black" alt="React">
</p>

<p>
  <img src="https://img.shields.io/badge/Test%20Accuracy-99.886%25-success" alt="Test Accuracy">
  <img src="https://img.shields.io/badge/Macro%20F1-99.886%25-success" alt="Macro F1">
  <img src="https://img.shields.io/badge/Test%20Images-1%2C750-2563EB" alt="Test Images">
  <img src="https://img.shields.io/badge/Zero--Shot%20Accuracy-55.257%25-orange" alt="Zero Shot Accuracy">
</p>

</div>

---

## 🧠 Overview

**GeoSigLIP** is an end-to-end geological image classification system that adapts Google's pretrained **SigLIP** vision-language model to domain-specific lithology recognition using **parameter-efficient LoRA fine-tuning**.

The project combines model adaptation, held-out evaluation, robustness analysis, and a usable inference application built with **FastAPI** and **React**.

> **Core idea:** start from a strong pretrained vision-language model, adapt selected parameters to geological imagery, rigorously evaluate the result, and expose the trained model through an interactive application.

---

## ✨ Highlights

- 🧠 Fine-tuned `google/siglip-base-patch16-224`
- ⚡ Parameter-efficient **LoRA** fine-tuning
- 🪨 7-class geological lithology classification
- 📊 Dedicated train, validation, and held-out test sets
- 🧪 Zero-shot SigLIP baseline
- 📈 Accuracy, precision, recall, Macro F1, and confusion-matrix analysis
- 🔎 SHA-256 duplicate and visual-similarity checks across splits
- 🚀 FastAPI inference API
- 🎨 React + Vite frontend
- 📌 Top-3 predictions with confidence scores

---

## 🧭 End-to-End Pipeline

```text
                    DCID-7 Geological Images
                              │
                              ▼
                    Exploratory Data Analysis
                              │
                              ▼
                       Zero-Shot SigLIP
                              │
                        Baseline Study
                              │
                              ▼
                  LoRA Fine-Tuning of SigLIP
                              │
                              ▼
                    Validation / Checkpoint
                              │
                              ▼
                   Held-Out Test Evaluation
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Zero-Shot SigLIP          SigLIP + LoRA
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    Robustness Analysis
                              │
                              ▼
                      Trained Checkpoint
                              │
                              ▼
                      FastAPI Backend
                              │
                              ▼
                       React Frontend
                              │
                              ▼
                Lithology + Confidence + Top-3
```

---

## 📈 Final Results

The final model was evaluated on a **held-out test set of 1,750 images**.

| Model | Accuracy | Macro F1 |
|:--|--:|--:|
| SigLIP Zero-Shot | 55.257% | 47.762% |
| **SigLIP + LoRA** | **99.886%** | **99.886%** |

### Improvement

| Metric | Gain |
|:--|--:|
| Accuracy | **+44.629 percentage points** |
| Macro F1 | **+52.124 percentage points** |

The zero-shot baseline measures pretrained SigLIP performance before task-specific adaptation. The fine-tuned model uses the learned classification head together with LoRA-adapted transformer projections.

> **Evaluation note:** the unusually strong fine-tuned result was followed by explicit data-integrity and similarity checks rather than being reported in isolation.

---

## 🧪 Robustness & Data Integrity

The project includes dedicated checks for possible split leakage and duplicate imagery.

### Split overlap

```text
Train ∩ Validation = 0
Train ∩ Test       = 0
Validation ∩ Test  = 0
```

### Exact duplicate detection

SHA-256 hashing found:

```text
Cross-split exact duplicates = 0
Conflicting duplicate labels = 0
```

### Visual similarity screening

A strict visual-fingerprint screen reported:

```text
Train → Validation = 0
Train → Test       = 4
Validation → Test  = 0
```

The four high-similarity train/test pairs were inspected as part of the robustness workflow.

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

## 🧠 Model Configuration

### Base model

```text
google/siglip-base-patch16-224
```

### LoRA configuration

```text
Rank:            16
Alpha:           32
Dropout:         0.05
Target modules:  q_proj, v_proj
```

LoRA adapters provide task-specific updates to selected transformer projections while keeping the pretrained backbone largely frozen.

---

## 📦 Dataset

| Split | Images |
|:--|--:|
| Train | 2,450 |
| Validation | 1,050 |
| Test | 1,750 |
| **Total** | **5,250** |

The test set was reserved for final evaluation and was not used for training or model selection.

---

## 🖥️ Application

GeoSigLIP is exposed through a full-stack inference application.

### User flow

```text
Upload geological image
          ↓
Image preview
          ↓
Analyze lithology
          ↓
FastAPI /predict
          ↓
GeoSigLIP + LoRA
          ↓
Prediction
          ↓
Confidence + Top-3 alternatives
```

### Application preview

<p align="center">
  <img src="docs/images/app-preview.png" alt="GeoSigLIP application preview" width="1000">
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
  <img src="docs/images/api-result.png" alt="GeoSigLIP FastAPI prediction response" width="1000">
</p>

Example response:

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

## 🗂️ Repository Structure

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
│       ├── app-preview.png
│       ├── api-endpoint.png
│       └── api-result.png
│
├── .gitignore
└── README.md
```

---

## 🧪 Experiment Workflow

| Notebook | Purpose |
|:--|:--|
| `00_prepare_kaggle.ipynb` | Dataset preparation |
| `01_eda.ipynb` | Exploratory data analysis |
| `02_baseline.ipynb` | Baseline / zero-shot experiments |
| `03_finetuning.ipynb` | LoRA fine-tuning |
| `04_final_evaluation.ipynb` | Final held-out evaluation |
| `05_robustness_analysis.ipynb` | Duplicate and leakage analysis |
| `06_deployment.ipynb` | Model inference and deployment workflow |

The experiments were executed on Kaggle, while notebook copies are preserved in this repository for inspection and reproducibility.

---

## ⚙️ Local Setup

### 1. Clone

```bash
git clone https://github.com/UtkarshRode/GeoSigLIP-Fine-Tuned-Vision-Model-for-Lithology-Classification.git
cd GeoSigLIP-Fine-Tuned-Vision-Model-for-Lithology-Classification
```

### 2. Backend

Create a virtual environment:

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

Start FastAPI:

```bash
uvicorn backend.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend

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

Model weights are maintained separately from the source repository.

---

## 🛠️ Tech Stack

### Machine Learning

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?logo=pytorch&logoColor=white)
![Transformers](https://img.shields.io/badge/Hugging%20Face-Transformers-FFD21E)
![SigLIP](https://img.shields.io/badge/SigLIP-Vision--Language-5C6BC0)
![LoRA](https://img.shields.io/badge/PEFT-LoRA-7E57C2)

### Backend

![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-121212)

### Frontend

![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=white)

### Experimentation

![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?logo=kaggle&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)

---

## 💡 Engineering Decisions

### Parameter-efficient adaptation
LoRA was selected to adapt a pretrained vision-language model without updating the full backbone.

### Meaningful baseline
The project compares the domain-adapted model against a genuine zero-shot SigLIP baseline.

### Held-out evaluation
A separate 1,750-image test set was reserved for final evaluation.

### Robustness analysis
The dataset was checked for split overlap, exact duplicates, conflicting labels, and high visual similarity.

### API-first inference
Model inference is isolated behind FastAPI so the frontend remains independent of model implementation details.

### Full-stack delivery
A React client consumes the prediction API and presents results in an interactive interface.

---

## 🚧 Deployment Status

> **Public live deployment is not currently hosted.**

The application has been tested end-to-end locally:

```text
React frontend
      ↓
FastAPI backend
      ↓
GeoSigLIP + LoRA
      ↓
Prediction
```

Screenshots of the working frontend and API flow are included above.

---

## 🗺️ Roadmap

- [x] Dataset preparation
- [x] Exploratory data analysis
- [x] Zero-shot baseline
- [x] LoRA fine-tuning
- [x] Validation and checkpointing
- [x] Held-out test evaluation
- [x] Robustness analysis
- [x] FastAPI inference
- [x] React frontend
- [x] GitHub repository
- [x] README and visual documentation
- [ ] Public deployment

---

## ⚠️ Limitations

GeoSigLIP predicts only the seven lithology classes represented in the project dataset.

Performance on images outside the training distribution may differ from the reported benchmark. The model should therefore be treated as an AI-assisted classification system rather than a replacement for professional geological interpretation.

---

## 👤 Author

**Utkarsh Rode**  
IIT Kharagpur

---

<div align="center">

**GeoSigLIP**  
*Fine-tuned vision intelligence for geological lithology classification.*

</div>
