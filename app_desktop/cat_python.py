import os
def show_file_contents(file_path):
    # os.system('cat ${file_path}')
    try:
        with open(file_path, "r", encoding='utf-8') as file:
            contents = file.read()
            print("ファイルの中身:")
            print(contents)
            file.close()
    except FileNotFoundError:
        print("ファイルが見つかりませんでした。")

# 使用例
file_path = "test_print.py"  # ファイルのパスを指定
show_file_contents(file_path)