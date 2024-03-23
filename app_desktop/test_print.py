import tkinter as tk

class OutputWindow:
    def __init__(self, root):
        self.root = root
        self.output_window = tk.Toplevel(root)
        self.text_widget = tk.Text(self.output_window, wrap="word")
        self.text_widget.pack(fill="both", expand=True)

    def write_output(self, text):
        self.text_widget.insert("end", text)
        self.text_widget.see("end")  # スクロールして最後の行を表示する

# 使用例
if __name__ == "__main__":
    root = tk.Tk()
    output_window = OutputWindow(root)

    # プリント関数をカスタマイズして出力をウィンドウに表示する
    def custom_print(*args, **kwargs):
        text = " ".join(map(str, args)) + "\n"
        output_window.write_output(text)

    # プリント関数を置き換える
    import builtins
    builtins.print = custom_print

    # ここからプログラムを実行する
    a = 111
    b = 11
    print("Hello, World!")
    print("This is a test message.")
    print(a+b)

    root.mainloop()

