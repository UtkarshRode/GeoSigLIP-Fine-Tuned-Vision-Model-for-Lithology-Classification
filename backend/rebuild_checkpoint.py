from pathlib import Path
import zipfile

source = Path(
    r"C:\Documents\GeoSigLIP\model\best_model\best_model"
)

output = Path(
    r"C:\Documents\GeoSigLIP\model\best_model.pt"
)

if not source.exists():
    raise FileNotFoundError(f"Source not found: {source}")

if output.exists():
    output.unlink()

with zipfile.ZipFile(
    output,
    "w",
    compression=zipfile.ZIP_STORED
) as zf:

    for file_path in source.rglob("*"):
        if file_path.is_file():

            relative = file_path.relative_to(source)

            # PyTorch checkpoint expects one root directory
            archive_path = (
                Path("best_model") / relative
            )

            zf.write(
                file_path,
                arcname=str(archive_path)
            )

print("Created:")
print(output)

print(
    "Size:",
    round(
        output.stat().st_size / (1024 ** 2),
        2
    ),
    "MB"
)