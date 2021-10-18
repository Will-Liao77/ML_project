import random
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as fd
import subprocess
import os
import io
import load_model_test
import string
import sys
import tempfile
from pygame import mixer
from gtts import gTTS

dot = 1
# sys.path.append('D:/CODE/python/project/load_model_test.py')

window = tk.Tk()
window.title('被動式英文學習平台')
# window.geometry('600x500')
# window['bg'] = 'black'
align_mode = 'nsew'
pad = 5


def speak(sentence, lang):
    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=sentence, lang=lang)
        tts.save('{}.mp3'.format(fp.name))
        mixer.init()
        mixer.music.load('{}.mp3'.format(fp.name))
        mixer.music.play(1)


if dot == 1:
    speak('Welcome to learning english system', 'en')
    dot = -1


def load_pic():
    pic_path = fd.askopenfilenames(initialdir="D:/", title="Select file",
                                   filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    pic_path = str(pic_path)
    pic_path = pic_path.strip('(').strip(')').strip(',').strip("'")
    # print(pic_path)
    f = open('./path.txt', 'w+')
    f.write(pic_path)
    # return pic_path

# def button_event():
    # if myentry.get() != '':
    # bt3['text'] = myentry.get()
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
div1 = tk.Frame(window, width=img_size, height=img_size, bg='#C9D1D9')
div2 = tk.Frame(window, width=div_size, height=div_size, bg='#1B98E0')
div3 = tk.Frame(window, width=div_size, height=div_size, bg='#08415C')
# div4 = tk.Frame(window, width=div_size, height=div_size, bg='red')

window.update()
win_size = min(window.winfo_width(), window.winfo_height())
# print(win_size)

div1.grid(column=0, row=0, padx=pad, pady=pad,
          rowspan=2, sticky=align_mode)
# div4.grid(column=0, row=1, padx=pad, pady=pad, sticky=align_mode)
div2.grid(column=1, row=0, padx=pad, pady=pad, sticky=align_mode)
div3.grid(column=1, row=1, padx=pad, pady=pad, sticky=align_mode)

load_pic()
f = open('./path.txt', 'r')
get_path = f.read()
im = Image.open(get_path)
imTK = ImageTk.PhotoImage(im, im.resize((img_size, img_size)))

image_main = tk.Label(div1, image=imTK)
image_main['height'] = img_size
image_main['width'] = img_size
image_main.grid(column=0, row=0, sticky=align_mode)
image_main.pack(side="bottom", fill="both", expand="yes")

load_model_test.model()

count = 0

lbl_question = tk.Label(div3, text='Question:', bg='#08415C',
                        fg='white', font=('microsoft yahei', 15))
lbl_question.grid(column=0, row=0, sticky=align_mode)

lbl_question_text = tk.Label(div3, text='test123', bg='#08415C',
                             fg='white', font=('microsoft yahei', 15))
lbl_question_text.grid(column=1, row=0, sticky=align_mode)

lbl_title1 = tk.Label(div3, text='Please Input Answer!', bg='#08415C',
                      fg='white', font=('microsoft yahei', 15))
lbl_title1.grid(column=1, row=2, sticky=align_mode)

lbl_count = tk.Label(div3, text=count, bg='#08415C',
                     fg='white', font=('microsoft yahei', 20))
lbl_count.grid(column=0, row=2, sticky=align_mode)

mylabel = tk.Label(div3, text='Answer:', bg='#08415C',
                   fg='white', font=('microsoft yahei', 15))
mylabel.grid(column=0, row=1, sticky=align_mode)

myentry = tk.Entry(div3)
myentry.grid(column=1, row=1, padx=5, pady=10, ipady=3, sticky=align_mode)


def change_question():
    f = open('./log.txt', 'r')
    pre_sol = f.read()
    lst = []
    pre_hidden = 1
    for i in pre_sol:
        lst.append(i)
    if len(lst) <= 3:
        hidden = random.randint(1, len(lst)-1)
        lst.remove(lst[hidden])
        lst.insert(hidden, "_")
        Lis_to_Str = "".join(lst)
        lst.clear()
        lbl_question_text.config(text=Lis_to_Str)
    else:
        hidden = random.randint(pre_hidden + 1, len(lst)-1)
        lst.remove(lst[hidden])
        lst.remove(lst[pre_hidden])
        lst.insert(hidden-1, "_")
        lst.insert(pre_hidden, "_")
        Lis_to_Str = "".join(lst)
        lst.clear()
        lbl_question_text.config(text=Lis_to_Str)


change_question()


def callback():
    load_pic()
    f = open('./path.txt', 'r')
    get_path = f.read()
    img2 = ImageTk.PhotoImage(Image.open(get_path))
    image_main.configure(image=img2)
    image_main.image = img2
    load_model_test.model()
    change_question()
    myentry.delete('0', 'end')
    lbl_title1.config(text="changed")


def btn_show_pre():
    global count

    if myentry.get() != '':
        f = open('./log.txt', 'r')
        pre_sol = f.read()
        pre_sol = pre_sol.lower()
        myentry_ans = myentry.get()
        myentry_ans = myentry_ans.lower()

        # lbl_title1.config(text=pre_sol)
        # print(myentry_ans)
        if pre_sol == myentry_ans:
            lbl_title1.config(text='Correct')
            count = count + 1
            lbl_count.config(text=count)
        else:
            lbl_title1.config(text='Error!')
            if count == 0:
                lbl_count.config(text=count)
            else:
                count = count - 1
                lbl_count.config(text=count)

    '''f = open('D:/CODE/python/log.txt', 'r')
    pre_sol = f.read()
    lbl_title1.config(text=pre_sol)
    # return f.read()'''


def show_ans():
    f = open('./log.txt', 'r')
    pre_sol = f.read()
    lbl_title1.config(text='answer is {}'.format(pre_sol))
    speak(pre_sol, 'en')


def restart():
    global count
    count = 0
    lbl_count.config(text=count)
    lbl_title1.config(text="restart")
    myentry.delete('0', 'end')


# bt1 = tk.Button(div2, text='選擇圖片', bg='green', fg='white')
bt1 = tk.Button(div2, text='change photo', bg='#1B98E0',
                fg='white', font=('microsoft yahei', 15))
bt2 = tk.Button(div2, text='submit', bg='#1B98E0',
                fg='white', font=('microsoft yahei', 15))
bt3 = tk.Button(div2, text='restart', bg='#1B98E0',
                fg='white', font=('microsoft yahei', 15))
bt4 = tk.Button(div2, text='show answer', bg='#1B98E0',
                fg='white', font=('microsoft yahei', 15))

bt1.grid(column=0, row=0, sticky=align_mode)
bt2.grid(column=1, row=0, sticky=align_mode)
bt3.grid(column=2, row=0, sticky=align_mode)
bt4.grid(column=3, row=0, sticky=align_mode)

bt1['command'] = callback
bt2['command'] = btn_show_pre
bt3['command'] = restart
bt4['command'] = show_ans

# layout(window, cols=2, rows=2)
# layout(div1)
layout(window, cols=2, rows=2)
layout([div1, div2, div3])

window.mainloop()
