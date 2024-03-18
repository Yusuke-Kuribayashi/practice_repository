# -*- coding: utf-8 -*-
from set_gui import GUI_Config
import tkinter as tk
import nbformat
from nbconvert import PythonExporter
import os, subprocess

class ScoringSupportSystem(GUI_Config):
    def __init__(self, master=None):
        super().__init__(master)

        self.start_button.configure(command=lambda:print("aaa"))

    # フォルダーを移動する ####
    def traverse_folder(self):
        WORK_DIR_PATH = os.getcwd()+"/kaitou/"+self.lesson_combobox.get()
        SAVE_DIR_PATH = os.getcwd()+"/kaitou/"+self.lesson_combobox.get()+"/python_folder"
        for file_name in os.listdir(WORK_DIR_PATH):
            file_path = os.path.join(WORK_DIR_PATH, file_name)
            if os.path.isdir(file_path):
                self.traverse_folder(file_path)
            elif self.is_python_file(file_path):
                break
            else:
                print(file_path)
                self.convert_ipynb_to_py(WORK_DIR_PATH, SAVE_DIR_PATH)

    # ipynbファイルをpythonファイルに変換する関数 ####
    def convert_ipynb_to_py(self, ipynb_file, output_folder):
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

    #　pythonファイルであるかを確認 ####
    def is_python_file(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower() == '.py'
    
    # pythonファイルを実行 ####
    def run_python_file(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
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

    # 新しいwindowの作成 ####
    def create_new_window(self):
        execute_window = tk.Toplevel(self.master)
        execute_window.title("python window")
        label = tk.Label(execute_window, text="This is a execute window")
        label.pack()


if __name__=="__main__":
    root = tk.Tk()
    app = GUI_Config(root)
    app.mainloop()