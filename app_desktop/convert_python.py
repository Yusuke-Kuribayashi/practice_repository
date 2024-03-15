import os
import nbformat
from nbconvert import PythonExporter

def convert_ipynb_to_py(ipynb_file, output_folder):
    # ファイル名を取得
    file_name = os.path.basename(ipynb_file)
    # 拡張子を除去して.pyファイル名を作成
    py_file = os.path.splitext(file_name)[0]+".py"
    # 出力先のパスを作成
    output_path = os.path.join(output_folder, py_file)

    # .ipynbファイルを読み込む
    with open(ipynb_file, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # PythonExporterを使用して，.pyファイルに変換
    exporter = PythonExporter()
    source, _ = exporter.from_notebook_node(nb)

    # .pyファイルに書き込む
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(source)

    print(f'successfully')

def traverse_folder(folder_path):
    print(folder_path)

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isdir(file_path):
            traverse_folder(file_path)
        else:
            print(file_path)

CURRENT_PATH = os.getcwd()
WORK_PATH = "/kaitou/第1回"
traverse_folder(CURRENT_PATH+WORK_PATH)

ipynb_file_path = "a.ipynb"
output_folder_path = "python_folder"

# フォルダが存在しない場合は作成
# if not os.path.exists(output_folder_path):
#     os.makedirs(output_folder_path)

# .ipynbファイルを.pyファイルに変換して保存
