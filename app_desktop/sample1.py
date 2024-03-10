import tkinter as tk
from tkinter import messagebox as mbox


# ボタンを押したときの処理
def calc():
    # 一人当たりの費用を計算
    total = float(texttotal.get())
    number_of_people = float(textpeople.get())
    split_the_bill = total / number_of_people

    # 結果をラベルに表示
    s = f"1人あたり{split_the_bill}円".format()
    labelResult['text'] = s

# windowの作成
win = tk.Tk()
win.title("sampleアプリ")
win.geometry("500x250")

# windowの中身を作成
labeltotal = tk.Label(win, text=u'合計金額: ')
labeltotal.pack()

labelpeople = tk.Label(win, text=u'人数: ')
labelpeople.pack()

labelResult = tk.Label(win, text=u'---')
labelResult.pack()

# ボタンを押したときの対応
calcButton = tk.Button(win, text=u'結果を見る！')
calcButton["command"] = calc
calcButton.pack()

# 質問内容を記載
texttotal = tk.Entry(win)
texttotal.insert(tk.END, input('合計金額は？:'))
texttotal.pack()

textpeople = tk.Entry(win)
textpeople.insert(tk.END, input('何人で割る？:'))
textpeople.pack()

#ウィンドウを動かす
win.mainloop()