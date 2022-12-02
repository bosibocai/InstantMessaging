# coding:utf-8
# coding:utf-8
from tkinter import *
import tkinter as tk

class ScrollFrame(tk.Frame):
    # 滑动窗口
    def __init__(self, parent):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")  # place canvas on self
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)  # bind an event whenever the size of the canvas frame changes.

        self.viewPort.bind('<Enter>', self.onEnter)  # bind wheel events when the cursor enters the control
        self.viewPort.bind('<Leave>', self.onLeave)  # unbind wheel events when the cursorl leaves the control

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onEnter(self, event):
        self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)

    def onLeave(self, event):
        self.canvas.unbind_all("<MouseWheel>")


class Example(tk.Frame):
    # html页面展示
    def __init__(self, root, onlineUsers):

        tk.Frame.__init__(self, root)
        self.scrollFrame = ScrollFrame(self)

        for username, ip in onlineUsers.items():

            print(username, ip)

        self.scrollFrame.pack(side="top", fill="both", expand=True)

    def printMsg(self, msg):
        print(msg)

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master, bg='red')
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        # 创建组件
        self.btn01 = Button(self)
        self.btn01['text'] = '点击送花'
        self.btn01.pack()
        self.btn01['command'] = self.songhua
        # 创建一个退出按钮
        self.btnQuit = Button(self, text='退出', command=root.destroy)
        self.btnQuit.pack()

    def songhua(self):
        tk.messagebox.showinfo('送花', '送你99朵玫瑰花')


root = Tk()
# 设置长 宽 起始位置
root.geometry('1200x700+100+100')
root.title('即时通讯系统')
app = Application(master=root)

root.mainloop()

