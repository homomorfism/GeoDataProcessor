from pathlib import Path

source_folder = Path("tests/dataset")

formats = ('.shp',)
for path in source_folder.rglob("**/*"):
    if path.is_file():
        if path.suffix in formats:
            print(path.parents[0])
