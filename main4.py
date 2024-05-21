import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

# Fungsi untuk memilih gambar yang ingin diperiksa
def select_image():
    global test_image, test_image_path
    test_image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if test_image_path:
        test_image = Image.open(test_image_path)
        test_image_thumbnail = test_image.copy()
        test_image_thumbnail.thumbnail((200, 200))
        test_image_thumbnail = ImageTk.PhotoImage(test_image_thumbnail)
        test_image_label.config(image=test_image_thumbnail)
        test_image_label.image = test_image_thumbnail

# Fungsi untuk mendeteksi watermark menggunakan metode LSB
def detect_watermark():
    if test_image:
        test_image_array = np.array(test_image.convert("RGB"))
        
        # Asumsikan watermark berada di bagian kiri atas gambar dengan ukuran tertentu
        watermark_size = (100, 100)  # Ubah ukuran ini sesuai dengan ukuran watermark yang digunakan
        watermark_area = test_image_array[0:watermark_size[0], 0:watermark_size[1]]
        
        # Ekstraksi watermark dari bit paling tidak signifikan
        extracted_watermark = np.zeros((watermark_size[0], watermark_size[1]), dtype=np.uint8)
        for i in range(watermark_size[0]):
            for j in range(watermark_size[1]):
                extracted_watermark[i, j] = watermark_area[i, j, 0] & 1
        
        # Konversi array biner menjadi gambar
        extracted_watermark_image = Image.fromarray((extracted_watermark * 255).astype(np.uint8), 'L')
        extracted_watermark_thumbnail = extracted_watermark_image.copy()
        extracted_watermark_thumbnail.thumbnail((200, 200))
        extracted_watermark_thumbnail = ImageTk.PhotoImage(extracted_watermark_thumbnail)
        extracted_watermark_label.config(image=extracted_watermark_thumbnail)
        extracted_watermark_label.image = extracted_watermark_thumbnail
        result_label.config(text="Watermark detected and displayed below")
    else:
        messagebox.showerror("Error", "Please select an image to check for watermark")

# Inisialisasi antarmuka Tkinter
root = tk.Tk()
root.title("Watermark Detector using LSB")

# Frame for centering widgets
center_frame = tk.Frame(root)
center_frame.pack(expand=True)

# Label dan tombol untuk memilih gambar yang ingin diperiksa
test_image_label = tk.Label(center_frame)
test_image_label.pack()
select_image_button = tk.Button(center_frame, text="Select Image", command=select_image, bg="black", fg="white")
select_image_button.pack(anchor='center', pady=5)

# Tombol untuk mendeteksi watermark
detect_watermark_button = tk.Button(center_frame, text="Detect Watermark", command=detect_watermark, bg="black", fg="white")
detect_watermark_button.pack(anchor='center', pady=5)

# Label untuk menampilkan hasil deteksi watermark
result_label = tk.Label(center_frame, text="")
result_label.pack()

# Label untuk menampilkan gambar watermark yang terdeteksi
extracted_watermark_label = tk.Label(center_frame)
extracted_watermark_label.pack()

# Jalankan aplikasi Tkinter
root.mainloop()
