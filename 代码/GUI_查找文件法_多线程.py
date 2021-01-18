import threading
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import json
import _thread


# 替换不合法的字符
def replace_illegal_characters(str_name):  # 替换不合法的字符
    list_illegal_characters = [" ", "<", ">", "?", "/", "\\", ":", "*", "|", "&"]  # 不合法字符列表
    for i in list_illegal_characters:
        str_name = str_name.replace(i, "_")
    return str_name


# 从json文件提取提取课程名称和视频名称
def get_output_folder_name(filename_json):
    # 从json文件提取提取课程名称和视频名称
    json_file = open(filename_json, "r", encoding="UTF-8")
    dict_json = json.load(json_file)
    json_file.close()

    # 替换不合法的字符
    all_name = replace_illegal_characters(dict_json['title'])
    out_name = replace_illegal_characters(dict_json['page_data']['part'])

    return all_name, out_name


# 创建GUI交互窗口
class GUI:
    path_video = 'D:/Python/哔哩哔哩缓存转换程序/download/'
    out_path = 'D:/Python/哔哩哔哩缓存转换程序/bilibili2/'
    # path_ffmpeg = 'I:/python/哔哩哔哩缓存转mp4工具/ffmpeg/bin/ffmpeg.exe'
    path_ffmpeg = 'D:/Python/哔哩哔哩缓存转换程序/ffmpeg/bin/ffmpeg.exe'
    font_style = ("微软雅黑", 16, "bold")
    path_entry_jsons = []
    path_audios = []
    path_videos = []
    percentage_of_progress = "0"

    def __init__(self):
        self.obj = None
        self.root = tk.Tk()
        self.root.minsize(800, 600)  # 窗口尺寸
        self.root.title("哔哩哔哩缓存转Mp4工具多线程")

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
        tk.Label(self.root, text="课程视频缓存文件夹:", font=self.font_style) \
            .place(x=100, y=150)  # 输入框，标记，按键
        tk.Entry(self.root, textvariable=self.path, width=90).place(x=100, y=200)  # 输入框绑定变量path
        tk.Button(self.root, text="目录选择", font=self.font_style, command=self.select_in_path) \
            .place(x=500, y=150)
        tk.Button(self.root, text="清除", font=self.font_style, command=self.clear_selected_folder) \
            .place(x=650, y=150)

        # 选择输出文件目录
        self.path2 = tk.StringVar()  # 变量path
        self.path2.set(self.out_path)
        tk.Label(self.root, text="输出目录:", font=self.font_style).place(x=100, y=250)  # 输入框，标记，按键
        tk.Entry(self.root, textvariable=self.path2, width=90).place(x=100, y=300)  # 输入框绑定变量path
        tk.Button(self.root, text="目录选择", font=self.font_style, command=self.select_out_path) \
            .place(x=600, y=250)

        self.start_convert = tk.Button(self.root, text="开始转换", font=self.font_style, command=self.convert_to_mp4)
        self.start_convert.place(x=600, y=350)

        tk.Label(self.root, text="转换进度:", font=self.font_style) \
            .place(x=100, y=450)  # 输入框，标记，按键

        self.canvas = tk.Canvas(self.root, width=465, height=22, bg="grey")
        self.canvas.place(x=100, y=500)

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
        self.path_video = self.path.get()

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
            self.start_convert.config(state = 'disabled')

            _thread.start_new_thread(self.convert, (self.path_ffmpeg, self.path_video, self.out_path))

    def convert(self, path_ffmpeg, in_path_list, out_path):
        all_text = []
        wrong_list = []
        print(in_path_list)
        for in_path in in_path_list.split(","):  # 遍历所有课程
            self.path_entry_jsons = []
            self.scan_path(in_path + "/", file_name="entry.json")
            for i, path_entry_json in enumerate(self.path_entry_jsons):
                try:
                    self.path_audios = []
                    self.path_videos = []
                    self.scan_path(path_entry_json.replace("entry.json", ""), file_name="audio.m4s")
                    self.scan_path(path_entry_json.replace("entry.json", ""), file_name="video.m4s")

                    # 生成输出目录和输出文件名
                    all_name, out_name = get_output_folder_name(path_entry_json.format(in_path))

                    tk.Canvas(self.root, width=700, height=30, bg="#f0f0f0").place(x=100, y=550)
                    tk.Label(self.root, text=all_name[:10]+" "*5+out_name[:15], font=self.font_style) \
                        .place(x=100, y=550)  # 输入框，标记，按键

                    if not os.path.exists(out_path + "/" + "/" + all_name):
                        os.makedirs(out_path + "/" + "/" + all_name)
                    file_name_out = "{}/{}/{}.mp4".format(out_path, all_name, out_name)
                    command_text = path_ffmpeg + ' -i {} -i {} -c:v copy -strict experimental {} -n' \
                        .format(self.path_videos[0], self.path_audios[0], file_name_out)
                    # os.system(command_text)
                    all_text.append(command_text)
                except:
                    wrong_list.append(path_entry_json)
        num = 0
        while num < len(self.path_entry_jsons):
            fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
            self.canvas.coords(fill_line, (0, 0, 500 * num / len(self.path_entry_jsons), 60))

            text_progress_statement = "{:4.2f}%    {}/{}".format(100 * (num + 1) / len(self.path_entry_jsons),
                                                                 (num + 1), len(self.path_entry_jsons))
            tk.Label(self.root, text=text_progress_statement, font=self.font_style) \
                .place(x=230, y=450)  # 输入框，标记，按键
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_1 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_1.start()
                num += 1
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_2 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_2.start()
                num += 1
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_3 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_3.start()
                thread_read_3.join()
                num += 1
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_4 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_4.start()
                num += 1
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_5 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_5.start()
                num += 1
            if num < len(self.path_entry_jsons):
                # 创建线程
                thread_read_6 = threading.Thread(target=os.system, args=(all_text[num],))
                # 启动线程
                thread_read_6.start()
                thread_read_6.join()
                num += 1
            if num - 5 < len(self.path_entry_jsons):
                thread_read_1.join()
            if num - 4 < len(self.path_entry_jsons):
                thread_read_2.join()
            if num - 3 < len(self.path_entry_jsons):
                thread_read_3.join()
            if num - 2 < len(self.path_entry_jsons):
                thread_read_4.join()
            if num - 1 < len(self.path_entry_jsons):
                thread_read_5.join()
            if num < len(self.path_entry_jsons):
                thread_read_6.join()
            print(num)
        print("转换失败列表：", wrong_list)
        tk.messagebox.showinfo(title='提示', message='转换完成')
        self.start_convert.config(state='normal')
        self.clear_selected_folder()

    def pick(self, obj, file_name):
        try:
            if obj[-len(file_name):] == file_name:
                if file_name == "audio.m4s":
                    if obj not in self.path_audios:
                        self.path_audios.append(obj)
                elif file_name == "video.m4s":
                    if obj not in self.path_videos:
                        self.path_videos.append(obj)
                elif file_name == "entry.json":
                    if obj not in self.path_entry_jsons:
                        self.path_entry_jsons.append(obj)
        except:
            return None

    def scan_path(self, path, file_name="entry.json"):
        print(path)
        for obj in os.listdir(path):
            if os.path.isfile(path + obj):
                self.pick(path + obj, file_name)
            elif os.path.isdir(path + obj):
                self.scan_path(path + obj + "/", file_name)


if __name__ == '__main__':
    GUI()