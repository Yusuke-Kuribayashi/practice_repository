import os, time
import nbformat
from nbconvert import PythonExporter
import subprocess
from IPython.display import clear_output

class ScoringLibs():
    def __init__(self):
        self.save_dir_path = None
        self.save_dir_name = "temporary_dir" 

    """
    @brief: ディレクトリを作成する関数
    @param: dir_path 作成したいディレクトリのパス
    """
    def create_dir(self, dir_path: str):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
    """
    @brief: pythonファイルを保存するディレクトリのパスを作成する関数
    @param: save_dir_path 保存したいディレクトリのパス
    """
    def set_save_dir_path(self, save_dir_path):
        self.save_dir_path = save_dir_path + "/" + self.save_dir_name
        print(f'save dir: {self.save_dir_path}')
        self.create_dir(self.save_dir_path)

    """
    @brief: pythonファイルであるかを判断するプログラム
    @param: file_path ファイルのパス
    """
    def is_python_file(self, file_path: str):
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() == '.py'

    """
    @brief: ipynbファイルをpyファイルに変換する関数
    @param: ipynb_file ipynbファイルのパス
    @param: output_folder 変換したpyファイルの保存先
    """
    def convert_ipynb_to_py(self, ipynb_file: str, output_folder: str):
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

        print(f'successfully {os.path.basename(output_path)}')

    """
    @brief: 選択したディレクトリ内にあるディレクトリを走査し,すべてのipynbファイルをpyファイルに変換する関数
    @param: work_dir_path 作業するディレクトリのパス
    """
    def traverse_folder(self, work_dir_path: str):
        for file_name in os.listdir(work_dir_path):
            if file_name == ".ipynb_checkpoints" or file_name == self.save_dir_name:
                continue
            file_path = os.path.join(work_dir_path, file_name)
            if os.path.isdir(file_path):
                self.traverse_folder(file_path)
            elif self.is_python_file(file_path):
                break
            else:
                self.convert_ipynb_to_py(file_path, self.save_dir_path)

    """
    @brief: pythonファイルを実行する関数
    """
    def run_python_file(self):
        for file_name in os.listdir(self.save_dir_path):
            file_path = os.path.join(self.save_dir_path, file_name)
            if os.path.isdir(file_path):
                continue
            else:
                result = subprocess.run(['python', file_path], capture_output=True, text=True)
                if result.returncode == 0:
                    print("Pythonファイルを正常に実行されました")
                    print(result.stdout)
                    time.sleep(5)
                    clear_output()
                else:
                    print("Pythonファイルの実行中にエラーが発生しました")
                    print(result.stderr)
