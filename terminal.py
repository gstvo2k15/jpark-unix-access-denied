"""
Jurassic Park-style "Access Denied" simulation.
Displays a looping GIF of Dennis Nedry with a custom UNIX background.
"""

import os
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk, ImageSequence
import pygame

# Resolve paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(BASE_DIR, "nedry.gif")
AUDIO_PATH = os.path.join(BASE_DIR, "denied.mp3")
BACKGROUND_PATH = os.path.join(BASE_DIR, "unix.jpg")

# Initialize pygame for sound playback
pygame.mixer.init()

def play_sound():
    """Plays the denial sound."""
    pygame.mixer.music.load(AUDIO_PATH)
    pygame.mixer.music.play()

def animate_gif(label, frames, index=0):
    """Loops through GIF frames using Tkinter's `after()` method."""
    if frames:
        frame = frames[index]
        img = ImageTk.PhotoImage(frame)
        label.config(image=img)
        label.image = img
        index = (index + 1) % len(frames)

        # Schedule next frame update without blocking execution
        label.after(100, animate_gif, label, frames, index)

def start_animation(root, label, frames):
    """Starts both the GIF animation and the sound."""
    root.title("Access Denied!")  # Set the title when clicking the button
    play_sound()
    animate_gif(label, frames)

def show_access_denied():
    """Creates the GUI window displaying the GIF and denial button."""
    root = tk.Tk()
    root.title("")  # Initially no title

    # Load the background image
    bg_image = Image.open(BACKGROUND_PATH)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Load GIF frames (fixed)
    gif = Image.open(GIF_PATH)
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]  # ✅ FIXED

    # Get window size based on background image
    bg_width, bg_height = bg_image.size

    # Get screen size
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate position to center the window
    pos_x = (screen_width - bg_width) // 2
    pos_y = (screen_height - bg_height) // 2

    # Set window size and position
    root.geometry(f"{bg_width}x{bg_height}+{pos_x}+{pos_y}")

    # Set background image
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Keep a reference to the background image to prevent garbage collection
    bg_label.image = bg_photo

    # GIF display label (initially empty)
    label = Label(root, bg="black")
    label.pack(expand=True)

    # Access button (starts animation & sound)
    btn = tk.Button(
        root, text="Attempt Access", font=("Arial", 14), width=15,
        command=lambda: start_animation(root, label, frames),  # ✅ Fix: Pass frames properly
        bg="red", fg="white", padx=20, pady=10
    )
    btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    show_access_denied()
