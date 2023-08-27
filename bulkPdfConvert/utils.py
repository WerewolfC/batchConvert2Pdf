"""Utils class containing constants and methods"""
from dataclasses import dataclass, field
from os import walk
from pathlib import Path
from typing import List


WINDOW_SIZE = "800x500"
WINDOW_TITLE = "Pdf batch convertion tool"

LBL_SOURCE_FOLDER = "Source folder:"
LBL_TARGET_FOLDER = "Target folder:"

GUI_STYLE = "warning"
GUI_HEADERS = "secondary"
GUI_THEME = "flatly"
GUI_CHECK = "-round-toggle"


@dataclass
class FolderContainer:
    """Contains a folder path and
    the file list contained in it
    """
    folder_source_path: Path = ""
    folder_target_path: Path = ""
    file_list: List[str] = field(default_factory=None)


def create_file_struct(source_folder, target_folder=None):
    """Recursively reads all the files in source folder
    and creates a list to be displayed on GUI and parsed
    """
    raw_generator = []
    raw_generator = walk(Path(source_folder))
    file_list_data = []
    for (current, _, files) in raw_generator:
        #search for .doc and .docx extensions
        doc_list = []
        doc_list = [doc_file for doc_file in files if doc_file.endswith((".docx", ".DOCX", ".doc", ".DOC"))]
        if doc_list :
            #add path + file list to the raw list
            file_list_data.append(FolderContainer(current, target_folder, doc_list))
            print(file_list_data)
    return file_list_data