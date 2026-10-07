import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Watermark App")
        self.window.geometry("600x600")

        # Store the image
        self.image = None
        self.original_image = None

        # Title
        self.title_label = tk.Label(
            window,
            text="Watermark Your Image",
            font=("Arial", 20)
        )
        self.title_label.pack(pady=20)

        # Upload button
        self.upload_button = tk.Button(
            window,
            text="Upload Image",
            command=self.upload_image,
            font=("Arial", 14)
        )
        self.upload_button.pack(pady=10)

        # Image display
        self.image_label = tk.Label(
            window,
            text="No image uploaded",
            font=("Arial", 14)
        )
        self.image_label.pack(pady=20)

        # Watermark text box
        self.watermark_entry = tk.Entry(
            window,
            width=40,
            font=("Arial", 12),
            justify="center"
        )
        self.watermark_entry.pack(pady=10)

        # Watermark button
        self.watermark_button = tk.Button(
            window,
            text="Add Watermark",
            command=self.add_watermark,
            font=("Arial", 14)
        )
        self.watermark_button.pack(pady=10)

        # Save button
        self.save_button = tk.Button(
            window,
            text="Save Image",
            command=self.save_image,
            font=("Arial", 14)
        )
        self.save_button.pack(pady=10)

    def upload_image(self):
        filename = filedialog.askopenfilename(
            filetypes=[
                ("Image Files", "*.jpg *.jpeg *.png")
            ]
        )

        if filename:
            self.original_image = Image.open(filename).copy()
            self.image = self.original_image.copy()

            # Create preview
            preview = self.image.copy()
            preview.thumbnail((500, 400))

            photo = ImageTk.PhotoImage(preview)

            self.image_label.config(image=photo)
            self.image_label.image = photo


    def add_watermark(self):
        if not hasattr(self, "original_image"):
            return

        watermark = self.watermark_entry.get().strip()
        if watermark == "":
            return

        # Start from the original image every time
        self.image = self.original_image.copy()

        draw = ImageDraw.Draw(self.image)

        # Start with a large font
        font_size = 40

        # Leave some space around the edges
        max_width = self.image.width * 0.9
        max_height = self.image.height * 0.9

        # Keep reducing the font until the text fits
        while font_size > 5:
            font = ImageFont.truetype("arial.ttf", font_size)

            bbox = draw.textbbox((0, 0), watermark, font=font)

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            if text_width <= max_width and text_height <= max_height:
                break

            font_size -= 1

        # Center the watermark
        x = (self.image.width - text_width) // 2
        y = (self.image.height - text_height) // 2

        # Draw the watermark
        draw.text(
            (x, y),
            watermark,
            font=font,
            fill="black"
        )

        # Create preview
        preview = self.image.copy()
        preview.thumbnail((500, 400))

        photo = ImageTk.PhotoImage(preview)

        # Update display
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def save_image(self):
        if self.image is None:
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg")
            ]
        )

        if filename:
            self.image.save(filename)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Create the application
    app = WatermarkApp(root)
    # Start the GUI
    root.mainloop()