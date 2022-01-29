from pathlib import Path

import appdirs


class FileIO:

    @staticmethod
    def get_data_directory():
        appname = "Mighty Useful"
        appauthor = "Nightmare"
        data_dir = appdirs.user_data_dir(appname, appauthor)
        print(data_dir)

        dir_path = Path(data_dir)
        tdir_path = dir_path.parent
        if not tdir_path.exists():
            tdir_path.mkdir(exist_ok=True)

        if not dir_path.exists():
            dir_path.mkdir(exist_ok=True)
        return dir_path
