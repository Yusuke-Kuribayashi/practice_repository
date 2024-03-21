# -*- coding: utf-8 -*-
import tkinter as tk
import os, subprocess, time
from tkinter import ttk
from my_module import ScoringLibs

class ScoringSupportSystem(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sLib = ScoringLibs()
        self.next_button_status = True

        self.master.title("Scoring Support System")
        self.master.geometry("400x300")

        # 採点する回を選択 ####
        self.lesson_label = tk.Label(self.master,
                                text="採点する回を選択してください(>ㅅ<)")
        self.lesson_label.grid(row=0, column=0, padx=10, pady=5)
        self.lesson_combobox = ttk.Combobox(self.master,
                                           values=["第"+str(i)+"回" for i in range(1,6)])
        self.lesson_combobox.grid(row=1, column=0, padx=10, pady=5)

        # 開始ボタン ####
        self.start_button = tk.Button(self.master,
                                      text="採点開始",
                                      command=lambda:self.scoring_start())
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 点数入力 ####
        self.score_label = tk.Label(self.master,
                                    text="点数を選択した後に，次へボタンを押してください....")
        self.score_label.grid(row=3, column=0, padx=10, pady=5)
        self.score_combobox = ttk.Combobox(self.master,
                                           values=[str(i) for i in range(0,6)])
        self.score_combobox.grid(row=4, column=0, padx=10, pady=5)
        self.score_combobox.current(5)
        
        # 次へボタン ####
        self.next_button = tk.Button(self.master,
                                     text="次の採点",
                                     command=lambda:self.next_stage())
        self.next_button.grid(row=5, column=0, columnspan=2, pady=10)

        # exitボタン ####
        self.exit_button = tk.Button(self.master,
                                     text="閉じる",
                                     command=lambda:self.master.destroy())
        self.exit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # setupボタン ####
        self.setup_button = tk.Button(self.master,
                                      text="set up",
                                      command=lambda:self.setup_func())
        self.setup_button.grid(row=1, column=1, columnspan=2, pady=10)

    def setup_func(self):
        dir = ["第"+str(i)+"回" for i in range(1,7)]
        for i in dir:
            DIR_PATH = os.getcwd() + "/kaitou/" + i
            self.sLib.create_dir(DIR_PATH)
        print(f'finish setting up successfully')

    def scoring_start(self):
        WORK_DIR = os.getcwd() + "/kaitou/" + self.lesson_combobox.get()
        self.sLib.set_save_dir_path(WORK_DIR)
        self.sLib.traverse_folder(WORK_DIR)
        
        other_window = tk.Toplevel(self)
        other_window.title("other window")
        other_window.geometry("500x400")

        # other_window.grab_set()
        other_window.focus_set()
        other_window.transient(self.master)

        for file_name in os.listdir(self.sLib.save_dir_path):
            if not self.next_button_status:
                print(f'Waiting for pressing next button....')
                while not self.next_button_status:
                    time.sleep(1)

            file_path = os.path.join(self.sLib.save_dir_path, file_name)
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
                self.next_button_status = False

        app.wait_window(other_window)
    
    def next_stage(self):
        self.next_button_status = True


if __name__=='__main__':
    root = tk.Tk()
    app = ScoringSupportSystem(root)
    app.mainloop()
