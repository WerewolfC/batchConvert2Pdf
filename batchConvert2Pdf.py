"""Main app class that is launching the app"""
from bulkPdfConvert.gui import MainWindow
from bulkPdfConvert.data import Filelist
from bulkPdfConvert.presenter import Presenter
from bulkPdfConvert.utils import GUI_THEME


if __name__ == "__main__":
    view = MainWindow(GUI_THEME)
    data = Filelist()
    presenter = Presenter(view, data)
    presenter.run()
