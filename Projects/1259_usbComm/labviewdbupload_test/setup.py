import cx_Freeze
from cx_Freeze import setup, Executable

setup(name = "labviewdbupload",
      version = "0",
      description = "Preliminary",
      executables = [Executable("labviewdbupload.py")]
      )
