"""Utils class containing constants and methods"""
from dataclasses import dataclass, field
from os import walk
from pathlib import Path
from typing import List
import concurrent.futures
from threading import Timer
from win32com import client as win32Client
import pythoncom


WINDOW_SIZE = "800x500"
WINDOW_TITLE = "Pdf batch conversion tool"

LBL_SOURCE_FOLDER = "Source folder:"
LBL_TARGET_FOLDER = "Target folder:"

GUI_STYLE = "warning"
GUI_HEADERS = "secondary"
GUI_THEME = "flatly"
GUI_CHECK = "-round-toggle"

#emoji
GREEN_CHECKMARK = 'WHITE HEAVY CHECK MARK'
RED_CROSS_MARK = 'CROSS MARK'
# PLUS_SIGN = 'LARGE PURPLE CIRCLE'
PLUS_SIGN = 'WHITE SQUARE BUTTON'


@dataclass
class FolderContainer:
    """Contains a folder path and
    the file list contained in it
    """
    folder_source_path: Path = ""
    file_list: List[str] = field(default_factory=None)


@dataclass
class ConvertOptions:
    """Contains the conversion options
    """
    folder_source_path: Path = ""
    folder_target_path: Path = ""
    use_same_folder : bool = False
    create_bookmarks: bool = True


@dataclass
class ConvertFile:
    """Contains the conversion input and put full path
    including the filename
    """
    input_full_path: Path = ""
    output_full_path: Path = ""


def recursive_check_names(output_full_path, object_pool, iterations):
    """Check recursive if the output name exists in a pool
    and returns the unique name
    """
    #check if pdf already exists and if so add -Copy to the end of name
    if output_full_path not in [obj.output_full_path for obj in object_pool]:
        return output_full_path
    else:
        new_full_path = output_full_path.with_stem(output_full_path.stem + f'({iterations})')
        return recursive_check_names(new_full_path, object_pool, iterations + 1)

def create_raw_data(source_folder):
    """Recursively reads all the files in source folder
    and creates a list to be displayed on GUI and parsed
    """
    raw_generator = []
    raw_generator = walk(Path(source_folder))
    file_list_data = []
    for (current, _, files) in raw_generator:
        #search for .doc and .docx extensions
        doc_list = []
        doc_list = [doc_file for doc_file in files\
                    if doc_file.endswith((".docx", ".DOCX", ".doc", ".DOC"))]
        if doc_list :
            #add path + file list to the raw list
            file_list_data.append(FolderContainer(current, doc_list))
    return file_list_data

def convert_to_pdf(*args):
    """Converts one doc file into pdf format
    """
    word = win32Client.Dispatch("Word.Application", pythoncom.CoInitialize())
    wd_export_format_pdf = 17
    print(args)
    print(type(args))
    bookmark_opt, file_info, = args[0]
    doc = word.Documents.Open(str(file_info.input_full_path))
    doc.ExportAsFixedFormat (OutputFileName=str(file_info.output_full_path),
                             ExportFormat=wd_export_format_pdf,
                             CreateBookmarks=bookmark_opt)
    doc.Close(0)

def main(*args):
    """Function used to start PDF conversion threads
    using the ThreadPoolExecutor
    """
    map_bookmark = {0: False, 1: True}
    conn, funct, file_list, opt_bookmark = args
    bookmark_state = map_bookmark.get(opt_bookmark)
    processed = 1
    with concurrent.futures.ThreadPoolExecutor(4) as executor:
        for active_task in executor.map(funct, [(bookmark_state, files) for files in file_list]):
            conn.send((processed, len(file_list)))
            print(f'type {type(active_task)}')
            print(f'type {active_task}')
            print(f'Files processed {processed}/{len(file_list)}')
            processed+=1
    return

def disable_event():
    """Empty function used to disable windows close x button"""
    pass


class RepeatTimer(Timer):
    """threading Timer subclass
    """
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
