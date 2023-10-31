"""Presenter class"""
from multiprocessing import Process, Pipe
from bulkPdfConvert.utils import convert_to_pdf, main, disable_event,\
        RepeatTimer

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
    def __init__(self, view, data) -> None:
        self.view = view
        self.data = data
        self.worker_process = None
        self.child_conn, self.parent_conn = Pipe()

    def run(self):
        """Create GUI and start mainloop
        """
        self.view.create_gui(self)
        # disable x close main window button
        self.view.protocol("WM_DELETE_WINDOW", disable_event)
        self.view.mainloop()

    def handle_start_convert(self, options_obj):
        """Creates the list and start conversion
        """
        self.data.set_options(options_obj)
        self.data.create_explicit_list()
        self.convert_files()

    def handle_return_file_list(self, path):
        """Returns a file list obj based on the path
        """
        self.data.create_raw_data(path)
        self.data.create_initial_list()
        self.view.update_list_view(self.data.get_explicit_list())

    def handle_update_file_list(self):
        """Update the initial list with target data
        """
        self.data.set_options(self.view.get_options())
        print(f'options in presenter {self.data.options}')
        self.data.create_explicit_list()
        self.view.update_list_view(self.data.get_explicit_list())

    def handle_close_app (self):
        """Terminate the app"""
        if self.worker_process is not None:
            self.worker_process.terminate()
        self.view.destroy()

    def convert_files(self):
        """Creates a process to execute pdf conversion
        """
        self.worker_process = Process(target=main,
                                      args =(self.child_conn,
                                             convert_to_pdf,
                                             self.data.get_explicit_list(),
                                             self.view.get_options()))
        self.worker_process.start()

        # create timer thread
        self.timer_thread = RepeatTimer(1, read_from_thread, [self])
        self.timer_thread.start() #recalling run
