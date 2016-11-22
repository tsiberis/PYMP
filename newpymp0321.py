#!/usr/bin/env python

'''
This is an attempt to rewrite the PyMP (Pygame's Music Player) program.
Started coding at 11/1/2008 and finished at 12/10/2008.

Here I'm using the Tk UI so I don't have to reinvent the wheel every time.
Technically it's still python and pygame. Works 4 both Linux & Windowz.

Guys, test yourselves for testicular cancer every now or so...

Version 0.3.1:
Some minor changes.

Version 0.3.1.1:
Again some changes. I don't have windows@home so...

Version 0.3.1.2:
...

Version 0.3.2:
mp3's are playable in windows too... I didn't know that.

Version 0.3.2.1:
Two tiny changes.
'''

#-------------------Imports-------------------
import pygame.mixer
import pygame.cdrom
from Tkinter import *
from os import path, listdir, getcwdu, chdir
from sys import platform
from locale import getdefaultlocale, setlocale, LC_ALL

#-------------------Constants-------------------
VERSION = '0.3.2.1'
PLATFORM = platform
DEFAULTLOCALE = getdefaultlocale()
FONT = 'Times'
FIRSTDIR = getcwdu()
SIZE = '8'
if PLATFORM == 'win32':
    SLASH = '\\'
else:
    SLASH = '/'

