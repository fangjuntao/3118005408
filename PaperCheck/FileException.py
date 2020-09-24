#读取的文件为空
class empty_error(Exception):
    def __init__(self):
        print("您输入的文本为空!!")
