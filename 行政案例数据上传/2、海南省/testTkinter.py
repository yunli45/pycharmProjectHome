from tkinter import *
import tkinter.messagebox
import time


root = Tk()
root.withdraw()
ss = time.time()
ans = tkinter.messagebox.askquestion("ceshi", "wenti ?")
print(ans)
ee = time.time()
print(type(ans))
print(ee -ss )
# print(time.strptime())