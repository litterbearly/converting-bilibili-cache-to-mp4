import cv2, threading

import time  # 引入time模块



def read_frame(cap):
    global frame, ret
    ret, frame = cap.read()
    cv2.waitKey(1000)


def bgr_to_gray(rgb):
    global gray
    gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(1000)


def gray_to_binary(gray):
    global binary
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)


frame = []
gray = []
binary = []
ret = False


cap = cv2.VideoCapture('video.mp4')


# 创建线程
thread_read = threading.Thread(target=read_frame, args=(cap,))
# 创建线程
thread_to_gray = threading.Thread(target=bgr_to_gray, args=(frame,))
# 启动线程
thread_read.start()

while cap.isOpened():
    # 等待线程结束
    thread_read.join()
    if ret:
        start = time.clock()
        # 创建线程
        thread_to_gray = threading.Thread(target=bgr_to_gray, args=(frame,))
        # 启动线程
        thread_to_gray.start()

        # 创建线程
        thread_read = threading.Thread(target=read_frame, args=(cap,))
        # 启动线程
        thread_read.start()
        thread_to_gray.join()


        # gray_to_binary(gray)
        end = time.clock()
        print('Running time: %s Seconds' % (end - start))  # 其中end-start就是程序运行的时间，bai单位是秒。
        cv2.imshow('a', gray)
        if cv2.waitKey(4) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
