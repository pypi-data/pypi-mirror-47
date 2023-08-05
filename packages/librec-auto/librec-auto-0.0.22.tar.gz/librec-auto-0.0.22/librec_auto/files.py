from pathlib2 import Path
import utils
import hashlib


class Files:
    """
    This class encapsulates the file system for librec-auto.

    The files for librec-auto can be stored in a number of possible locations:
    - global location: determined by the install location of librec-auto
    - data-specific location: determined by the location of a data directory
    - user-specific location: associated with the user's home directory
    - experiment-specific location: in a directory associated with a specific experiment.

    These are the types of files that are managed:
    - configuration files (XML). Stores information about how experiments are configured.
    - properties files (key=value format). Generated from configuration files for input to librec
    - split files (UIR or UIRT format). Generated by separating input data files into different test/training splits
    - experiment logs (csv files). Content is algorithm-specific. Generated by a run on the
    """

    _global_path = None
    _user_path = None
    _exp_path = None
    _config_dir_name = None
    _data_dir_name = None
    _res_dir_name = None
    _split_dir_name = None

    _DEFAULT_USER_PATH_STR = "~/.librec-auto"
    _DEFAULT_GLOBAL_PATH_STR = "/opt/librec-auto"

    _DEFAULT_CONFIG_DIR_NAME = "conf"
    _DEFAULT_DATA_DIR_NAME = "data"
    _DEFAULT_RES_DIR_NAME = "result"
    _DEFAULT_SPLIT_DIR_NAME = "split"

    _DEFAULT_SYSTEM_CONFIG_FILENAME = "librec-auto-config.xml"
    _DEFAULT_CACHE_FILENAME = ".cache"

    def __init__(self):
        self._config_dir_name = self._DEFAULT_CONFIG_DIR_NAME
        self._data_dir_name = self._DEFAULT_DATA_DIR_NAME
        self._res_dir_name = self._DEFAULT_RES_DIR_NAME
        self._split_dir_name = self._DEFAULT_SPLIT_DIR_NAME

        maybe_global_path = Path(Files._DEFAULT_GLOBAL_PATH_STR)
        if maybe_global_path.is_dir():
            self._global_path = maybe_global_path
        maybe_user_path = Path(Files._DEFAULT_USER_PATH_STR)
        if maybe_user_path.is_dir():
            self._user_path = maybe_user_path

    def get_global_path(self): return self._global_path

    def get_user_path(self): return self._user_path

    def get_exp_path(self): return self._exp_path

    def set_global_path(self, path): self._global_path = Path(path)

    def set_user_path(self, path): self._user_path = Path(path)

    def set_exp_path(self, path): self._exp_path = Path(path)

    @staticmethod
    def dir_hash(maybe_path):
        """
        Starting from a directory, gets all subdirectories, extracts the individual files and creates a hash value
        using the file name, size, and last modification date.

        Probably just modification date is enough.
        :param maybe_path:
        :return:
        """
        hasher = hashlib.sha1()
        path = utils.force_path(maybe_path)
        full_listing = path.glob('**/*')
        files = [fl for fl in full_listing if fl.is_file()]
        for fl in files:
            fl_stat = fl.stat()
            fl_size = fl_stat.st_size
            fl_date = fl_stat.st_mtime
            fl_info = "{}-{}-{}".format(fl.name, fl_size, fl_date)
            fl_bytes = fl_info.encode('utf-8')
            hasher.update(fl_bytes)
        return hasher.hexdigest()

    def find_file(self, name):
        """
        Returns the first path corresponding the file name, searching first in the experiment directory,
        then in the user's local directory, then in the global directory.
        :param name:
        :return: path or None
        """
        exp_path = self.get_exp_path() / name
        if exp_path.is_file():
            return exp_path
        else:
            user_path = self.get_user_path() / name
            if user_path.is_file():
                return user_path
            else:
                global_path = self.get_global_path() / name
                if global_path.is_file():
                    return global_path
                else:
                    return None

    def find_config_file(self, name):
        return self.find_file(''.join([self._config_dir_name, "/", name]))

    def find_data_file(self, name):
        return self.find_file(''.join([self._data_dir_name, "/", name]))
