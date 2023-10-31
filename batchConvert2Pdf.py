"""Main app class that is launching the app"""
from bulkPdfConvert.gui import MainWindow
from bulkPdfConvert.data import Filelist
from bulkPdfConvert.presenter import Presenter
import bulkPdfConvert.utils as utils


if __name__ == "__main__":
    view = MainWindow(utils.GUI_THEME)
    data = Filelist()
    presenter = Presenter(view, data)
    presenter.run()
