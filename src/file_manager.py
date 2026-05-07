import os
from pathlib import Path
from typing import AnyStr, List


class FileManager:
    __RESOURCES_DIR = "data"

    def create_data(self, folders: List[str] | str | None = None) -> Path:
        folder_list = [] if folders is None else self.__folders(folders)
        project_dir = self.get_project_dir()
        self.__create_folder(project_dir, [self.__RESOURCES_DIR, *folder_list])
        return project_dir / self.__RESOURCES_DIR / Path(*folder_list)

    def __create_folder(self, path: Path, folders: List[str] | str):
        folders = self.__folders(folders)
        for folder in folders:
            path = path / folder
            path.mkdir(exist_ok=True)

    def get_project_dir(self) -> Path:
        path = self.__get_path_dir(__file__)
        return path.parent

    def __get_path_dir(self, cls: os.PathLike[AnyStr]) -> Path:
        file = os.path.abspath(cls)
        folder = os.path.dirname(file)
        return Path(folder)

    def __folders(self, folders: List[str] | str):
        return folders if isinstance(folders, list) else [folders]
