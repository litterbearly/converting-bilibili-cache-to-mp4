import threading
import time
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import json


# 替换不合法的字符
def replace_illegal_characters(str_name):  # 替换不合法的字符
    list_illegal_characters = [" ", "<", ">", "?", "/", "\\", ":", "*", "|", "&", "____", "___", "__"]  # 不合法字符列表
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
    input_path = ''
    out_path = ''
    path_ffmpeg = ''
    font_style = ("微软雅黑", 16, "bold")
    all_path_entry_json = []
    path_audios = []
    path_videos = []

    # 向窗口添加元素
    def __init__(self):
        self.obj = None
        self.root = tk.Tk()
        self.root.minsize(800, 600)  # 窗口尺寸
        self.root.title("哔哩哔哩Cache缓存转Mp4工具多线程")

        # 从conf.json文件读取配置
        tk.Button(self.root, text="读取conf", font=self.font_style, command=self.read_conf_json) \
            .place(x=500, y=10)

        # 将配置写入conf.json文件
        tk.Button(self.root, text="写入conf", font=self.font_style, command=self.write_conf_json) \
            .place(x=650, y=10)

        # 选择ffmpeg.exe文件路径
        self.path0 = tk.StringVar()  # 变量path
        self.path0.set(self.path_ffmpeg)
        tk.Label(self.root, text="ffmpeg.exe文件路径:", font=self.font_style) \
            .place(x=95, y=90)  # 输入框，标记，按键
        tk.Button(self.root, text="文件选择", font=self.font_style, command=self.select_ffmpeg_path) \
            .place(x=500, y=80)
        tk.Entry(self.root, textvariable=self.path0, width=90).place(x=100, y=140)  # 输入框绑定变量path

        # 选择缓存文件目录
        self.path1 = tk.StringVar()  # 变量path
        self.path1.set(self.input_path)
        tk.Label(self.root, text="cache缓存文件夹:", font=self.font_style) \
            .place(x=100, y=185)  # 输入框，标记，按键
        tk.Button(self.root, text="选择目录", font=self.font_style, command=self.select_in_path) \
            .place(x=500, y=180)
        tk.Button(self.root, text="清除", font=self.font_style, command=self.clear_selected_in_folder) \
            .place(x=650, y=180)
        tk.Entry(self.root, textvariable=self.path1, width=90)\
            .place(x=100, y=240)  # 输入框绑定变量path

        # 选择输出文件目录
        self.path2 = tk.StringVar()  # 变量path
        self.path2.set(self.out_path)
        tk.Label(self.root, text="输出目录:", font=self.font_style)\
            .place(x=100, y=285)  # 输入框，标记，按键
        tk.Button(self.root, text="选择目录", font=self.font_style, command=self.select_out_path) \
            .place(x=500, y=280)
        tk.Button(self.root, text="清除", font=self.font_style, command=self.clear_selected_out_folder) \
            .place(x=650, y=280)
        tk.Entry(self.root, textvariable=self.path2, width=90)\
            .place(x=100, y=340)  # 输入框绑定变量path

        self.start_convert = tk.Button(self.root, text="开始转换", font=self.font_style, command=self.convert_to_mp4)
        self.start_convert.place(x=650, y=400)

        tk.Label(self.root, text="转换进度:", font=self.font_style) \
            .place(x=100, y=450)  # 输入框，标记，按键

        self.canvas = tk.Canvas(self.root, width=465, height=22, bg="grey")
        self.canvas.place(x=100, y=500)

        self.root.mainloop()

    # 从conf.json文件提取默认配置
    def read_conf_json(self, ):
        json_file = open("conf.json", "r", encoding="UTF-8")
        dict_json = json.load(json_file)
        json_file.close()

        if not dict_json['path_ffmpeg']:
            tkinter.messagebox.showwarning('提示', 'conf.json中无ffmpeg配置，请手动选择。')
            return None
        self.path0.set(dict_json['path_ffmpeg'])
        self.path_ffmpeg = self.path0.get()

        self.path1.set(dict_json['input_path'])
        self.input_path = self.path1.get()

        self.path2.set(dict_json['out_path'])
        self.out_path = self.path2.get()

        self.root.update()  # 刷新页面

    # 将当前配置覆盖写入到conf.json文件
    def write_conf_json(self, ):
        if self.path_ffmpeg:
            json_file = open("conf.json", "w", encoding="UTF-8")
            current_conf = {"path_ffmpeg": str(self.path_ffmpeg),
                            "input_path": str(self.input_path),
                            "out_path": str(self.out_path)
                            }
            json.dump(current_conf, json_file, ensure_ascii=False)  # ensure_ascii=False 不将字符转换为ascii码，即直接保存中文
            json_file.close()
        else:
            tkinter.messagebox.showwarning('警告', '未选择ffmpeg.exe文件')

    # 选择ffmpeg.exe路径
    def select_ffmpeg_path(self):  # ffmpeg路径选择
        # 选择文件path_接收文件地址
        path0_ = tkinter.filedialog.askopenfilename()
        self.path0.set(path0_)
        self.path_ffmpeg = self.path0.get()

    # 添加输入目录
    def select_in_path(self):  # 输入目录添加
        # 选择文件path_接收文件地址
        path_ = tkinter.filedialog.askdirectory()

        # path设置path_的值
        if not self.path1.get():
            self.path1.set(path_)
        else:
            self.path1.set(self.path1.get() + "," + path_)
        self.input_path = self.path1.get()

    # 清空已选择的输入文件夹
    def clear_selected_in_folder(self):
        self.path1.set("")
        self.input_path = ""

    # 输出目录选择
    def select_out_path(self):
        # 选择文件path_接收文件地址
        path2_ = tkinter.filedialog.askdirectory()
        # path设置path_的值
        self.path2.set(path2_)
        if "" != self.path2.get():
            self.out_path = self.path2.get()

    # 清空已选择的输入文件夹
    def clear_selected_out_folder(self):
        self.path2.set("")
        self.out_path = ""

    # 开始处理线程
    def convert_to_mp4(self):
        if not self.input_path:
            tkinter.messagebox.showwarning('警告', '请选择需要转换的缓存文件夹')
        elif not self.path_ffmpeg:
            tkinter.messagebox.showwarning('警告', '请选择ffmpeg.exe文件')
        elif not self.out_path:
            tkinter.messagebox.showwarning('警告', '请选择保存文件夹')
        else:
            self.start_convert.config(state='disabled')
            thread_read_convert = threading.Thread(target=self.convert,
                                                   args=(self.path_ffmpeg, self.input_path, self.out_path,))
            thread_read_convert.start()

    # 扫描和转换
    def convert(self, path_ffmpeg, in_path_list, out_path):
        start_time = time.time()
        all_command_text = []
        all_classes_name = []
        all_class_name = []

        wrong_list = []
        self.all_path_entry_json = []
        for in_path in in_path_list.split(","):  # 遍历所有课程
            self.scan_path(in_path + "/", file_name="entry.json")
        try:
            if not self.all_path_entry_json:
                raise LookupError("已选择的目录中查找不到entry.json文件")
        except LookupError as e:
            tkinter.messagebox.showwarning('警告', repr(e))
            self.start_convert.config(state='normal')
            return None
        if self.all_path_entry_json:
            for i, path_entry_json in enumerate(self.all_path_entry_json):
                try:
                    self.path_audios = []
                    self.path_videos = []
                    self.scan_path(path_entry_json.replace("entry.json", ""), file_name="audio.m4s")
                    self.scan_path(path_entry_json.replace("entry.json", ""), file_name="video.m4s")

                    # 当查找不到文件是报错 LookupError--"无效数据查询的基类"
                    if not self.path_audios or not self.path_videos:
                        raise LookupError("查找不到audio或video文件")
                    # 当查找不到文件是报错 LookupError--"无效数据查询的基类"
                    if len(self.path_audios) > 1 or len(self.path_videos) > 1:
                        raise LookupError("查找到多个audio或video文件")

                    # 生成输出目录和输出文件名
                    classes_name, class_name = get_output_folder_name(path_entry_json)

                    if not os.path.exists(out_path + "/" + classes_name):
                        os.makedirs(out_path + "/" + classes_name)
                    file_name_out = "{}/{}/{}.mp4".format(out_path, classes_name, class_name)
                    command_text = path_ffmpeg + ' -i {} -i {} -c:v copy -strict experimental {} -y' \
                        .format(self.path_videos[0], self.path_audios[0], file_name_out)

                    all_classes_name.append(classes_name)
                    all_class_name.append(class_name)
                    all_command_text.append(command_text)
                except LookupError as e:
                    print("引发异常：", repr(e))
                    wrong_list.append(path_entry_json)
            # print(sorted(set(all_classes_name), key=all_classes_name.index), "\n", all_class_name)
            # input()

        for num in range(len(all_command_text)//2):
            # 创建线程
            thread_read_1 = threading.Thread(target=os.system, args=(all_command_text[2*num],))
            thread_read_2 = threading.Thread(target=os.system, args=(all_command_text[2*num+1],))

            # 启动线程
            thread_read_1.start()
            thread_read_2.start()

            # 线程结束
            thread_read_1.join()
            thread_read_2.join()

            # 转换进度百分比展示
            text_progress_statement = "{:4.2f}%    {:2d}/{}". \
                format(100 * (2*(num+1)) / len(all_command_text), (2*(num+1)), len(all_command_text))
            tk.Label(self.root, text=text_progress_statement, font=self.font_style) \
                .place(x=400, y=450)  # 输入框，标记，按键

            # 转换进度条
            tk.Canvas(self.root, width=700, height=30, bg="#f0f0f0").place(x=100, y=550)  # 覆盖前一步进度条，使其与窗口底色相同
            fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")  # 生成当前步的进度条
            self.canvas.coords(fill_line, (0, 0, 500 * (2*(num+1)) / len(all_command_text), 60))

            # 当前转换文件名
            tk.Label(self.root,
                     text=all_classes_name[(2*num+1)][:10] + " " * 5 + all_class_name[(2*num+1)][:15],
                     font=self.font_style).place(x=100, y=550)  # 输入框，标记，按键
        if len(all_command_text) % 2:
            os.system(all_command_text[-1])
            # 转换进度百分比展示
            text_progress_statement = "{:4.2f}%    {}/{}". \
                format(100, len(all_command_text), len(all_command_text))
            tk.Label(self.root, text=text_progress_statement, font=self.font_style) \
                .place(x=400, y=450)  # 输入框，标记，按键

            # 转换进度条
            tk.Canvas(self.root, width=700, height=30, bg="#f0f0f0").place(x=100, y=550)  # 覆盖前一步进度条，使其与窗口底色相同
            fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")  # 生成当前步的进度条
            self.canvas.coords(fill_line, (0, 0, 500 * 1, 60))

            # 当前转换文件名
            tk.Label(self.root,
                     text=all_classes_name[-1][:10] + " " * 5 + all_class_name[-1][:15],
                     font=self.font_style).place(x=100, y=550)  # 输入框，标记，按键

        if wrong_list:
            print("查找audio或video文件失败列表：", wrong_list)
        end_time = time.time()
        print((end_time - start_time) / 60, " 分钟")
        tk.messagebox.showinfo(title='提示', message='转换完成')
        self.start_convert.config(state='normal')
        self.clear_selected_in_folder()
        self.clear_selected_out_folder()

    # 递归法查找对应名称的文件
    def scan_path(self, path, file_name="entry.json"):
        for obj in os.listdir(path):
            if os.path.isfile(path + obj):
                file = path + obj
                if file[-len(file_name):] == file_name:
                    if file_name == "audio.m4s":
                        if file not in self.path_audios:
                            self.path_audios.append(file)
                    if file_name == "video.m4s":
                        if file not in self.path_videos:
                            self.path_videos.append(file)
                    if file_name == "entry.json":
                        if file not in self.all_path_entry_json:
                            self.all_path_entry_json.append(file)
            elif os.path.isdir(path + obj):
                self.scan_path(path + obj + "/", file_name)


if __name__ == '__main__':
    GUI()
