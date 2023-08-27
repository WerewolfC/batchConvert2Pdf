# from docx2pdf import convert
# convert("input.docx")

from bulkPdfConvert.gui import MainWindow
from bulkPdfConvert.presenter import Presenter
import bulkPdfConvert.utils as utils


from tqdm.auto import tqdm
from win32com import client as win32Client
from pathlib import Path


def resolve_paths(input_path, output_path):
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve() if output_path else None
    output = {}
    if input_path.is_dir():
        output["batch"] = True
        output["input"] = str(input_path)
        if output_path:
            assert output_path.is_dir()
        else:
            output_path = str(input_path)
        output["output"] = output_path
    else:
        output["batch"] = False
        assert str(input_path).endswith((".docx", ".DOCX", ".doc", ".DOC"))
        output["input"] = str(input_path)
        if output_path and output_path.is_dir():
            output_path = str(output_path / (str(input_path.stem) + ".pdf"))
        elif output_path:
            assert str(output_path).endswith(".pdf")
        else:
            output_path = str(input_path.parent / (str(input_path.stem) + ".pdf"))
        output["output"] = output_path
    return output


def convertToPdf(input_path, output_path=None):
    word = win32Client.Dispatch("Word.Application")
    wdExportFormatPDF = 17
    wdExportCreateHeadingBookmarks = 1

    paths = resolve_paths(input_path, output_path)
    pbar = tqdm(total=1)
    docx_filepath = Path(paths["input"]).resolve()
    pdf_filepath = Path(paths["output"]).resolve()
    print(docx_filepath)
    print(pdf_filepath)
    doc = word.Documents.Open(str(docx_filepath))
    doc.ExportAsFixedFormat (OutputFileName=str(pdf_filepath),
                             ExportFormat=wdExportFormatPDF,
                             CreateBookmarks=wdExportCreateHeadingBookmarks)
    doc.Close(0)
    pbar.update(1)


if __name__ == "__main__":
    #convertToPdf("C:\\00_User\\04_Projects\\Python\\PDFconverter\\input.docx")
    # f_data = utils.create_file_struct(r"C:\00_User\04_Projects\Python\PDFconverter\testFolder")
    # from pprint import pprint
    # #pprint(f_data)
    # for each in f_data:
    #     pprint(each)
    # demoWindow = MainWindow(utils.GUI_THEME)
    # demoWindow.mainloop()

    view = MainWindow(utils.GUI_THEME)
    presenter = Presenter(view)
    presenter.run()