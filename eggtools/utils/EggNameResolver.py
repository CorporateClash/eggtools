import os
import logging

from panda3d.core import Filename


class EggNameResolver:
    _search_paths = list()
    OLD_PREFIX = "ttcc"
    NEW_PREFIX = "cc"

    def __init__(self, search_paths, loglevel=logging.CRITICAL):
        """
        Utility class to try and resolve certain texture names automatically
        """
        self.search_paths = search_paths
        logging.basicConfig(level=loglevel)

    @property
    def search_paths(self) -> list:
        return self._search_paths

    @search_paths.setter
    def search_paths(self, path: list):
        if type(path) is not list:
            path = [path]
        for sp in path:
            self._search_paths.append(sp)

    def try_different_names(self, filename: str, prefix_type: str = "t") -> str:
        # Replace: toontown_background --> tt_t_background
        new_filename = filename.replace(f"{self.OLD_PREFIX}_", f"{self.NEW_PREFIX}_{prefix_type}_")
        if not new_filename.startswith(f"{self.NEW_PREFIX}_{prefix_type}_"):
            new_filename = f"{self.NEW_PREFIX}_{prefix_type}_{filename}"

        for filepath in self.search_paths:
            # We have to convert back into Filename because os.path can't find files with like
            # /f/path/to/assets\mytexture.png
            if os.path.isfile(Filename.fromOsSpecific(os.path.join(filepath, new_filename))):
                logging.info(f"found similar texture name to {filename}: {new_filename}")
                return new_filename
        # can't find any hits, just return em back
        return filename


    # Todo: Search via md5 hash?
