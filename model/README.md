# Model Weights

The trained GeoSigLIP LoRA checkpoint is intentionally not stored in Git history because of its size.

The model was fine-tuned from:

- Base model: `google/siglip-base-patch16-224`
- Method: LoRA
- Rank: 16
- Alpha: 32
- Dropout: 0.05
- Target modules: `q_proj`, `v_proj`

Final test performance:

- Accuracy: 99.886%
- Macro F1: 99.886%

The checkpoint should be downloaded separately and placed at:

`model/best_model.pt`