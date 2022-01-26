import appdirs
from pathlib import Path


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


# if default file exists, return it.  if not return directory
def get_data_file():
    dir_path = get_data_directory()
    file_name = "all.csv"
    file_path = dir_path / file_name

    if file_path.exists():
        print("File Exists")
        return file_path
    else:
        print("File Nexists")
        return dir_path


# if default file exists, return it.  if not return None
def get_strategies_file():
    dir_path = get_data_directory()
    file_name = "strategies.csv"
    file_path = dir_path / file_name

    if file_path.exists():
        print("Config File Exists")
        return file_path
    else:
        print("Config File Nexists")
        return None
