import cv2
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from shutil import copyfile
from tkinter import ttk

def choose_input_folder():
    global input_folder_path
    input_folder_path = filedialog.askdirectory()
    input_folder_label.config(text="Selected input folder: " + input_folder_path)

def choose_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    output_folder_label.config(text="Selected output folder: " + output_folder_path)

def detect_faces():
    if not input_folder_path or not output_folder_path:
        messagebox.showerror("Error", "Please select both folders.")
        return
    
    image_files = [f for f in os.listdir(input_folder_path) if f.endswith('.jpg') or f.endswith('.png')]
    total_images = len(image_files)
    
    progress = tk.DoubleVar()
    progress_bar = ttk.Progressbar(window, variable=progress, maximum=total_images)
    progress_bar.pack()
    
    detected_images = 0
    
    for idx, file_name in enumerate(image_files):
        image_path = os.path.join(input_folder_path, file_name)
        
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise Exception("Could not read the image")
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                copyfile(image_path, os.path.join(output_folder_path, file_name))
                detected_images += 1
        
        except Exception as e:
            print(f"Problem with file {file_name}: {str(e)}")
        
        progress.set(idx + 1)
        window.update_idletasks()
    
    messagebox.showinfo("Scanning Complete", f"Found {detected_images} images with faces.")
    progress_bar.destroy()

window = tk.Tk()
window.title("Face Sorting")
window.geometry("350x220")  # Adjusted window size

input_folder_path = ""
output_folder_path = ""

input_folder_label = tk.Label(window, text="Choose input folder")
input_folder_label.pack()

input_button = tk.Button(window, text="Select folder", command=choose_input_folder)
input_button.pack()

output_folder_label = tk.Label(window, text="Choose output folder")
output_folder_label.pack()

output_button = tk.Button(window, text="Select folder", command=choose_output_folder)
output_button.pack()

# Creating an empty label for spacing
empty_label = tk.Label(window, text="")
empty_label.pack()

start_button = tk.Button(window, text="Start scanning", command=detect_faces)
start_button.pack()

window.mainloop()
