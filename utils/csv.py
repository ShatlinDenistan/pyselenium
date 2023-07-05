import pandas as pd

from utils.file import FileUtils


class CSV(FileUtils):
    def read(self, path, sheetname=None):
        return pd.read_csv(filepath_or_buffer=path)
