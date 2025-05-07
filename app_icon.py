from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with a white background
    size = 256
    image = Image.new('RGB', (size, size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw a blue rectangle for the background
    draw.rectangle([(0, 0), (size, size)], fill='#2196F3')
    
    # Draw a white circle
    margin = 20
    draw.ellipse([(margin, margin), (size-margin, size-margin)], fill='white')
    
    # Draw a dollar sign
    try:
        font = ImageFont.truetype("Arial", 120)
    except:
        font = ImageFont.load_default()
    
    text = "$"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill='#2196F3', font=font)
    
    # Save as ICO file
    image.save('app_icon.ico')
    print("Icon created successfully!")

if __name__ == '__main__':
    create_icon() 