#-------------------Classes-------------------
class Player:
    def __init__(self,master):
        self.master = master
        self.listbox = Listbox(master, selectmode=SINGLE, bg='white', font=(FONT,SIZE))
        self.yscroll = Scrollbar(master, command=self.listbox.yview, orient=VERTICAL)
        self.xscroll = Scrollbar(master, command=self.listbox.xview, orient=HORIZONTAL)
        self.listbox.configure(xscrollcommand=self.xscroll.set, yscrollcommand=self.yscroll.set)
        self.listbox.bind('<Double-1>',self.handle_double_click_event)
        self.listbox.place(x=0, y=0, width=142, height=202)
        self.xscroll.place(x=0, y=200, height=17, width=157)
        self.yscroll.place(x=140, y=0, height=200, width=17)

        self.V = StringVar()
        self.label0 = Label(master, anchor='e', textvariable=self.V, font=(FONT,SIZE))
        self.label0.place(x=0, y=219, width=477, height=17)

        self.labelframe = Frame(master, bd=2, relief='groove')
        self.labelframe.place(x=0, y=217, width=477, height=2)

        self.R1 = IntVar()
        self.radio1frame = Frame(master, bd=2, relief='groove')
        self.radio1 = Radiobutton(master, text='8000', value=8000, variable=self.R1, font=(FONT,SIZE))
        self.radio2 = Radiobutton(master, text='11025', value=11025, variable=self.R1, font=(FONT,SIZE))
        self.radio3 = Radiobutton(master, text='22050', value=22050, variable=self.R1, font=(FONT,SIZE))
        self.radio4 = Radiobutton(master, text='32000', value=32000, variable=self.R1, font=(FONT,SIZE))
        self.radio5 = Radiobutton(master, text='44100', value=44100, variable=self.R1, font=(FONT,SIZE))
        self.radio6 = Radiobutton(master, text='48000', value=48000, variable=self.R1, font=(FONT,SIZE))
        self.label1 = Label(master, text='Sampling Rate', font=(FONT,SIZE))
        self.radio1frame.place(x=167, y=10, width=100, height=155)
        self.label1.place(in_=self.radio1frame, x=1, y=0)
        self.radio1.place(in_=self.radio1frame, x=5, y=20)
        self.radio2.place(in_=self.radio1frame, x=5, y=40)
        self.radio3.place(in_=self.radio1frame, x=5, y=60)
        self.radio4.place(in_=self.radio1frame, x=5, y=80)
        self.radio5.place(in_=self.radio1frame, x=5, y=100)
        self.radio6.place(in_=self.radio1frame, x=5, y=120)
        self.radio5.select()

        self.R2 = IntVar()
        self.radio2frame = Frame(master, bd=2, relief='groove')
        self.radio7 = Radiobutton(master, text=' 8', value=8, variable=self.R2, font=(FONT,SIZE))
        self.radio8 = Radiobutton(master, text='-16', value=-16, variable=self.R2, font=(FONT,SIZE))
        self.label2 = Label(master, text='Sample Size', font=(FONT,SIZE))
        self.radio2frame.place(x=277, y=10, width=90, height=75)
        self.label2.place(in_=self.radio2frame, x=1, y=0)
        self.radio7.place(in_=self.radio2frame, x=5, y=20)
        self.radio8.place(in_=self.radio2frame, x=5, y=40)
        self.radio8.select()

        self.R3 = IntVar()
        self.radio3frame = Frame(master, bd=2, relief='groove')
        self.radio9 = Radiobutton(master, text='No', value=1, variable=self.R3, font=(FONT,SIZE))
        self.radio10 = Radiobutton(master, text='Yes', value=2, variable=self.R3, font=(FONT,SIZE))
        self.label3 = Label(master, text='Stereo', font=(FONT,SIZE))
        self.radio3frame.place(x=277, y=95, width=90, height=75)
        self.label3.place(in_=self.radio3frame, x=1, y=0)
        self.radio9.place(in_=self.radio3frame, x=5, y=20)
        self.radio10.place(in_=self.radio3frame, x=5, y=40)
        self.radio10.select()

        self.R4 = IntVar()
        self.radio4frame = Frame(master, bd=2, relief='groove')
        self.radio11 = Radiobutton(master, text='512', value=512, variable=self.R4, font=(FONT,SIZE))
        self.radio12 = Radiobutton(master, text='1024', value=1024, variable=self.R4, font=(FONT,SIZE))
        self.radio13 = Radiobutton(master, text='2048', value=2048, variable=self.R4, font=(FONT,SIZE))
        self.radio14 = Radiobutton(master, text='3072', value=3072, variable=self.R4, font=(FONT,SIZE))
        self.radio15 = Radiobutton(master, text='4096', value=4096, variable=self.R4, font=(FONT,SIZE))
        self.radio16 = Radiobutton(master, text='5120', value=4800, variable=self.R4, font=(FONT,SIZE))
        self.label4 = Label(master, text='Buffer Size', font=(FONT,SIZE))
        self.radio4frame.place(x=377, y=10, width=90, height=155)
        self.label4.place(in_=self.radio4frame, x=1, y=0)
        self.radio11.place(in_=self.radio4frame, x=5, y=20)
        self.radio12.place(in_=self.radio4frame, x=5, y=40)
        self.radio13.place(in_=self.radio4frame, x=5, y=60)
        self.radio14.place(in_=self.radio4frame, x=5, y=80)
        self.radio15.place(in_=self.radio4frame, x=5, y=100)
        self.radio16.place(in_=self.radio4frame, x=5, y=120)
        self.radio15.select()

        self.buttonframe = Frame(master)
        self.b1 = Button(master, text='Stop Music', command=self.stop_music, font=(FONT,SIZE))
        self.b2 = Button(master, text='Change Mixer', command=self.apply_changes, font=(FONT,SIZE))
        self.b3 = Button(master, text='About PyMP', command=self.about, font=(FONT,SIZE))
        self.buttonframe.place(x=168, y=180, width=300, height=30)
        self.b1.place(in_=self.buttonframe, x=0, y=0, width=95, height=30)
        self.b2.place(in_=self.buttonframe, x=105, y=0, width=95, height=30)
        self.b3.place(in_=self.buttonframe, x=210, y=0, width=95, height=30)

        self.gcwd = getcwdu()
        self.V.set(self.gcwd)
        if PLATFORM == 'win32':
            self.L = []
            self.get_drives()
        self.create_dir()

    def create_dir(self):
        self.listbox.delete(0, END)

        self.folderlist = []
        self.filelist = []

        self._listdir = listdir(u'.')
        self._listdir.sort()

        for i in self._listdir:
            if i[0] != '.' and path.isdir(self.gcwd +  SLASH + i):
                self.folderlist.append(i)
            elif i[-4:].upper() == '.WAV'\
                 or i[-4:].upper() == '.MP3'\
                 or (i[-4:].upper() == '.CDA' and PLATFORM == 'win32')\
                 or i[-4:].upper() == '.MID'\
                 or i[-4:].upper() == '.OGG' and not self.is_ogg_video(i)\
                 or i[-3:].upper() == '.XM':
                     self.filelist.append(i)
        if not self.gcwd == SLASH:
            self.listbox.insert(END, SLASH)
        for x in self.folderlist:
            self.listbox.insert(END, SLASH + x)
        for x in self.filelist:
            self.listbox.insert(END, x)

    def is_ogg_video(self,_file):
        returned_value = 0
        opened_file = open(_file)
        first_line = opened_file.readline()
        if 'theora' in first_line:
            returned_value = 1
        opened_file.close()
        return returned_value

    def find_drives(self):
        self.L = []
        for i in range(ord('a'), ord('z') + 1):
            drive = chr(i).upper() + ':'
            if path.exists(drive):
                self.L.append(drive)
        self.L.sort()
        return self.L

    def get_drives(self):
        self.drive_list = []
        number_of_drives = pygame.cdrom.get_count()
        for x in range(number_of_drives):
            drive = pygame.cdrom.CD(x)
            drive_name = drive.get_name()
            self.drive_list.append((x, drive_name))

    def quit_drives(self):
        self.stop_drives()
        for x in self.drive_list:
            if pygame.cdrom.CD(x[0]).get_init():
                pygame.cdrom.CD(x[0]).quit()

    def stop_drives(self):
        for x in self.drive_list:
            if pygame.cdrom.CD(x[0]).get_init():
                if pygame.cdrom.CD(x[0]).get_busy():
                    pygame.cdrom.CD(x[0]).stop()

    def a_drive_is_busy(self):
        a = 0
        for x in self.drive_list:
            if pygame.cdrom.CD(x[0]).get_init():
                if pygame.cdrom.CD(x[0]).get_busy():
                    a = 1
                    break
        return a

    def play_music(self,name):
        a = path.split(name)
        b = path.splitdrive(name)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        elif PLATFORM == 'win32' and self.a_drive_is_busy():
            self.stop_drives()

        if name[-4:].upper() == '.CDA':
            drive = b[0] + SLASH

            for x in self.drive_list:
                if drive == x[1]:
                    drive_id = x[0]

            track_list = listdir(u'.')
            track_number = track_list.index(a[1])

            self.pcc = pygame.cdrom.CD(drive_id)
            self.pcc.init()

            try:
                self.pcc.play(track_number)
                self.V.set('loaded ... '+a[1])
            except RuntimeError:
                self.V.set('could not load ...')

        else:

            try:
                pygame.mixer.music.load(name.encode(DEFAULTLOCALE[1]))
                pygame.mixer.music.play()
                self.V.set('loaded ... '+a[1])
            except RuntimeError:
                self.V.set('could not load ...')

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.V.set('music stopped ...')
        elif PLATFORM == 'win32' and self.a_drive_is_busy():
            self.stop_drives()
            self.V.set('music stopped ...')
        else: self.V.set('trying to stop ...')

    def about(self):
        self.stop_music()
        pygame.mixer.quit()
        self.R1.set('44100')
        self.R2.set('-16')
        self.R3.set('2')
        self.R4.set('4096')
        pygame.mixer.init(self.R1.get(),self.R2.get(),self.R3.get(),self.R4.get())
        self.play_music(path.join(FIRSTDIR,'GODREST.MID'))

        self.msg = 0
        self.opened_file = open(path.join(FIRSTDIR,'info.txt'),'r').readlines()

        self.top = Toplevel(self.master)
        self.top.title('About PyMP')
        self.top.resizable(width=FALSE, height=FALSE)
        self.top.geometry("200x200+238+118")
        self.top.focus()

        self.M = StringVar()
        self.mlabel = Label(self.top, textvariable=self.M, font=(FONT,SIZE))
        self.mlabel.place(x=0, y=5, width=200, height=180)
        b1 = Button(self.top, text='Next', command=self._msg, font=(FONT,SIZE))
        b1.place(x=10, y=170, width=80, height=25)
        b2 = Button(self.top, text='Ok', command=self.top_destroy, font=(FONT,SIZE))
        b2.place(x=110, y=170, width=80, height=25)
        b1.invoke()

    def _msg(self):
        a = self.opened_file[self.msg]
        text = ''
        for string in a:
            if string == '^':
                text += '\n'
            elif string == '%':
                self.msg = -1
            else:
                text += string
        self.M.set(text)
        self.msg += 1

    def top_destroy(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.V.set('music stopped ...')
        self.top.destroy()

    def _chdir(self,_dir):
        chdir(_dir)
        self.gcwd = getcwdu()
        self.create_dir()

    def handle_double_click_event(self,event):
        index = event.widget.nearest(event.y)

        filename = event.widget.get(index)
        if PLATFORM == 'win32':
            if filename == SLASH:
                a = path.split(self.gcwd)
                if a[1] != '':
                    self._chdir(a[0])
                    self.V.set(self.gcwd)
                elif a[1] == '':
                    self.listbox.delete(0, END)
                    self.find_drives()
                    for x in self.L:
                        self.listbox.insert(END, x)
                    self.V.set('My Computer')
                return
            elif filename in self.L:
                self._chdir(filename)
                self.V.set(self.gcwd)
                return
        else:
            if filename == SLASH:
                a = path.split(self.gcwd)
                if a[1] != '':
                    self._chdir(a[0])
                    self.V.set(self.gcwd)
                return

        _dirname = path.normpath(self.gcwd + SLASH + filename)
        if path.isdir(_dirname):
            try:
                self._chdir(_dirname)
                self.V.set(_dirname)
            except OSError:
                a = path.split(self.gcwd)
                self.V.set('access denied ...')
                self._chdir(a[0])
        elif path.isfile(_dirname):
            self.play_music(_dirname)

    def mixer_quit_and_init(self):
        pygame.mixer.quit()
        pygame.mixer.init(self.R1.get(),self.R2.get(),self.R3.get(),self.R4.get())

    def apply_changes(self):
        self.stop_music()
        self.mixer_quit_and_init()
        self.V.set('mixer changed ...')

#-------------------Functions-------------------
def main():
    if DEFAULTLOCALE == (None, None):
        setlocale(LC_ALL, '')
    pygame.mixer.init(44100,-16,2,4096)
    if PLATFORM == 'win32':
        pygame.cdrom.init()

    root = Tk()
    root.geometry("477x236+100+100")
    root.resizable(width=FALSE, height=FALSE)
    root.title('PyMP v' + VERSION)

    player = Player(root)
    root.mainloop()
    pygame.mixer.quit()
    if PLATFORM == 'win32':
        player.quit_drives()
        pygame.cdrom.quit()
    root.quit()

if __name__ == "__main__": main()
