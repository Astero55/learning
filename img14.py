import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, Scrollbar
from PIL import Image, ImageTk
import numpy as np
from collections import Counter

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])

def compare_images(img1_path, img2_path):
    img1 = Image.open(img1_path).convert('RGB')
    img2 = Image.open(img2_path).convert('RGB')

    img1 = img1.resize((250, 250), Image.LANCZOS)
    img2 = img2.resize((250, 250), Image.LANCZOS)

    img1 = np.array(img1)
    img2 = np.array(img2)

    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= float(img1.shape[0] * img1.shape[1])
    err /= 255.0**2

    similarity_score = 100 * (1 - err)

    return similarity_score

def get_top_colors(image_path, top_colors=10):
    with Image.open(image_path).convert('RGB') as img:
        width, height = img.size
        left = width * 0.25
        top = height * 0.25
        right = width * 0.75
        bottom = height * 0.75
        img = img.crop((left, top, right, bottom)).getdata()

    color_counter = Counter(img)
    common_colors = color_counter.most_common(top_colors)
    total_pixels = sum(color_counter.values())
    color_percentage = [(rgb_to_hex(color), count / total_pixels * 100) for color, count in common_colors]

    return color_percentage

def open_image(label):
    file_path = filedialog.askopenfilename()
    img = Image.open(file_path)
    preview = img.resize((250, 250), Image.LANCZOS)
    photo = ImageTk.PhotoImage(preview)

    label.config(image=photo)
    label.image = photo

    return file_path

def compare():
    similarity_score = compare_images(image1_path.get(), image2_path.get())
    result_label.config(text=f"Your images are {similarity_score:.2f}% similar")

    top_colors1 = get_top_colors(image1_path.get())
    top_colors2 = get_top_colors(image2_path.get())

    color_result_text.delete(1.0, tk.END)
    color_result_text.insert(tk.END, "Top 10 colors in image 1:\n")
    for color, percentage in top_colors1:
        color_result_text.insert(tk.END, f"{color}: {percentage:.2f}%\n")

    color_result_text.insert(tk.END, "\nTop 10 colors in image 2:\n")
    for color, percentage in top_colors2:
        color_result_text.insert(tk.END, f"{color}: {percentage:.2f}%\n")

root = tk.Tk()
root.geometry('600x600')
root.title("Image Comparison")

style = ttk.Style(root)
style.theme_use('clam')

image1_path = tk.StringVar()
image2_path = tk.StringVar()

image1_label = tk.Label(root)
image1_label.pack()

open_image1_button = ttk.Button(root, text='Open Image 1', command=lambda: image1_path.set(open_image(image1_label)))
open_image1_button.pack()

image2_label = tk.Label(root)
image2_label.pack()

open_image2_button = ttk.Button(root, text='Open Image 2', command=lambda: image2_path.set(open_image(image2_label)))
open_image2_button.pack()

compare_button = ttk.Button(root, text='Compare', command=compare)
compare_button.pack()

result_label = tk.Label(root, text="", font=("Helvetica", 18))
result_label.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

color_result_text = tk.Text(root, yscrollcommand=scrollbar.set)
color_result_text.pack()

scrollbar.config(command=color_result_text.yview)

explanation_text = "This app compares two images by calculating the Mean Squared Error (MSE) between them. " \
                   "The MSE is the average squared difference between the corresponding pixels in the two images. " \
                   "The MSE is then normalized and subtracted from 100 to give a similarity score. " \
                   "A higher score indicates more similar images."
explanation_label = tk.Label(root, text=explanation_text, wraplength=400, font=("Helvetica", 12))
explanation_label.pack()

root.mainloop()
