from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from PlayerFunctions import *


root = Tk()
root.title("Music")
root.iconbitmap("music-2-64.ico")
root.geometry("500x500")

#adding background image
bg = PhotoImage(file="bg3.png")
label1= Label(root,image = bg )
label1.place(x=0 , y= 0)



#Initialise Pygame mixer
pygame.mixer.init()


#Song Time Info
def play_time():
    #check for double timing
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() /1000

    #throw a temporary label to get data
    #slider_label.config(text = f'Slider:{int(my_slider.get())} and Song Pos : {int(current_time)}')

    #converting into time format
    converted_current_time = time.strftime('%H:%M:%S',time.gmtime(current_time))

    #get currently playing song
    current_song = song_box.curselection()

    song = song_box.get(current_song)

    song = f'C:/Users/parth/PycharmProjects/Tkinter/Music/{song}.mp3'

    #getting song length
    song_mut = MP3(song)

    global song_length
    song_length = song_mut.info.length

    #converting to Time Format
    converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed : {converted_song_length} ')

    elif paused :
        pass

    elif  int(my_slider.get()) == int(current_time):
        # update slider to position
        slider_posistion = int(song_length)

        my_slider.config(to=slider_posistion, value=int(current_time))
    else:
        # update slider to position
        slider_posistion = int(song_length)

        my_slider.config(to=slider_posistion, value=int(my_slider.get()))

        converted_current_time = time.strftime('%H:%M:%S', time.gmtime(int(my_slider.get())))

        status_bar.config(text=f'Time Elapsed : {converted_current_time} of {converted_song_length} ')

        #move this thing along by 1 sec
        next_time = int(my_slider.get()) + 1
        my_slider.config(value = next_time)

    #output time to status bar
    #status_bar.config(text=f'Time Elapsed : {converted_current_time} of {converted_song_length} ')

    #update slider position value to current song position
    #my_slider.config(value=int(current_time))



    #update time
    status_bar.after(1000,play_time)


#add song fucntion
def add_song():
    song = filedialog.askopenfilename(initialdir = 'Music/' , title = "Choose a song " , filetypes=(("mp3 files", "*.mp3"),))

    #replacing full path of song to just name
    song = song.replace("C:/Users/parth/PycharmProjects/Tkinter/Music/","")
    song = song.replace(".mp3","")

    song_box.insert(END , song)

#add many songs to playlist
def add_many_song():
    songs = filedialog.askopenfilenames(initialdir = 'Music/' , title = "Choose a song " , filetypes=(("mp3 files", "*.mp3"),))

    for song in songs:
        song = song.replace("C:/Users/parth/PycharmProjects/Tkinter/Music/", "")
        song = song.replace(".mp3", "")
        song_box.insert(END,song)


#play song function
def play():
    #set stopped var to false so song can play
    global stopped
    stopped = False
    # gets whatever is highlighted in the list box
    song = song_box.get(ACTIVE)
    song = f'C:/Users/parth/PycharmProjects/Tkinter/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops= 0)

    #call playtime fucntion to get time length of songs
    play_time()
    current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text=current_volume * 100)

    """#update slider to position
    slider_posistion = int(song_length)
    my_slider.config(to=slider_posistion , value = )
"""
#song stop function
global stopped
stopped = False
def stop():
    #reset slider and status bar
    status_bar.config(text= '')

    my_slider.config(value = 0)
    pygame.mixer.music.stop()
    #song_box.select_clear(ACTIVE)

    #set stop variable to True
    global stopped
    stopped = True
#create global pause variable
global paused
paused  = False


#Pause and unpause song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

#Play next song in Playlist
def next_song():
    #resetting slider and status bar
    status_bar.config(text='')

    my_slider.config(value=0)
    #get the current song tuple number
    next_one = song_box.curselection()  #query songbox for current song
    #add one to the current song number
    next_one= next_one[0]+1
    song = song_box.get(next_one)

    song = f'C:/Users/parth/PycharmProjects/Tkinter/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #move Active bar in Playlists
    song_box.select_clear(0,END)

    #activate new Song bar
    song_box.activate(next_one)

    #set active bar to next song
    song_box.selection_set(next_one, last = None )


