"""Presenter class"""
from bulkPdfConvert.utils import create_file_struct, ConvertOptions


class Presenter():
    """Presenter class
    """
    def __init__(self, view) -> None:
        self.view = view
        self.convert_options = ConvertOptions()
        self.view_file_list = None

    def run(self):
        """Create GUI and start mainloop
        """
        self.view.create_gui(self)
        self.view.mainloop()

    def handle_set_convert_options(self, options_obj):
        """Retrieves and stores the conversion options
        """
        self.convert_options = options_obj
        self.view_file_list = create_file_struct(self.convert_options.folder_source_path,
                                                 self.convert_options.folder_target_path)

    def handle_return_file_list(self, path):
        """Returns a file list obj based on the path
        """
        self.view_file_list = create_file_struct(path)
        self.view.update_list_view(self.view_file_list)
