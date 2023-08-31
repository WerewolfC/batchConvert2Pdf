"""Presenter class"""
from multiprocessing import Process, Pipe
from pathlib import Path
# from bulkPdfConvert.paralellProcess import main
from bulkPdfConvert.utils import ConvertOptions, ConvertFile,\
        create_raw_data, recursive_check_names, convert_to_pdf,\
        RepeatTimer, main

def read_from_thread(presenter):
    """Executed by Timer thread
    implements the Pipe rcv method
    """
    if presenter.parent_conn.poll():
        recv_data = presenter.parent_conn.recv()
        presenter.view.update_progressbar(recv_data)


class Presenter():
    """Presenter class
    """
    def __init__(self, view) -> None:
        self.view = view
        self.convert_options = ConvertOptions()
        self.view_file_list = None
        self.explicit_list = []
        self.worker_process = None
        self.child_conn, self.parent_conn = Pipe()

    def run(self):
        """Create GUI and start mainloop
        """
        self.view.create_gui(self)
        self.view.mainloop()

    def handle_set_convert_data(self, options_obj):
        """Retrieves and stores the conversion options
        """
        self.convert_options = options_obj
        self.create_explicit_list()
        self.convert_files()

    def handle_return_file_list(self, path):
        """Returns a file list obj based on the path
        """
        self.view_file_list = create_raw_data(path)
        self.view.update_list_view(self.view_file_list)

    def handle_close_app (self):
        """Terminate the app"""
        if self.worker_process is not None:
            self.worker_process.terminate()
        self.view.destroy()

    def create_explicit_list(self):
        """create explicit file list [ [input0_full_path, output1_full_path], ..... ]
        """
        self.explicit_list = []
        for container in self.view_file_list:
            for file in container.file_list:
                #create output full file path
                if self.convert_options.use_same_folder:
                    output_path = Path(container.folder_source_path)
                else:
                    output_path = Path(self.convert_options.folder_target_path)

                temp_out_full_path = recursive_check_names(output_path.joinpath(file).with_suffix('.pdf'),
                                                           self.explicit_list,
                                                           0
                )

                converted_file = ConvertFile(Path(container.folder_source_path).joinpath(file),
                                             temp_out_full_path)

                #create [input_path, output_path] and add them to self.explicit_list
                self.explicit_list.append(converted_file)
        #TODO: remove print
        from pprint import pprint
        pprint(f'Explicit list --> \n{self.explicit_list}')

    def convert_files(self):
        """Creates a process to execute pdf conversion
        """
        self.worker_process = Process(target=main,
                                      args =(self.child_conn,
                                             convert_to_pdf,
                                             self.explicit_list,
                                             self.convert_options.create_bookmarks))
        self.worker_process.start()

        # create timer thread
        self.timer_thread = RepeatTimer(1, read_from_thread, [self])
        self.timer_thread.start() #recalling run
