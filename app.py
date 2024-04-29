import cv2
import easygui
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
import os

def upload_image():
    image_path = easygui.fileopenbox()
    if image_path:
        cartoonify(image_path)

def cartoonify(image_path):
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    smooth_gray_image = cv2.medianBlur(gray_image, 5)
    edges_image = cv2.adaptiveThreshold(smooth_gray_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color_image = cv2.bilateralFilter(original_image, 9, 300, 300)
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges_image)

    cartoon_image = cv2.cvtColor(cartoon_image, cv2.COLOR_BGR2RGB)
    cartoon_image_pil = Image.fromarray(cartoon_image)

    # Save the cartoonified image
    new_name = "cartoonified_image"
    path1 = os.path.dirname(image_path)
    extension = os.path.splitext(image_path)[1]
    path = os.path.join(path1, new_name + extension)
    cartoon_image_pil.save(path)

    # Display the cartoonified image
    cartoon_image_tk = ImageTk.PhotoImage(cartoon_image_pil)
    display_label.config(image=cartoon_image_tk)
    display_label.image = cartoon_image_tk

    # Save button
    save_button = tk.Button(top, text="Save Cartoon Image", command=lambda: save_image(cartoon_image_pil, path))
    save_button.pack()

def save_image(image, path):
    message = "Image saved as " + os.path.basename(path) + " at " + os.path.dirname(path)
    messagebox.showinfo(title=None, message=message)

top = tk.Tk()
top.geometry('600x600')
top.title('Cartoonify Your Image!')
top.configure(background='white')

upload_button = tk.Button(top, text="Upload Image", command=upload_image)
upload_button.pack()

display_label = tk.Label(top)
display_label.pack()

top.mainloop()
