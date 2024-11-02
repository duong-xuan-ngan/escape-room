import tkinter as tk
import pygame
from PIL import Image, ImageTk
import random
import time
import threading

class Jumpscare:
    def __init__(self, master):
        self.master = master
        self.master.withdraw()
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)
        pygame.mixer.init()
        self.trigger_jumpscare()
    
    def trigger_jumpscare(self):
        screen_width, screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        window_size = 1000
        position_x = (screen_width - window_size) // 2
        position_y = (screen_height - window_size) // 2

        self.master.geometry(f"{window_size}x{window_size}+{position_x}+{position_y}")
        self.master.deiconify()

        self.canvas = tk.Canvas(self.master, width=window_size, height=window_size)
        self.canvas.pack()
        self.scare_image = Image.open("scare.png")
        self.scare_image = self.scare_image.resize((window_size, window_size))
        self.scare_image_tk = ImageTk.PhotoImage(self.scare_image)

        self.canvas.create_image(0, 0, anchor="nw", image=self.scare_image_tk)

        pygame.mixer.music.load('jumpscare.mp3')
        pygame.mixer.music.play()

        self.shake_thread = threading.Thread(target=self.shake)
        self.shake_thread.start()

        self.master.after(3000, self.close_jumpscare)

    def shake(self):
        end_time = time.time() + 3
        original_x = self.master.winfo_x()
        original_y = self.master.winfo_y()

        while time.time() < end_time:
            x_offset = random.randint(-200, 200)
            y_offset = random.randint(-200, 200)
            self.master.geometry(f"+{original_x + x_offset}+{original_y + y_offset}")
            self.master.update()
            time.sleep(0.03)
    def close_jumpscare(self):
        self.master.destroy()
