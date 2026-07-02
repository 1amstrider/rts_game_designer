from pathlib import Path


class ImageManager:
    def __init__(self, image_dir: str | Path):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(parents=True, exist_ok=True)
