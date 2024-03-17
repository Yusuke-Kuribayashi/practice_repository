import tkinter as tk
from tkinter import ttk

def say_hello():
    hello_window = tk.Toplevel(root)
    hello_label = tk.Label(hello_window, text="Hello World!")
    hello_label.pack()

def show_result():
    result_window = tk.Toplevel(root)
    selected_value = score_combobox.get()
    result_label = tk.Label(result_window, text=f"Selected score: {selected_value}")
    result_label.pack()

def start_program():
    # selected_value = round_combobox.get()
    # for i in range(int(selected_value)):
    say_hello()

root = tk.Tk()
root.title("Program")

round_label = tk.Label(root, text="Select round:")
round_label.grid(row=0, column=0, padx=10, pady=5)
round_combobox = ttk.Combobox(root, values=["第"+str(i)+"回" for i in range(1, 6)])
round_combobox.grid(row=0, column=1, padx=10, pady=5)

start_button = tk.Button(root, text="Start")
start_button.grid(row=1, column=0, columnspan=2, pady=10)
start_button.configure(command=start_program)

score_label = tk.Label(root, text="Select score:")
score_label.grid(row=2, column=0, padx=10, pady=5)
score_combobox = ttk.Combobox(root, values=["A", "B", "C", "D", "E"])
score_combobox.grid(row=2, column=1, padx=10, pady=5)
score_combobox.current(0)

exit_button = tk.Button(root, text="Exit", command=show_result)
exit_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
