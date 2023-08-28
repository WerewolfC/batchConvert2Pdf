"""Main app class that is launching the app"""
from bulkPdfConvert.gui import MainWindow
from bulkPdfConvert.presenter import Presenter
import bulkPdfConvert.utils as utils


if __name__ == "__main__":
    view = MainWindow(utils.GUI_THEME)
    presenter = Presenter(view)
    presenter.run()
