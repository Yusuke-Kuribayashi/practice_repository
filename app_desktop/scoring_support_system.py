# -*- coding: utf-8 -*-
import tkinter as tk
import os, subprocess, time
from tkinter import ttk
from my_module import ScoringLibs

class ScoringSupportSystem(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sLib = ScoringLibs()
        self.run_flag = False


        self.master.title("Scoring Support System")
        self.master.geometry("1000x500")

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

        # プログラム実行フラグ ####
        self.run_button = tk.Button(self.master,
                                      text="run python file",
                                      command=lambda:self.flag_func())
        self.run_button.grid(row=1, column=3, columnspan=2, pady=10)

        # ウィジェットの作成 ####
        self.text_widget = tk.Text(self.master, wrap="word")
        self.text_widget.grid(row=2, column=2, rowspan=7, columnspan=3)

    def setup_func(self):
        dir = ["第"+str(i)+"回" for i in range(1,7)]
        for i in dir:
            DIR_PATH = os.getcwd() + "/kaitou/" + i
            self.sLib.create_dir(DIR_PATH)
        print(f'finish setting up successfully')

    def scoring_start(self):
        # pythonファイルを一か所に集める
        WORK_DIR = os.getcwd() + "/kaitou/" + self.lesson_combobox.get()
        self.sLib.set_save_dir_path(WORK_DIR)
        self.sLib.traverse_folder(WORK_DIR)

        # pythonディレクトリの中身のファイルをすべて取得
        self.file_list = os.listdir(self.sLib.save_dir_path)

        # 初めのファイルを実行
        self.sLib.cat_python_file(self.file_list[0], self.custom_print)
        if self.run_flag:
            self.custom_print(f'----------\n')
            self.sLib.run_python_file(self.file_list[0], self.custom_print)

        del self.file_list[0]
    
    def next_stage(self):
        self.text_widget.delete(1.0, tk.END)
        time.sleep(2)

        # エクセルへの書き込み
        # self.score_combobox.get() 値の取得
        
        # 次のプログラムの実行
        if len(self.file_list) > 0:
            self.sLib.cat_python_file(self.file_list[0], self.custom_print)
            if self.run_flag:
                self.custom_print(f'----------\n')
                self.sLib.run_python_file(self.file_list[0], self.custom_print)
            del self.file_list[0]
        else:
            self.custom_print(f'Scoring has finished')

    def custom_print(self, *args, **kwargs):
        text = " ".join(map(str, args)) + "\n"
        self.text_widget.insert("end", text)
        self.text_widget.see("end")

    def flag_func(self):
        self.run_flag = not self.run_flag

if __name__=='__main__':
    root = tk.Tk()
    app = ScoringSupportSystem(root)
    app.mainloop()
