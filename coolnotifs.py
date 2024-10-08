import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageFont
import numpy as np
import os

"""
TODO:

implement what chatgpt told me to do, which is:

FUCKKKK

import os

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path for "gun.jpg"
input_image_path = os.path.join(script_dir, "gun.jpg")

# Now you can open the image using the correct path
img = Image.open(input_image_path)

Do not ask me how, do not ask me why. All i know is that it's needed to work
on more than just my machine.
"""

global script_dir
script_dir = os.path.dirname(os.path.realpath(__file__))
print(script_dir)

def average_color(image):
    """Calculate the average color of the given image."""
    # Convert image to numpy array
    img_array = np.array(image)
    # Calculate the average color for each channel (R, G, B)
    avg_color = img_array.mean(axis=(0, 1))  # Average over height and width
    return tuple(map(int, avg_color))  # Return as integer RGB tuple

def overlay_text(draw, x, y, font, text, line_spacing=5):
    # Split the text into lines for multi-line support
    lines = []
    words = text.split()
    current_line = ""

    # Maximum width for wrapping text
    max_width = 300 - x  # Adjust based on your image width and padding

    for word in words:
        # Check if adding the next word exceeds the max width
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]  # Calculate width from bbox
        print(bbox)
        
        if text_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Append the last line
    lines.append(current_line)

    # Draw each line of text at the specified coordinates
    for line in lines:
        draw.text((x, y), line, fill=(255, 255, 255), font=font)  # White color
        # Calculate the height of the current line using textbbox
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]  # Height is the difference between bottom and top of the bbox
        y += line_height + line_spacing  # Move down by the height of the text + line spacing

def create_images(input_image_path, mask_image_path, text1, text2):
    # Step 1: Load the input image to calculate the average color
    img = Image.open(input_image_path)
    
    # Step 2: Calculate the average color for the background
    avg_bg_color = average_color(img)
    
    # Step 3: Create Image 1 with the average color
    image1 = Image.new("RGB", (300, 100), avg_bg_color)

    # Step 4: Create Image 2 with #000000
    image2 = Image.new("RGB", (300, 100), "#000000")

    # Step 5: Resize the square image
    width, height = img.size
    new_width = 150
    new_height = int((new_width / width) * height)  # Maintain aspect ratio
    resized_img = img.resize((new_width, new_height))

    # Step 6: Center the resized image on Image 2
    x_offset = 0  # Overlap left edge with the left edge of Image 2
    y_offset = (100 - new_height) // 2  # Center vertically
    image2.paste(resized_img, (x_offset, y_offset))

    # Step 7: Load the mask image and resize it to 300x100
    mask_image = Image.open(mask_image_path).convert("L")  # Load as grayscale
    mask_image = mask_image.resize((300, 100))  # Resize to match Image 2 dimensions

    # Step 8: Apply the mask to Image 2
    image2.putalpha(mask_image)

    # Step 9: Overlay Image 2 over Image 1
    image1_with_overlay = Image.alpha_composite(image1.convert("RGBA"), image2.convert("RGBA"))

    # Step 10: Prepare to draw text on the final image
    draw = ImageDraw.Draw(image1_with_overlay)

    # Define text and properties
    padding = 10  # Padding for text
    bold_font_path = "/usr/share/fonts/TTF/JetBrainsMono-Bold.ttf"  # Replace with actual path
    regular_font_path = "/usr/share/fonts/TTF/JetBrainsMono-Regular.ttf"  # Replace with actual path
    font_size = 15  # Font size
    bold_font = ImageFont.truetype(bold_font_path, font_size)  # Load the bold font
    regular_font = ImageFont.truetype(regular_font_path, font_size)  # Load the regular font

    # Overlay the text onto the image
    overlay_text(draw, padding + 130, padding, bold_font, text1)  # Draw bold text
    overlay_text(draw, padding + 130, padding + 25, regular_font, text2)  # Draw regular text below the bold text

    # Step 11: Save the modified image
    image1_with_overlay.save(f"{script_dir}/image3.png", "PNG")

# Example usage
#create_images("/home/cheddy/.cache/vlc/art/arturl/0954c9bc00d50b1442401b05629bfd8d/art", "/home/cheddy/Documents/notifmask.png","Now Playing:", "Katamari - Femtanyl")  # Replace with actual paths

def create_overlay(image_path):
    # Create a new Tkinter window
    overlay = tk.Tk()
    overlay.overrideredirect(True)  # Remove window borders and title bar
    overlay.attributes("-topmost", True)  # Keep on top of all other windows
    overlay.geometry("300x100-14+50")  # Set size and position

    # Load the image using PIL
    img = Image.open(image_path)
    img = img.resize((300, 100), Image.LANCZOS)  # Resize the image to fit the overlay
    photo = ImageTk.PhotoImage(img)

    # Create a label to display the image
    label = tk.Label(overlay, image=photo, bg='black')  # Set bg to black or transparent
    label.image = photo  # Keep a reference to avoid garbage collection
    label.pack(expand=True, fill='both')

    # Set a timer to destroy the overlay after a certain time
    overlay.after(6000, overlay.destroy)  # Destroy after 6 seconds

    overlay.bind("<Button-1>", lambda e: overlay.destroy())
    
    overlay.mainloop()

# Example usage with an image path
#create_overlay("image3.png")  # Replace with your image path

def sendnotif(text1, text2, image="Default.png"):
    if not image[0] == "/":
        create_images(f"{script_dir}/{image}", f"{script_dir}/ImageMask.png", text1, text2)
    else:
        create_images(f"{image}", f"{script_dir}/ImageMask.png", text1, text2)
    create_overlay(f"{script_dir}/image3.png")
