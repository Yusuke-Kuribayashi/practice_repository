# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

# memo ####
# ボタンの挙動は.configure(command=〇〇)で後から追加可能
# comboboxの値を取得するときは，self.lesson_combobox.get()
###########
class GUI_Config(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

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
                                      text="採点開始")
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
                                     text="次の採点")
        self.next_button.grid(row=5, column=0, columnspan=2, pady=10)

        # exitボタン ####
        self.exit_button = tk.Button(self.master,
                                     text="閉じる",
                                     command=lambda:self.master.destroy())
        self.exit_button.grid(row=6, column=0, columnspan=2, pady=10)

if __name__=="__main__":
    root = tk.Tk()
    app = GUI_Config(root)
    app.mainloop()
