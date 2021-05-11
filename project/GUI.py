import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
import subprocess
import os
import io
import load_model_test
import string
import sys
sys.path.append('D:/CODE/python/project/load_model_test.py')


window = tk.Tk()
window.title('GUI')
window['bg'] = 'black'
align_mode = 'nsew'
pad = 5


def load_pic():
    pic_path = fd.askopenfilenames(initialdir="D:/", title="Select file",
                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    pic_path = str(pic_path)
    pic_path = pic_path.strip('(').strip(')').strip(',').strip("'")
    # print(pic_path)
    f = open('path.txt', 'w+')
    f.write(pic_path)
    # return pic_path


# def button_event():
    # if myentry.get() != '':
    #bt3['text'] = myentry.get()
    # print(myentry.get())
    #    f = open('D:/CODE/python/log.txt', 'r')
    #   if myentry.get() == f.read():


def layout(obj, cols=1, rows=1):
    def method(trg, col, row):

        for c in range(cols):
            trg.columnconfigure(c, weight=1)

        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj) == list:
        [method(trg, cols, rows) for trg in obj]
    else:
        trg = obj
        method(trg, cols, rows)


div_size = 200
img_size = div_size * 2
div1 = tk.Frame(window, width=img_size, height=img_size, bg='blue')
div2 = tk.Frame(window, width=div_size, height=div_size, bg='green')
div3 = tk.Frame(window, width=div_size, height=div_size, bg='orange')
#div4 = tk.Frame(window, width=div_size, height=div_size, bg='red')

window.update()
win_size = min(window.winfo_width(), window.winfo_height())
# print(win_size)

div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=2, sticky=align_mode)
#div4.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)
div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)

load_pic()
f = open('D:/CODE/python/path.txt', 'r')
get_path = f.read()
im = Image.open(get_path)
imTK = ImageTk.PhotoImage(im, im.resize((img_size, img_size)))

image_main = tk.Label(div1, image=imTK)
image_main['height'] = img_size
image_main['width'] = img_size
image_main.grid(column=0, row=0, sticky=align_mode)
image_main.pack(side="bottom", fill="both", expand="yes")
load_model_test.model()


def callback():
    load_pic()
    f = open('D:/CODE/python/path.txt', 'r')
    get_path = f.read()
    img2 = ImageTk.PhotoImage(Image.open(get_path))
    image_main.configure(image=img2)
    image_main.image = img2
    load_model_test.model()


lbl_title1 = tk.Label(div3, text='text', bg='orange',
                      fg='white', font=('microsoft yahei', 20))
lbl_title1.grid(column=1, row=1, sticky=align_mode)

mylabel = tk.Label(div3, text='Answer:', bg='orange',
                   fg='white', font=('microsoft yahei', 15))
mylabel.grid(column=0, row=0, sticky=align_mode)

myentry = tk.Entry(div3)
myentry.grid(column=1, row=0, padx=5, pady=10, ipady=3, sticky=align_mode)


def btn_show_pre():
    if myentry.get() != '':
        f = open('D:/CODE/python/log.txt', 'r')
        pre_sol = f.read()
        pre_sol = pre_sol.lower()

        myentry_ans = myentry.get()
        myentry_ans = myentry_ans.lower()

        # lbl_title1.config(text=pre_sol)
        # print(myentry_ans)
        if pre_sol == myentry_ans:
            lbl_title1.config(text='Correct')
        else:
            lbl_title1.config(text='Error! answer is {}'.format(pre_sol))
    '''f = open('D:/CODE/python/log.txt', 'r')
    pre_sol = f.read()
    lbl_title1.config(text=pre_sol)
    # return f.read()'''


#bt1 = tk.Button(div2, text='選擇圖片', bg='green', fg='white')
bt1 = tk.Button(div2, text='change photo', bg='green',
                fg='white', font=('microsoft yahei', 15))
bt2 = tk.Button(div2, text='submit', bg='green',
                fg='white', font=('microsoft yahei', 15))
#bt3 = tk.Button(div3, text='submit', command=button_event)
#bt3.configure(font=('microsoft yahei', 10))

bt1.grid(column=0, row=0, sticky=align_mode)
bt2.grid(column=0, row=1, sticky=align_mode)
#bt3.grid(column=2, row=0, sticky=align_mode)

bt1['command'] = callback
bt2['command'] = btn_show_pre

layout(window, cols=2, rows=2)
layout(div1)
layout(window, cols=2, rows=2)
layout([div1, div2, div3])

window.mainloop()
