import os

path_entry_jsons = []


def pick(obj):
    global path_entry_jsons
    try:
        if obj[-9:] == "video.m4s":
            path_required.append(obj)
    except:
        return None


def scan_path(ph):
    file_list = os.listdir(ph)
    for obj in file_list:
        if os.path.isfile(ph+obj):
            pick(ph+obj)
        elif os.path.isdir(ph+obj):
            scan_path(ph+obj+"\\")


if __name__ == "__main__":
    path = "F:\\python\\download\\16944429\\"
    scan_path(path)
    print(path_entry_jsons)