import pandas as pd
from utils.file import FileUtils


class Excel(FileUtils):
    def read(self, path, sheetname=None):
        return pd.read_excel(filepath=path, sheet_name=sheetname)