def previous_song():
    # resetting slider and status bar
    status_bar.config(text='')

    my_slider.config(value=0)

    # get the current song tuple number
    prev_one = song_box.curselection()  # query songbox for current song
    # add one to the current song number
    prev_one = prev_one[0] - 1
    song = song_box.get(prev_one)

    song = f'C:/Users/parth/PycharmProjects/Tkinter/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # move Active bar in Playlists
    song_box.select_clear(0, END)

    # activate new Song bar
    song_box.activate(prev_one)

    # set active bar to next song
    song_box.selection_set(prev_one, last=None)


#delete a song():
def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()


#delete all songs
def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()

#Create slider fucntion
def slide(x):
    #slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
    song = song_box.get(ACTIVE)
    song = f'C:/Users/parth/PycharmProjects/Tkinter/Music/{song}.mp3'

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0 ,start = int(my_slider.get()))


#volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

    #get current vol
    #current_volume = pygame.mixer.music.get_volume()
    #slider_label.config(text = current_volume * 100)


#create Master frame
master_frame = Frame(root)
master_frame.pack(pady=20 )
label2 = Label(master_frame , image = bg)
label2.place(x=0 , y= 0)

#create Playlist BOX
song_box = Listbox(master_frame, bg = "black" ,bd = 30,fg = "cyan" , width = 60,selectbackground="gray",selectforeground= "black")
song_box.grid(row = 0 , column = 0)

#Define Player Control Butttons Images

back_btn_img = PhotoImage(file ='50pxButtons/Previous.png')
forward_btn_img = PhotoImage(file = '50pxButtons/Next.png')
play_btn_img = PhotoImage(file = '50pxButtons/Play.png')
pause_btn_img    = PhotoImage(file = '50pxButtons/Pause.png')
stop_btn_img     = PhotoImage(file = '50pxButtons/RESET.png')

#Create Player Control Frames
controls_frame =Frame(master_frame)
controls_frame.grid(row = 1,column = 0,pady=20)

#create volume frame
volume_frame = LabelFrame(master_frame , text = "Volume")
volume_frame.grid(row = 0 , column= 1,padx = 20)

#PLayer Control Buttons
back_btn = Button(controls_frame , image= back_btn_img, borderwidth=0,command= previous_song)
forward_btn =Button(controls_frame , image=forward_btn_img , borderwidth=0,command= next_song)
play_btn =Button(controls_frame , image=play_btn_img , borderwidth=0,command= play)
pause_btn =Button(controls_frame , image=pause_btn_img , borderwidth=0,command =lambda : pause(paused))
stop_btn =Button(controls_frame , image=stop_btn_img ,borderwidth=0,command= stop)

back_btn.grid(row= 0,column=0,padx= 10,pady=10)
forward_btn.grid(row= 0,column=1,padx= 10,pady=10)
play_btn.grid(row= 0,column=2,padx= 10,pady=10)
pause_btn.grid(row= 0,column=3,padx= 10,pady=10)
stop_btn.grid(row= 0,column=4,padx= 10,pady=10)

#create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs " , menu= add_song_menu)
add_song_menu.add_command(label="Add one song to Playlist" , command=add_song)

#add many songs to the list
add_song_menu.add_command(label="Add Many songs to Playlist" , command=add_many_song)


#create delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label= "Remove Songs " , menu = remove_song_menu)
remove_song_menu.add_command(label="Delete a song from Playlist ",command=delete_song )
remove_song_menu.add_command(label="Delete all songs from Playlist ",command=delete_all_songs)


#create a status bar
status_bar = Label(root , text='',bd=1 , relief = GROOVE ,anchor = E)
status_bar.pack(fill=X,side=BOTTOM,ipady=2 )


#creating slider
my_slider = ttk.Scale(master_frame , from_ =0 ,to = 100 , orient = HORIZONTAL, value = 0 , command= slide , length = 340)
my_slider.grid(row=2, column=0 ,pady = 10)

#create volume slider
volume_slider = ttk.Scale(volume_frame , from_ =0 ,to = 1 , orient = VERTICAL , value = 1 , command= volume , length = 125)
volume_slider.pack(pady=10)


#create Temporary SLider Label
#slider_label = Label(root,text = "0")
#slider_label.pack(pady=10)

root.mainloop()
