import shutil
from pathlib import Path


def filter_files(folder: Path, supported_formats: tuple[str]) -> list[Path]:
    """
    Traverse through the directory and collects for image files with supported formats

    :param folder: path to source folder
    :param supported_formats: extensions to look for

    :return: list of found files matching extensions
    """
    assert folder.is_dir(), f"{str(folder)} not a folder"

    files = []
    for path in folder.rglob("**/*"):
        if path.is_file() and path.suffix in supported_formats:
            files.append(path)

    assert len(files) != 0, "Found 0 files in folder!"
    return files


def get_parents_folder(folder: Path, supported_formats: tuple[str]) -> list[Path]:
    assert folder.is_dir()

    parents = []
    for path in folder.rglob("**/*"):
        if path.is_file() and path.suffix in supported_formats:
            parents.append(path.parents[0])

    assert len(parents) != 0
    return parents


def create_empty_folder(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path=path)

    path.mkdir()
