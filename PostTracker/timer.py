from threading import *

def hello():
    print("hello, world")

# Create thread
t = Timer(3, hello)

# Start thread after 10 thread
t.start()


#
# import threading
#
# class MyThread (threading.Thread):
#
#     def __init__(self,x):
#         self.__x = x
#         threading.Thread.__init__(self)
#
#     def run (self):
#         print(str(self.__x))
#
# for x in range(100):
#     MyThread(x).start()
