# -*- coding: utf-8 -*-

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.master.title("タイトル")
        self.master.geometry("400x300") #windowsのサイズ(幅x高さ)

        # ボタンの作成
        btn_exit = tk.Button(
            self.master,
            text = "Exit",
            command = lambda:self.master.destroy()
        )
        btn_exit.pack()

        # 別ウィンドウの表示
        btn_model = tk.Button(
            self.master,
            text = "other window",
            command = self.create_other_window
        )
        btn_model.pack()

    def create_other_window(self):
        dlg_modeless = tk.Toplevel(self)
        dlg_modeless.title("other window")
        dlg_modeless.geometry("300x200")

        dlg_modeless.grab_set()
        dlg_modeless.focus_set()
        dlg_modeless.transient(self.master)

        print("hello world")

        app.wait_window(dlg_modeless)  
        print("ダイアログが閉じられた")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop() # ここでウィンドウが消えないように無限ループ
