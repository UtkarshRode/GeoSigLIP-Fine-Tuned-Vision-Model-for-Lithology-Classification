# GeoSigLIP

AI-powered lithology classification from geological rock images.

GeoSigLIP fine-tunes Google's SigLIP vision-language model using parameter-efficient LoRA adaptation for 7-class geological image classification.

## Highlights

- SigLIP-based geological image classification
- LoRA fine-tuning
- 7 lithology classes
- 2,450 training images
- 1,050 validation images
- 1,750 held-out test images
- Zero-shot baseline evaluation
- Robustness and split-integrity analysis
- FastAPI inference backend
- React frontend
- Top-3 predictions and confidence scores

## Lithology Classes

1. Red sandstone
2. Light sandstone
3. Gray siltstone
4. Mudstone
5. Granite
6. Basalt
7. Marble

## Results

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| SigLIP Zero-Shot | 55.257% | 47.762% |
| SigLIP + LoRA | 99.886% | 99.886% |

Improvement:

- Accuracy: +44.629 percentage points
- Macro F1: +52.124 percentage points

## Architecture

```text
React Frontend
      |
      v
FastAPI Backend
      |
      v
GeoSigLIP Inference
      |
      v
SigLIP + LoRA
      |
      v
Lithology + Confidence + Top-3