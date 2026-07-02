from pathlib import Path


class ExcelManager:
    def __init__(self, output_dir: str | Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_placeholder(self):
        return self.output_dir / "heroes.xlsx"
