import tkinter as tk
import pygame
from PIL import Image, ImageTk
import random
import time
import threading

class Jumpscare:
    def __init__(self, master):
        self.master = master
        # Remove withdraw() to prevent initial delay
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)
        pygame.mixer.init()
        
        # Preload audio and image during initialization
        pygame.mixer.music.load('jumpscare3.mp3')
        
        # Get screen dimensions immediately
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        # Preload and process image
        self.scare_image = Image.open("jumpscare.jpg")
        self.scare_image = self.scare_image.resize((self.screen_width, self.screen_height))
        self.scare_image_tk = ImageTk.PhotoImage(self.scare_image)
        
        # Set up window and canvas immediately
        self.master.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        self.canvas = tk.Canvas(self.master, width=self.screen_width, height=self.screen_height)
        self.canvas.pack()
        
        # Trigger immediately
        self.trigger_jumpscare()
    
    def trigger_jumpscare(self):
        # Display immediately
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()
        
        # Display the image instantly
        self.canvas.create_image(0, 0, anchor="nw", image=self.scare_image_tk)
        
        # Play sound immediately
        pygame.mixer.music.play()
        
        # Start shaking without delay
        self.shake_thread = threading.Thread(target=self.shake, daemon=True)
        self.shake_thread.start()
        
        # Close after 3 seconds
        self.master.after(3000, self.close_jumpscare)
    
    def shake(self):
        end_time = time.time() + 3
        original_x = self.master.winfo_x()
        original_y = self.master.winfo_y()
        
        while time.time() < end_time:
            x_offset = random.randint(-20, 20)
            y_offset = random.randint(-20, 20)
            self.master.geometry(f"+{original_x + x_offset}+{original_y + y_offset}")
            self.master.update()
            time.sleep(0.03)
    
    def close_jumpscare(self):
        self.master.destroy()