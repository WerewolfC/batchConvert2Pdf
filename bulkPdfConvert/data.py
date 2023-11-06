"""File list data class"""
from pathlib import Path
from os import walk

from bulkPdfConvert.utils import FolderContainer, ConvertFileFormat, FileStatus


class Filelist:
    """File list class"""

    def __init__(self) -> None:
        self.raw_data_list = []
        self.explicit_data_list = []
        self.options = None

    def set_options(self, options_obj):
        """Saves a ConvertOptions obj locally"""
        self.options = options_obj

    def create_raw_data(self, source_folder):
        """Recursively reads all the files in source folder
        and creates a list to be displayed on GUI and parsed
        """
        raw_generator = []
        raw_generator = walk(Path(source_folder))
        for current, _, files in raw_generator:
            # search for .doc and .docx extensions
            doc_list = []
            doc_list = [
                doc_file
                for doc_file in files
                if doc_file.endswith((".docx", ".DOCX", ".doc", ".DOC"))
            ]
            if doc_list:
                # add path + file list to the raw list
                self.raw_data_list.append(FolderContainer(current, doc_list))

    def recursive_check_names(self, output_full_path, object_pool, iterations):
        """Check recursive if the output name exists in a pool
        and returns the unique name
        """
        # check if pdf already exists and if so add -Copy to the end of name
        if output_full_path not in [obj.output_full_path for obj in object_pool]:
            return output_full_path
        else:
            new_full_path = output_full_path.with_stem(
                output_full_path.stem + f"({iterations})"
            )
            return self.recursive_check_names(
                new_full_path, object_pool, iterations + 1
            )

    def create_explicit_list(self):
        """create explicit file list [ [input0_full_path, output1_full_path], ..... ]"""
        print(f"options in data {self.options}")
        for file_obj in self.explicit_data_list:
            # create output full file path
            if self.options.use_same_folder:
                output_path = file_obj.input_full_path.parents[0]
            else:
                output_path = self.options.folder_target_path

            filename = file_obj.input_full_path.name
            temp_out_full_path = self.recursive_check_names(
                output_path.joinpath(filename).with_suffix(".pdf"),
                self.explicit_data_list,
                0,
            )
            file_obj.output_full_path = temp_out_full_path
        # TODO: remove print
        from pprint import pprint

        pprint(f"Explicit list --> \n{self.explicit_data_list}")

    def create_initial_list(self):
        """Creates a list of files that were found in the source folder"""
        file_no = 1
        self.explicit_data_list = []
        for container in self.raw_data_list:
            for file in container.file_list:
                converted_file = ConvertFileFormat(
                    file_no,
                    FileStatus.ADDED,
                    Path(container.folder_source_path).joinpath(file),
                    None,
                )

                # create [input_path, output_path] and add them to self.explicit_data_list
                self.explicit_data_list.append(converted_file)
                file_no += 1
                # TODO: remove print
        from pprint import pprint

        pprint(f"Initial list --> \n{self.explicit_data_list}")

    def get_explicit_list(self):
        """Returns the explicit list"""
        return self.explicit_data_list

    def update_status_explicit_list(self, input_file_path, status):
        """Updates the status value for a specified element
        for which the full source path is provided
        """
        # search the source filename in the explicit list and get the file_no
        file_idx = [
            file.file_number
            for file in self.explicit_data_list
            if file.input_full_path == input_file_path
        ]
        if file_idx:
            self.explicit_data_list[file_idx[0]].conversion_status = status

    def update_target_info_explicit_list(self, source_file_path, target_file_path):
        """Updates the target filename and full target path for
        the file_number provided
        """
        # search for input filename in the explicit list and get the file_no
        file_idx = [
            file.file_number
            for file in self.explicit_data_list
            if file.input_full_path == source_file_path
        ]
        if file_idx:
            self.explicit_data_list[file_idx[0]].output_full_path = target_file_path
