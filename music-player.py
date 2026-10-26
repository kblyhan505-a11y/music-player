import glob  #klasörde ki dosyaları listelemek için kullanıcaz 
import os #sistem klasörlerine dosylarına ulaşabilmek için
import tkinter as tk  #arayüz
from tkinter import *   #içeride ki metotları direkt olarak kullanabilirim
import vlc  #müzik ses dosylarını çalabilmek için
from PIL import Image , ImageTk    #buton ikonları png yüklenip orada göstermek için kullanmak için

def last(list):  #listenin son elemanını döndüren yardımcı fonksiyon
    return list[-1]    #listenin son indexini döndürür

def music_name():
    global my_music , music_number   #dış kapsam alanında ki musicleri ve mevcut şarkının indexine erişim için
    return last(my_music[music_number].split("/"))   #tam yolu  / ile bölüp son parçayı dosya yolunu alır 


def play_music():    #seçili olan şarkıyı başlatma fonksiyonu
    global my_music , music_number , player , instance 
    to_play=my_music[music_number]    #çalınacak dosyanın dosya yolu
    media= instance.media_new(to_play)    #vlc instance dan yeni bir medya nesnesi oluştur
    player.set_media(media)    #oluşturulan medyayı playera atadık
    player.play()


def pause_music():
    player.pause()

def next_music():
    global  my_music , music_number , music_label
    if music_number < len(my_music) -1:
        music_number +=1                       #liste sonuna gelene kadar indexi bir arttırabilirsin 
    music_label.config(text=str(music_name))   #şarkı adını da güncelledik                         
    play_music()

def previous_music():
    global  my_music , music_number , music_label
    if music_number > 0:
        music_number -=1                       #liste sonuna gelene kadar indexi bir eksiltebilsin 
        music_label.config(text=music_name())  #şarkı adını da güncelledik                         
    play_music()


def set_volume(value):
    volume= int(value)
    player.audio_set_volume(volume)


music_number= 0      #sıfırıncı indexte ki müzik ile başlanacak
window=Tk()
window.geometry("500x300")   #boyutları ayarladık
window.resizable(False,False)   #boyutlandırmayı sağa sola aşağı büyütmeyi kapattık
window.title("Mp3 Player")
window.configure(bg="#1e1e2e")

instance= vlc.Instance()   #vlc ile instance oluşturduk ama (pc de vlc kurulıu olduğu için direkt alabildik )
player=instance.media_player_new()  #media oynatıcı nesnesini oluşturduk
music_folder= os.path.join(os.path.dirname(os.path.abspath("__file__")),"music-player")
my_music= glob.glob(os.path.join(music_folder, "*.mp3"))


if not my_music:
    raise SystemExit(f"{music_folder} klasöründe mp3 dosyası bulunamadı")

def load_image(image_path, size=(50, 50)):
    image=Image.open(image_path)  #görseli PIL ile aç
    return ImageTk.PhotoImage(image.resize(size))   #görseli istenilen boyuta getirip tkinter foramtına dönüştürür.

play_image=load_image('music-player/img/play.png')
pause_image=load_image('music-player/img/pause.png')
forwad_image=load_image('music-player/img/forwad.png')
prev_image=load_image('music-player/img/prev.png')
stop_image=load_image('music-player/img/stop.png')

music_label= tk.Label(window, text=music_name(),font=("Segoe", 12, "bold"), fg="#cdd6f4", bg="#1e1e2e", wraplength=460 , justify="center" )


play= tk.Button(window , image=play_image, command=play_music , width=50 , height=50, bg='#1e1e2e', activebackground='#313244', bd=0)
pause= tk.Button(window , image=pause_image, command=pause_music , width=50 , height=50, bg='#1e1e2e', activebackground='#313244', bd=0)
forwad= tk.Button(window , image=forwad_image, command=next_music , width=50 , height=50, bg='#1e1e2e', activebackground='#313244', bd=0)
prev = tk.Button(window , image=prev_image, command=previous_music , width=50 , height=50, bg='#1e1e2e', activebackground='#313244', bd=0)
stop= tk.Button(window , image=stop_image, command=window.destroy , width=50 , height=50, bg='#1e1e2e', activebackground='#313244', bd=0)

button_y=140
button_gap=15
button_w=50
buttons_total_width=5 * button_w + 4* button_gap
start_x=(500 - buttons_total_width) //2

prev.place(x= start_x , y=button_y)  #1.sıra
play.place(x=start_x + (button_w + button_gap) *1, y=button_y) # 2sıra
pause.place(x=start_x + (button_w + button_gap) *2, y=button_y)  #3 sıra
stop.place(x=start_x + (button_w + button_gap) *3, y=button_y) #4sıra
forwad.place(x=start_x + (button_w + button_gap) *4, y=button_y) #5 sıra

music_label.place (x=20, y=30, width=460)  #şarkı adı yerleşim
volume_label= Label (window , text="Ses Seviyesi ", font=("Segoe UI, 10"), fg="#cdd6f4" , bg="#1e1e2e")
volume_label.place(x=20, y=200)
volume_slider= Scale(window, from_=0, to= 100, orient=HORIZONTAL, command=set_volume, length=460, bg="#1e1e2e", fg="#cdd6f4", troughcolor="#313244", highlightthickness=0, bd=0)
volume_slider.set(50)
volume_slider.place(x=20 , y=245)


window.mainloop()