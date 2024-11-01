import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageEnhance

# ASCII characters used to create the art
ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65  # Adjust height for better aspect ratio
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    return image.convert("L")  # Convert image to grayscale

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = ""
    for pixel in pixels:
        # Ensure pixel is in the range of the ASCII_CHARS
        ascii_str += ASCII_CHARS[min(len(ASCII_CHARS) - 1, pixel // 25)]
    return ascii_str

def convert_image_to_ascii(image):
    image = resize_image(image)
    image = grayify(image)
    ascii_str = pixels_to_ascii(image)
    img_width = image.width
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[i:i + img_width] for i in range(0, ascii_str_len, img_width)])
    return ascii_img

def upload_image():
    global ascii_image_text
    file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if not file_path:
        return
    try:
        original_image = Image.open(file_path)
        contrast_value = contrast_scale.get()  # Get contrast adjustment value
        enhancer = ImageEnhance.Contrast(original_image)
        adjusted_image = enhancer.enhance(contrast_value)
        ascii_art = convert_image_to_ascii(adjusted_image)

        ascii_image_text.delete(1.0, tk.END)  # Clear existing text
        ascii_image_text.insert(tk.END, ascii_art)  # Insert ASCII art

        save_button.config(state=tk.NORMAL)  # Enable save button after conversion
    except Exception as e:
        messagebox.showerror("Error", f"Unable to convert image to ASCII. {str(e)}")

def save_ascii_art():
    ascii_art = ascii_image_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as f:
            f.write(ascii_art)

# GUI Setup
root = tk.Tk()
root.title("ASCII Art Creator")
root.geometry("1920x1080")  # Increase the overall window size

frame = ttk.Frame(root)
frame.pack(pady=20)

contrast_scale = tk.DoubleVar(value=1.0)  # Default contrast value
contrast_label = ttk.Label(frame, text="Contrast:")
contrast_label.pack()

contrast_slider = ttk.Scale(frame, from_=0.0, to=3.0, variable=contrast_scale, orient=tk.HORIZONTAL)
contrast_slider.pack()

upload_button = ttk.Button(frame, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Increased size for the ASCII art display canvas
ascii_image_text = tk.Text(frame, wrap=tk.WORD, height=40, width=120)  # Bigger canvas
ascii_image_text.pack(pady=10)

save_button = ttk.Button(frame, text="Save ASCII Art", command=save_ascii_art, state=tk.DISABLED)
save_button.pack(pady=10)

root.mainloop()
