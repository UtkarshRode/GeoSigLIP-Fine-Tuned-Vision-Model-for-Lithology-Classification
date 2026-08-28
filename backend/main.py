from pathlib import Path
from typing import List

import numpy as np
import torch
import torch.nn as nn

from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoImageProcessor, SiglipForImageClassification


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "model"
    / "best_model.pt"
)

MODEL_NAME = "google/siglip-base-patch16-224"

CLASS_NAMES = [
    "Red sandstone",
    "Light sandstone",
    "Gray siltstone",
    "Mudstone",
    "Granite",
    "Basalt",
    "Marble",
]

NUM_CLASSES = len(CLASS_NAMES)

LABEL2ID = {
    name: i
    for i, name in enumerate(CLASS_NAMES)
}

ID2LABEL = {
    i: name
    for i, name in enumerate(CLASS_NAMES)
}

LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05


# ============================================================
# Device
# ============================================================

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print("Device:", DEVICE)

if DEVICE.type == "cuda":
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ============================================================
# LoRA layer
# ============================================================

class LoRALinear(nn.Module):

    def __init__(
        self,
        base_layer: nn.Linear,
        rank: int = 16,
        alpha: int = 32,
        dropout: float = 0.05,
    ):
        super().__init__()

        if not isinstance(
            base_layer,
            nn.Linear
        ):
            raise TypeError(
                "LoRALinear requires an nn.Linear layer."
            )

        self.base_layer = base_layer

        self.rank = rank
        self.alpha = alpha
        self.scaling = alpha / rank

        # Freeze original pretrained layer
        for parameter in (
            self.base_layer.parameters()
        ):
            parameter.requires_grad = False

        layer_device = (
            base_layer.weight.device
        )

        layer_dtype = (
            base_layer.weight.dtype
        )

        self.lora_A = nn.Linear(
            base_layer.in_features,
            rank,
            bias=False,
            device=layer_device,
            dtype=layer_dtype,
        )

        self.lora_B = nn.Linear(
            rank,
            base_layer.out_features,
            bias=False,
            device=layer_device,
            dtype=layer_dtype,
        )

        self.dropout = nn.Dropout(
            dropout
        )

        # Same initialization used during training
        nn.init.kaiming_uniform_(
            self.lora_A.weight,
            a=np.sqrt(5),
        )

        nn.init.zeros_(
            self.lora_B.weight
        )

    def forward(self, x):
        base_output = self.base_layer(x)

        lora_output = self.lora_B(
            self.lora_A(
                self.dropout(x)
            )
        )

        return (
            base_output
            + self.scaling * lora_output
        )


# ============================================================
# Build exact trained model
# ============================================================

def build_model() -> nn.Module:

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model checkpoint not found:\n{MODEL_PATH}"
        )

    print(
        "Loading base model:",
        MODEL_NAME
    )

    model = (
        SiglipForImageClassification
        .from_pretrained(
            MODEL_NAME,
            num_labels=NUM_CLASSES,
            label2id=LABEL2ID,
            id2label=ID2LABEL,
            ignore_mismatched_sizes=True,
        )
        .to(DEVICE)
    )

    # Freeze everything
    for parameter in model.parameters():
        parameter.requires_grad = False

    # Recreate exactly the LoRA layers
    for layer in (
        model
        .vision_model
        .encoder
        .layers
    ):

        layer.self_attn.q_proj = LoRALinear(
            layer.self_attn.q_proj,
            rank=LORA_R,
            alpha=LORA_ALPHA,
            dropout=LORA_DROPOUT,
        )

        layer.self_attn.v_proj = LoRALinear(
            layer.self_attn.v_proj,
            rank=LORA_R,
            alpha=LORA_ALPHA,
            dropout=LORA_DROPOUT,
        )

    # Classifier was trained
    for parameter in (
        model.classifier.parameters()
    ):
        parameter.requires_grad = True

    print(
        "Loading checkpoint:",
        MODEL_PATH
    )

    checkpoint = torch.load(
        MODEL_PATH,
        map_location=DEVICE,
        weights_only=True,
    )

    result = model.load_state_dict(
        checkpoint,
        strict=True,
    )

    if result.missing_keys:
        raise RuntimeError(
            "Missing checkpoint keys:\n"
            + "\n".join(
                result.missing_keys
            )
        )

    if result.unexpected_keys:
        raise RuntimeError(
            "Unexpected checkpoint keys:\n"
            + "\n".join(
                result.unexpected_keys
            )
        )

    model.eval()

    print(
        "Checkpoint loaded successfully."
    )

    print(
        "Missing keys:",
        len(result.missing_keys)
    )

    print(
        "Unexpected keys:",
        len(result.unexpected_keys)
    )

    return model


# ============================================================
# Load processor + model once
# ============================================================

processor = AutoImageProcessor.from_pretrained(
    MODEL_NAME
)

model = build_model()


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="GeoSigLIP Lithology API",
    description=(
        "Lithology classification using "
        "SigLIP fine-tuned with LoRA on DCID-7."
    ),
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Health endpoint
# ============================================================

@app.get("/")
def root():
    return {
        "project": "GeoSigLIP",
        "status": "running",
        "model": MODEL_NAME,
        "device": str(DEVICE),
        "classes": NUM_CLASSES,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": True,
        "device": str(DEVICE),
    }


# ============================================================
# Prediction helper
# ============================================================

def predict_image(
    image: Image.Image,
    top_k: int = 3,
):
    image = image.convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt",
    )

    pixel_values = (
        inputs["pixel_values"]
        .to(DEVICE)
    )

    with torch.no_grad():

        outputs = model(
            pixel_values=pixel_values
        )

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1,
        )[0]

    top_k = min(
        top_k,
        NUM_CLASSES
    )

    values, indices = torch.topk(
        probabilities,
        k=top_k,
    )

    predictions: List[dict] = []

    for value, index in zip(
        values.cpu().tolist(),
        indices.cpu().tolist(),
    ):

        predictions.append({
            "label": ID2LABEL[index],
            "confidence": round(
                float(value),
                6
            ),
            "confidence_percent": round(
                float(value) * 100,
                2
            ),
        })

    return predictions


# ============================================================
# Prediction endpoint
# ============================================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    if not file.content_type:
        raise HTTPException(
            status_code=400,
            detail="File type could not be determined.",
        )

    if not file.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="Please upload an image file.",
        )

    try:

        contents = await file.read()

        if not contents:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty.",
            )

        from io import BytesIO

        image = Image.open(
            BytesIO(contents)
        ).convert("RGB")

        predictions = predict_image(
            image,
            top_k=3,
        )

        best = predictions[0]

        return {
            "filename": file.filename,
            "predicted_lithology": best["label"],
            "confidence": best[
                "confidence"
            ],
            "confidence_percent": best[
                "confidence_percent"
            ],
            "top_k_predictions": predictions,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {exc}",
        ) from exc