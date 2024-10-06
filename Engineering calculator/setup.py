from cx_Freeze import setup, Executable
import sys
import os

# Increase the recursion limit
sys.setrecursionlimit(1500)

# Determine the absolute path to the icon
icon_path = os.path.join(os.path.dirname(__file__), 'icon.ico')
# print(f"icon path:{icon_path}")
# print(f"path: {os.path.dirname(__file__)}")

# Dependencies are automatically detected, but it might need fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('EngineeringCalc.py', base=base, 
               target_name='Engineering Calculator', 
               icon=icon_path)
]

setup(name='Engineering calc',
      version='1',
      description='Engineering calc for engineering students',
      options={'build_exe': build_options},
      executables=executables)
