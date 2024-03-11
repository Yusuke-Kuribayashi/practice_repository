# -*- coding: utf-8 -*-
import ipynb_import_lib

path_file = r"C:\Users\kuribayashi\practice_repository\app_desktop\sample.ipynb"
code1 =ipynb_import_lib.get_code_from_ipynb(path_file)
print(code1)