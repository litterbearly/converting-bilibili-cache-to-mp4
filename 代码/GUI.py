import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import json
import _thread


def replace_illegal_characters(str_name):
    # 替换不合法的字符
    list_illegal_characters = [" ", "<", ">", "?", "/", "\\", ":", "*", "|"]  # 不合法字符列表
    for i in list_illegal_characters:
        str_name = str_name.replace(i, "_")

    return str_name


def get_output_folder_name(filename_json):
    # 从json文件提取提取课程名称和视频名称
    print(filename_json)
    json_file = open(filename_json, "r", encoding="UTF-8")
    dict_json = json.load(json_file)
    json_file.close()

    # 替换不合法的字符
    all_name = replace_illegal_characters(dict_json['title'])
    out_name = replace_illegal_characters(dict_json['page_data']['part'])

    return all_name, out_name


def convert(path_ffmpeg, in_path_list, out_path):
    for in_path in in_path_list:  # 遍历所有课程
        dir_list = os.listdir(in_path)  # 获取课程下的所有单个视频目录列表
        # dir_list = sorted(dir_list, key=int, reverse=False)  # 按数值大小进行排序
        # for i in dir_list:  # 从列表中删除非缓存视频目录
        #     if len(i) > 3:
        #         dir_list.remove(i)
        for i in dir_list:  # 遍历课程下的所有视频目录
            for root, dirs, files in os.walk(in_path + "/" + i):
                if dirs:
                    name = str(dirs[0])
                    path_in = "{}/{}/{}".format(in_path, i, name)
                    print(path_in)
                    video_in = "{}/video.m4s".format(path_in)  # 输入视频(无声音)路径
                    audio_in = "{}/audio.m4s".format(path_in)  # 输入音频路径

                    # 生成输出目录和输出文件名
                    all_name, out_name = get_output_folder_name("{}/{}/entry.json".format(in_path, i))
                    if not os.path.exists(out_path + "/" + "/" + all_name):
                        os.makedirs(out_path + "/" + "/" + all_name)
                    file_name_out = "{}/{}/{}-{}.mp4".format(out_path, all_name, i, out_name)
                    command_text = path_ffmpeg + ' -i {} -i {} -c:v copy -strict experimental {} -n'\
                        .format(video_in, audio_in, file_name_out)
                    os.system(command_text)


class GUI:
    path_video = []
    out_path = ''
    path_ffmpeg = 'D:/Soft/ffmpeg/bin/ffmpeg.exe'
    font_style = ("宋体", 16, "bold", "italic")

    def __init__(self):
        self.root = tk.Tk()
        self.root.minsize(800, 600)  # 窗口尺寸
        self.root.title("bilibili缓存转Mp4工具")

        # 选择ffmpeg.exe文件路径
        self.path0 = tk.StringVar()  # 变量path
        self.path0.set(self.path_ffmpeg)
        tk.Label(self.root, text="ffmpeg.exe文件路径:", font=self.font_style) \
            .place(x=100, y=50)  # 输入框，标记，按键
        tk.Entry(self.root, textvariable=self.path0, width=90).place(x=100, y=100)  # 输入框绑定变量path
        tk.Button(self.root, text="选择文件", font=self.font_style, command=self.select_ffmpeg_path) \
            .place(x=500, y=50)

        # 选择缓存文件目录
        self.path = tk.StringVar()  # 变量path
        self.path.set(self.path_video)
        tk.Label(self.root, text="课程视频缓存文件夹:(纯数字)", font=self.font_style)\
            .place(x=100, y=150)  # 输入框，标记，按键
        tk.Entry(self.root, textvariable=self.path, width=90).place(x=100, y=200)  # 输入框绑定变量path
        tk.Button(self.root, text="目录选择", font=self.font_style, command=self.select_in_path)\
            .place(x=500, y=150)
        tk.Button(self.root, text="清除", font=self.font_style, command=self.clear_selected_folder)\
            .place(x=650, y=150)

        # 选择输出文件目录
        self.path2 = tk.StringVar()  # 变量path
        self.path2.set(self.out_path)
        tk.Label(self.root, text="输出目录:", font=self.font_style).place(x=100, y=250)  # 输入框，标记，按键
        tk.Entry(self.root, textvariable=self.path2, width=90).place(x=100, y=300)  # 输入框绑定变量path
        tk.Button(self.root, text="目录选择", font=self.font_style, command=self.select_out_path)\
            .place(x=600,y=250)

        tk.Button(self.root, text="开始转换", font=self.font_style, command=self.convert_to_mp4)\
            .place(x=600, y=500)

        self.root.mainloop()

    def select_ffmpeg_path(self):  # ffmpeg路径选择
        # 选择文件path_接收文件地址
        path0_ = tkinter.filedialog.askopenfilename()
        self.path0.set(path0_)
        self.path_ffmpeg = self.path0.get()
        print(self.path_ffmpeg)



    def select_in_path(self):  # 输入目录添加
        # 选择文件path_接收文件地址
        path_ = tkinter.filedialog.askdirectory()

        # path设置path_的值
        if not self.path.get():
            self.path.set(path_)
        else:
            self.path.set(self.path.get() + "," + path_)
        self.path_video = self.path.get().split(",")

    def clear_selected_folder(self):  # 清空已选择的输入文件夹
        self.path.set("")
        self.path_video = self.path.get().split(",")

    def select_out_path(self):  # 输出目录选择
        # 选择文件path_接收文件地址
        path2_ = tkinter.filedialog.askdirectory()
        # path设置path_的值
        self.path2.set(path2_)
        if "" != self.path2.get():
            self.out_path = self.path2.get()

    def convert_to_mp4(self):  #
        if not self.path_video:
            tkinter.messagebox.showwarning('警告', '请选择需要转换的缓存文件夹')
        else:
            _thread.start_new_thread(convert, (self.path_ffmpeg, self.path_video, self.out_path))
            self.path_video = []


if __name__ == '__main__':
    GUI()
