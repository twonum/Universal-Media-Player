import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import customtkinter as ctk
import pygame
from moviepy.editor import VideoFileClip
from PIL import Image, ImageTk
import threading
import time

# Initialize Pygame
pygame.mixer.init()

# Global variables
list_of_media = []
list_of_covers = []
current_index = 0
media_length = 0
clip = None

# Function to load media files
def load_media():
    global list_of_media, list_of_covers, current_index, media_length, clip
    filetypes = [('Media Files', '*.mp3 *.wav *.ogg *.mp4 *.avi *.mov')]
    filenames = filedialog.askopenfilenames(filetypes=filetypes)
    if filenames:
        list_of_media = list(filenames)
        list_of_covers = ['img/default_cover.jpg'] * len(list_of_media)
        current_index = 0
        play_media()

# Function to display album cover
def get_album_cover(media_name):
    global current_index
    cover_path = list_of_covers[current_index]
    try:
        image1 = Image.open(cover_path)
        image2 = image1.resize((250, 250))
        load = ImageTk.PhotoImage(image2)
        cover_label.config(image=load)
        cover_label.image = load
    except FileNotFoundError:
        cover_label.config(image='')

    stripped_string = media_name.split('/')[-1].split('.')[0]
    song_name_label.config(text=stripped_string)

# Function to update progress bar
def update_progress():
    while pygame.mixer.music.get_busy() or (clip and clip.is_playing()):
        time.sleep(1)
        if media_length > 0:
            pos = pygame.mixer.music.get_pos() / 1000 if pygame.mixer.music.get_busy() else clip.reader.get_position()
            progressbar.set(pos / media_length)

# Function to play media
def play_media():
    global current_index, media_length, clip
    if not list_of_media:
        messagebox.showerror("Error", "No media files loaded.")
        return

    media_name = list_of_media[current_index]
    if media_name.endswith(('.mp3', '.wav', '.ogg')):
        pygame.mixer.music.load(media_name)
        pygame.mixer.music.play()
        media_length = pygame.mixer.Sound(media_name).get_length()
        clip = None
    elif media_name.endswith(('.mp4', '.avi', '.mov')):
        clip = VideoFileClip(media_name)
        media_length = clip.duration
        clip.preview()  # This will open the default video player for preview
        pygame.mixer.music.stop()  # Ensure pygame is not playing any sound
    else:
        messagebox.showerror("Error", "Unsupported media format!")
        return

    get_album_cover(media_name)
    threading.Thread(target=update_progress, daemon=True).start()

# Function to skip forward in media
def skip_forward():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() + 5000)  # Skip forward by 5 seconds
    elif clip and clip.is_playing():
        clip.reader.seek(clip.reader.get_position() + 5)

# Function to skip backward in media
def skip_back():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.set_pos(pygame.mixer.music.get_pos() - 5000)  # Skip backward by 5 seconds
    elif clip and clip.is_playing():
        clip.reader.seek(clip.reader.get_position() - 5)

# Function to adjust volume
def volume(value):
    pygame.mixer.music.set_volume(float(value))

# Function to handle playback speed (requires different library or workaround)
def speed_control(speed):
    pass

# Function to exit the application
def exit_application():
    root.quit()

# Initialize the main window
root = ctk.CTk()
root.title('Universal Media Player')
root.geometry('600x600')  # Adjusted height for better layout
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# UI Elements
cover_label = ctk.CTkLabel(root, text="Cover", fg_color='#222222')
cover_label.place(relx=0.5, rely=0.25, anchor=tk.CENTER)

song_name_label = ctk.CTkLabel(root, text="", fg_color='#222222', text_color='white')
song_name_label.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

play_button = ctk.CTkButton(master=root, text='Play', command=play_media)
play_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

skip_f = ctk.CTkButton(master=root, text='>', command=skip_forward, width=2)
skip_f.place(relx=0.7, rely=0.55, anchor=tk.CENTER)

skip_b = ctk.CTkButton(master=root, text='<', command=skip_back, width=2)
skip_b.place(relx=0.3, rely=0.55, anchor=tk.CENTER)

volume_slider = ctk.CTkSlider(master=root, from_=0, to=1, command=volume, width=210)
volume_slider.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

speed_slider = ctk.CTkSlider(master=root, from_=0.5, to=2.0, command=speed_control, width=210)
speed_slider.set(1.0)
speed_slider.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

progressbar = ctk.CTkProgressBar(master=root, progress_color='#32a85a', width=250)
progressbar.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

load_button = ctk.CTkButton(master=root, text='Load Media', command=load_media)
load_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

exit_button = ctk.CTkButton(master=root, text='Exit', command=exit_application)
exit_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

# Run the application
root.mainloop()
