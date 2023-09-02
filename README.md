# batchConvert2Pdf
Python ttk GUI app conversion tool from .doc and .docx to .pdf format
![image](https://github.com/WerewolfC/batchConvert2Pdf/assets/136624525/21cd78c5-ff9a-4d3e-b097-7a8ad364fb83)

By choosing the source folder, all *.docx and *.doc files from that folder and the subfolders will be selected for conversion to .pdf.
		
Each individual converted file can be saved in the same folder as the original .doc file or all the pdf files can be saved in the selected target folder.
In case the same doc file (same filename) exists in the source folder (including subfolders), the converted files will have (0), (1)... appended to the pdf filename. If the pdf filename already exists in the target folder before conversion, the pdf file will be overwritten.


The option of having the bookmarks ( based on word file header formatting) is enabled by default.

# System requirements
- Windows
- Microsoft Word
- Python 3.11

Tested with Windows 10, Word 365 and Python 3.11

# Setup and how to use
- Download the zipped code and extract it.
- Run setup.bat to create Python virtual enviroment and the launcher file.


To start the application, use launcher.bat.


# Credits
Thanks [AlJohri](https://github.com/AlJohri) for hint that ExportAsFixedFormat can be used to generate pdf with bookmarks.
