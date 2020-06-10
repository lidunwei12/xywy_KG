# 开启多个线程，同时执行任务，有几个线程就执行几个任务

import threading
import time
import queue


class MyThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()


def worker():
    while not q.empty():
        item = q.get()  # 或得任务
        print('Processing : ', item)
        time.sleep(1)


def main():
    threads = []
    for task in range(100):
        q.put(task)
    for i in range(threadNum):  # 开启三个线程
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()


if __name__ == '__main__':
    time_start =time.time()
    q = queue.Queue()
    threadNum = 5
    main()
    print(time.time()-time_start)
