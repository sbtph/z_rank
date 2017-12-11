# coding: utf-8
import time
import os
import threading
import set_outdated_data

def spider1():
    while True:
        os.system("scrapy crawl smzdm")
        time.sleep(60)  # 1 minute

def spider2():
    while True:
        os.system("scrapy crawl update")
        time.sleep(60*2)  # 2 minutes

def clear():
    while True:
        set_outdated_data(1)  # 过期天数
        time.sleep(12*60*60) # 12 hours

threads = []
t1 = threading.Thread(target=spider1)
threads.append(t1)
t2 = threading.Thread(target=spider2)
threads.append(t2)
t3 = threading.Thread(target=clear)
threads.append(t3)

if __name__ == '__main__':
    try:
        for t in threads:
            t.setDaemon(True)
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        print ("error:")
        print (e)
