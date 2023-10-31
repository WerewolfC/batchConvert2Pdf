"""Utils class containing constants and methods"""
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
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
STATUS_OK = 'WHITE HEAVY CHECK MARK'
STATUS_FAILED = 'CROSS MARK'
STATUS_ADDED = 'WHITE SQUARE BUTTON'
STATUS_UNKNOWN = 'BLACK QUESTION MARK ORNAMENT'


class FileStatus(Enum):
    """Class stores the status of a file element"""
    OK = STATUS_OK
    FAILED = STATUS_FAILED
    ADDED = STATUS_ADDED
    UNKNOWN = STATUS_UNKNOWN


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
class ConvertFileFormat:
    """Contains the conversion input and put full path
    including the filename
    """
    file_number: int = 0
    conversion_status: FileStatus = FileStatus.UNKNOWN
    input_full_path: Path = ""
    output_full_path: Path = ""


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
