"""Utils class containing constants and methods"""
from dataclasses import dataclass, field
from os import walk
from pathlib import Path
from typing import List
from win32com import client as win32Client


WINDOW_SIZE = "800x500"
WINDOW_TITLE = "Pdf batch conversion tool"

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


@dataclass
class ConvertOptions:
    """Contains the conversion options
    """
    folder_source_path: Path = ""
    folder_target_path: Path = ""
    create_bookmarks: bool = True


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


def resolve_paths(input_path, output_path):
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve() if output_path else None
    output = {}
    if input_path.is_dir():
        output["batch"] = True
        output["input"] = str(input_path)
        if output_path:
            assert output_path.is_dir()
        else:
            output_path = str(input_path)
        output["output"] = output_path
    else:
        output["batch"] = False
        assert str(input_path).endswith((".docx", ".DOCX", ".doc", ".DOC"))
        output["input"] = str(input_path)
        if output_path and output_path.is_dir():
            output_path = str(output_path / (str(input_path.stem) + ".pdf"))
        elif output_path:
            assert str(output_path).endswith(".pdf")
        else:
            output_path = str(input_path.parent / (str(input_path.stem) + ".pdf"))
        output["output"] = output_path
    return output


def convert_to_pdf(input_path, output_path=None):
    """Converts one doc file into pdf format
    """
    word = win32Client.Dispatch("Word.Application")
    wdExportFormatPDF = 17
    wdExportCreateHeadingBookmarks = 1

    paths = resolve_paths(input_path, output_path)
    pbar = tqdm(total=1)
    docx_filepath = Path(paths["input"]).resolve()
    pdf_filepath = Path(paths["output"]).resolve()
    print(docx_filepath)
    print(pdf_filepath)
    doc = word.Documents.Open(str(docx_filepath))
    doc.ExportAsFixedFormat (OutputFileName=str(pdf_filepath),
                             ExportFormat=wdExportFormatPDF,
                             CreateBookmarks=wdExportCreateHeadingBookmarks)
    doc.Close(0)
    pbar.update(1)
