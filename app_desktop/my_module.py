import os
import nbformat
from nbconvert import PythonExporter
import subprocess

"""
@brief: ディレクトリを作成する関数
@param: dir_path 作成したいディレクトリのパス
"""
def create_dir(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

"""
@brief: pythonファイルであるかを判断するプログラム
@param: file_path ファイルのパス
"""
def is_python_file(file_path: str):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() == '.py'

"""
@brief: ipynbファイルをpyファイルに変換する関数
@param: ipynb_file ipynbファイルのパス
@param: output_folder 変換したpyファイルの保存先
"""
def convert_ipynb_to_py(ipynb_file: str, output_folder: str):
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

"""
@brief: 選択したディレクトリ内にあるディレクトリを走査し,すべてのipynbファイルをpyファイルに変換する関数
@param: work_dir_path 作業するディレクトリのパス
"""
def traverse_folder(work_dir_path: str, save_dir_name: str):
    save_dir_path = work_dir_path + save_dir_name
    for file_name in os.listdir(work_dir_path):
        file_path = os.path.join(work_dir_path, file_name)
        if os.path.isdir(file_path):
            traverse_folder(file_path, save_dir_name)
        elif is_python_file(file_path):
            break
        else:
            print(f'file_path: {file_path}\nsave_dir: {save_dir_path}')
            convert_ipynb_to_py(file_path, save_dir_path)

"""
@brief: pythonファイルを実行する関数
@param: dir_path 実行したいpythonファイルが保存されているディレクトリ
"""
def run_python_file(dir_path: str):
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isdir(file_path):
            continue
        else:
            result = subprocess.run(['python', file_path], capture_output=True, text=True)
            if result.returncode == 0:
                print("Pythonファイルを正常に実行されました")
                print(result.stdout)
            else:
                print("Pythonファイルの実行中にエラーが発生しました")
                print(result.stderr)
