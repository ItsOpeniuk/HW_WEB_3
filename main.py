from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil

class Processing:
    def __init__(self, source_file_path, destination_root_folder):
        self.source_file_path = Path(source_file_path)
        self.destination_root_folder = Path(destination_root_folder)

    def process_file(self):
        path_file = self.source_file_path
        root_folder = self.destination_root_folder

        file_extension = path_file.suffix[1:]
        file_name = path_file.stem
        create_folders = root_folder.joinpath(file_extension)
        create_folders.mkdir(exist_ok=True)
        target_file = create_folders.joinpath(file_name + "." + file_extension)
        shutil.move(path_file, target_file)

    def process_folder(self):
        for i in self.source_file_path.iterdir():
            if i.is_dir():
                self.source_file_path = i
                self.process_folder()
            else:
                self.process_file()
        else:
            self.delete_empty_folder()

    def delete_empty_folder(self):
        for folder in self.destination_root_folder.iterdir():
            if folder.is_dir() and not list(folder.iterdir()):
                folder.rmdir()

    @staticmethod
    def main_thread(folder_path: Path):
        if folder_path.exists() and folder_path.is_dir():
            processor = Processing(folder_path, folder_path)
            with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
                executor.submit(processor.process_folder)
        else:
            print("folder does not exist.")


if __name__ == "__main__":
    folder_path = Path("/Users/Openiuk/Hom_wokr_3")
    Processing.main_thread(folder_path)


