from ast import Pass
from fileinput import filename
import json
from pathlib import Path
from collections.abc import ABC, abstractmethod

class FileUtils(ABC):
    
    @abstractmethod
    def read(path, sheetname):
        Pass

            
