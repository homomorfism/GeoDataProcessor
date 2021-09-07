from pathlib import Path


def filter_files(folder: Path, supported_formats: list[str]) -> list[Path]:
    """
    Traverse through the directory and collects for image files with supported formats

    :param folder: path to source folder
    :param supported_formats: extensions to look for

    :return: list of found files matching extensions
    """
    assert folder.is_dir(), f"{str(folder)} not a folder"
    files = list(path for path in folder.rglob("**/*") if path.is_file() and path.suffix in supported_formats)
    assert len(files) != 0, "Found 0 files in folder!"
    return files
