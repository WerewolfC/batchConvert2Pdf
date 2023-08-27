"""Presenter class"""
from bulkPdfConvert.utils import create_file_struct


class Presenter():
    """Presenter class
    """
    def __init__(self, view) -> None:
        self.view = view

    def run(self):
        self.view.create_gui(self)
        self.view.mainloop()

    def handle_get_file_list(self):
        """Returns a file list data obj
        """
        return create_file_struct(r"C:\00_User\04_Projects\Python\PDFconverter\testFolder")
