""" GUI class"""
import tkinter as tk
from typing import Protocol
from pathlib import Path
from tkinter.filedialog import askdirectory
from ttkbootstrap import utility
from ttkbootstrap.tooltip import ToolTip
import ttkbootstrap as ttk

from bulkPdfConvert import utils


class Presenter(Protocol):
    """Protocol implementation for Presenter class"""
    def handle_set_convert_data(self):
        ...

    def handle_return_file_list(self):
        ...

class MainWindow(ttk.Window):
    """Main GUI class"""
    def __init__(self, theme_name):
        super().__init__(theme_name)
        self.title(utils.WINDOW_TITLE)
        self.geometry(utils.WINDOW_SIZE)
        self.resizable(True, True)

        self.source_path = tk.StringVar(master=self, value="Please select source folder")
        self.target_path = tk.StringVar(master=self, value="Please select save folder")
        self.actual_progress = tk.IntVar(master=self, value=0)
        self.opt_same_location = tk.IntVar(master=self, value=0)
        self.opt_bookmark = tk.IntVar(master=self, value=1)
        self.file_count = 0

        self.file_list_data = None
        self.presenter = None

    def create_gui(self, presenter):
        """Create GUI for main window"""
        self.presenter = presenter
        frm_main = ttk.Frame(master=self)
        frm_source_select = ttk.Frame(master=frm_main)
        frm_target_select = ttk.Frame(master=frm_main)
        frm_progress = ttk.Frame(master=frm_main)
        frm_listing = ttk.Frame(master=frm_main)
        frm_convert = ttk.Frame(master=frm_main)
        frm_options = ttk.Frame(master=frm_convert)

        #source elements
        tk.Label(master=frm_source_select, text=utils.LBL_SOURCE_FOLDER).pack(side=tk.LEFT,
                                                                            expand=False,
                                                                            fill=tk.X,
                                                                            padx=5,
                                                                            anchor=tk.W)
        self.ent_source = ttk.Entry(master=frm_source_select,
                                  textvariable=self.source_path,
                                  state=tk.DISABLED,
                                  justify=tk.LEFT,
                                  bootstyle="readonly")
        self.ent_source.pack(side=tk.LEFT,
                            fill=tk.X,
                            padx=5,
                            expand=True)

        self.btn_select_source = ttk.Button(master=frm_source_select,
                                        text="Browse",
                                        width=10,
                                        command=self._source_select,
                                        bootstyle=utils.GUI_STYLE)
        ToolTip(self.btn_select_source, text="Select starting folder - recursive conversion")
        self.btn_select_source.pack(side=tk.LEFT)
        self.bind('<Control-1>', lambda event:self._source_select())
        frm_source_select.pack(side=tk.TOP, fill=tk.X, pady=5)

        #target elements
        tk.Label(master=frm_target_select, text=utils.LBL_TARGET_FOLDER).pack(side=tk.LEFT,
                                                                            expand=False,
                                                                            fill=tk.X,
                                                                            padx=5,
                                                                            anchor=tk.W)
        self.ent_arget = ttk.Entry(master=frm_target_select,
                                  textvariable=self.target_path,
                                  state=tk.DISABLED,
                                  justify=tk.LEFT,
                                  bootstyle="readonly")
        self.ent_arget.pack(side=tk.LEFT,
                            fill=tk.X,
                            padx=5,
                            expand=True)

        self.btn_select_target = ttk.Button(master=frm_target_select,
                                        text="Browse",
                                        width=10,
                                        command=self._target_select,
                                        state=tk.NORMAL,
                                        bootstyle=utils.GUI_STYLE)
        ToolTip(self.btn_select_target, text="Select storage folder")
        self.btn_select_target.pack(side=tk.LEFT)
        self.bind('<Control-2>', lambda event:self._target_select())
        frm_target_select.pack(side=tk.TOP, fill=tk.X, pady=5)

        #options, convert and progress bar
        self.btn_convert = ttk.Button(master=frm_convert,
                                command=self._callback_convert,
                                text="Convert",
                                bootstyle=utils.GUI_STYLE,
                                width=10
                                )
        ToolTip(self.btn_convert, text="Convert to PDF format")
        self.btn_convert.pack(side=tk.RIGHT, padx=110)
        self.bind('<space>', lambda event:self._callback_convert())

        ttk.Checkbutton(master=frm_options,
                        variable=self.opt_same_location,
                        command=self._toggle_target_button,
                        text="Same location",
                        onvalue=1,
                        offvalue=0,
                        bootstyle=utils.GUI_STYLE+utils.GUI_CHECK
                        ).pack(side=tk.TOP, expand=True, fill=tk.X)
        ttk.Checkbutton(master=frm_options,
                variable=self.opt_bookmark,
                text="Create bookmarks",
                onvalue=1,
                offvalue=0,
                bootstyle=utils.GUI_STYLE+utils.GUI_CHECK
                ).pack(side=tk.TOP, expand=True, fill=tk.X)
        frm_options.pack(side=tk.RIGHT, fill=tk.X, pady=5)

        frm_convert.pack(side=tk.TOP, fill=tk.X)

        #progress bar
        self.prgress_bar = ttk.Progressbar(master=frm_progress,
                                           variable=self.actual_progress,
                                           value=5,
                                           bootstyle="success-stripped")
        self.prgress_bar.pack(side=tk.TOP, fill=tk.X, pady=5, padx=30)
        frm_progress.pack(side=tk.TOP, fill=tk.X)
        #TODO: progress bar needs to show actual conversion steps
        #self.prgress_bar.start(100)

        #list_view
        self.list_view = ttk.Treeview(
                                    master=frm_listing,
                                    bootstyle=utils.GUI_HEADERS,
                                    columns=[0, 1, 2],
                                    show="headings"
        )
        self.list_view.heading(0, text='No.', anchor=tk.W)
        self.list_view.heading(1, text='Filename', anchor=tk.W)
        self.list_view.heading(2, text='Full path', anchor=tk.W)
        self.list_view.column(
            column=0,
            anchor=tk.W,
            width=utility.scale_size(self, 40),
            stretch=False
        )
        self.list_view.column(
            column=1,
            anchor=tk.W,
            width=utility.scale_size(self, 150),
            stretch=True
        )
        self.list_view.column(
            column=1,
            anchor=tk.W,
            width=utility.scale_size(self, 350),
            stretch=True
        )
        self.list_view.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        scroll_bar = ttk.Scrollbar(master=self.list_view,
                                   orient=tk.VERTICAL,
                                   command=self.list_view.yview)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_view.configure(yscrollcommand=scroll_bar.set)

        self.btn_exit = ttk.Button(master=frm_listing,
                                        text="Exit",
                                        command=self._close,
                                        width=10,
                                        state=tk.NORMAL,
                                        bootstyle=utils.GUI_STYLE)
        ToolTip(self.btn_exit, text="Exit")
        self.btn_exit.pack(side=tk.TOP, pady=5)
        self.bind('<Control-q>', lambda event:self._close())

        frm_listing.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        #pack main frame
        frm_main.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def ask_file_list(self):
        """Ask presenter for file list
        based on the selected Source path
        """
        if Path(self.source_path.get()).is_dir():
            self.presenter.handle_return_file_list(Path(self.source_path.get()))

    def _source_select(self):
        """Create source select button and selection dialog
        """
        source_path = askdirectory(title="Browse for top source folder")
        if source_path:
            self.source_path.set(source_path)
            self.ask_file_list()

    def _target_select(self):
        """Create target select button and selection dialog
        """
        target_path = askdirectory(title="Browse for save folder")
        if target_path:
            self.target_path.set(target_path)

    def _callback_convert(self):
        """Gather all the data used for conversion and
        call presenter handle
        """
        target = 'not valid path'
        #if target selected and same location option not set or
        #target empty but same location option detected call presenter
        if Path(self.source_path.get()).is_dir():
            if self.opt_same_location.get() == 1:
                target = self.source_path.get()
            elif Path(self.target_path.get()).is_dir():
                target = self.target_path.get()

        if Path(self.source_path.get()).is_dir() and Path(target).is_dir():
            settings = utils.ConvertOptions(Path(self.source_path.get()),
                                            Path(target),
                                            self.opt_same_location.get(),
                                            self.opt_bookmark.get()
                                            )
            self.presenter.handle_set_convert_data(settings)

    def _toggle_target_button(self):
        """Toggle target browse button state
        and try to send the convert options
        """
        if str(self.btn_select_target['state']) == tk.NORMAL:
            self.btn_select_target.config(state=tk.DISABLED)
        elif str(self.btn_select_target['state']) == tk.DISABLED:
            self.btn_select_target.config(state=tk.NORMAL)

    def _close(self):
        """Terminate the GUI"""
        self.destroy()

    def update_list_view(self, list_data):
        """Update tree view with info from parameter list_data
        """
        #clear the treeview
        self.list_view.delete(*self.list_view.get_children())

        # #populate the list
        self.file_count = 0
        for folder_element in list_data:
            for each_file in folder_element.file_list:
                self.file_count += 1
                f_name = each_file
                path = folder_element.folder_source_path
                iid = self.list_view.insert(parent='',
                                            index=tk.END,
                                            values=(self.file_count, f_name, path)
                )
        #if no suitable files are found... let the user know
        if not self.file_count:
            iid = self.list_view.insert(parent='',
                                            index=tk.END,
                                            values=(self.file_count, 'No documents found', '')
                )
