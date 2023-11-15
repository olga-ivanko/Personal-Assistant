import re
import shutil
from pathlib import Path


SUBFOLDER_NAME_TO_EXTENSIONS = {
    "archives" : (".zip", ".tar", ".gz"),
    "video" : (".avi", ".mp4", ".ogg", ".wav", ".amr", ".mov",  ".mkv", ".wmv", ".mpg", ".mpeg", ".m4v"),
    "audio" : (".mp3", ".wav", ".ogg", ".flac", ".aif", ".mid", ".midi", ".wma"),
    "documents": (".doc", ".docx", ".txt", ".pdf", ".pptx"),
    "images": (".jpg", ".png", ".bmp", ".jpeg", ".svg", ".tif", ".tiff"),
    "spreadsheets": (".xlsx", ".xls", ".xlsm", ".xml"),
    "presentation": (".pptx", ".ppt"),
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

extentions = {"identified": [], "non_idintified": []}


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in SUBFOLDER_NAME_TO_EXTENSIONS.items():
        if ext in exts:
            extentions.get(
                "identified",
            ).append(ext)
            return cat
    return "Other"


def normalize(file_name: str) -> str:
    normalized_name = re.sub("\W", "_", file_name.translate(TRANS))
    return normalized_name


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    new_name = Path(normalize(file.stem) + file.suffix)
    new_path = target_dir.joinpath(new_name.name)
    print(category, new_path)
    if not target_dir.exists():
        target_dir.mkdir()
    if not new_path.exists():
        file.replace(new_path)
    return None


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
    return None


def archive_unpack(sort_folder: Path) -> None:
    try:
        for element in sort_folder.glob("*archives\*"):
            new_folder_for_archive = element.parent.joinpath(element.stem)
            shutil.unpack_archive(element, new_folder_for_archive)
    except shutil.ReadError:
        return None


def del_empty_folders(sorted_folder_path: Path) -> None:
    for i in sorted_folder_path.iterdir():
        if i.stem in SUBFOLDER_NAME_TO_EXTENSIONS.keys():
            continue
        elif i.stem == "Other" and i.is_dir:
            continue
        else:
            shutil.rmtree(i, ignore_errors=True)
    return None


def record_result(sorted_folder: Path) -> None:
    for i in sorted_folder.joinpath("Other").iterdir():
        extentions.get("non_idintified",).append(i.suffix)
    print(
        " non-idintified extentions: ", set(extentions.get("non_idintified",)), 
          "\n", "idintified extentions: ", set(extentions.get("identified",)),
          )
    return None


def main(imput_path: Path) -> str:
    sort_folder(imput_path)
    archive_unpack(imput_path)
    del_empty_folders(imput_path)
    record_result(imput_path)
    return f"Your folder {imput_path} is sorted"
