import os
import argparse
from PIL import Image, ImageDraw, ImageFont
from exif import Image as ExifImage
from datetime import datetime

def get_exif_data(image_path):
    with open(image_path, 'rb') as img_file:
        img = ExifImage(img_file)
        
    if not img.has_exif:
        return ["No EXIF data found", ""]
    
    try:
        camera = img.model
    except AttributeError:
        camera = "N/A"

    try:
        # Try different possible EXIF tags for lens model
        if hasattr(img, 'lens_model'):
            lens = img.lens_model
        elif hasattr(img, 'lens_make'):
            lens = img.lens_make
        else:
            lens = "N/A"
    except AttributeError:
        lens = "N/A"
        
    try:
        focal_length = f"{img.focal_length}mm"
    except AttributeError:
        focal_length = "N/A"
        
    try:
        f_stop = f"f/{img.f_number:.1f}"
    except AttributeError:
        f_stop = "N/A"
        
    try:
        exposure_time = f"{img.exposure_time}s"
        # Convert fractions like 1/1000 to proper format
        if exposure_time.startswith("0."):
            denominator = int(1 / float(img.exposure_time))
            exposure_time = f"1/{denominator}s"
    except AttributeError:
        exposure_time = "N/A"
        
    try:
        iso = f"ISO {img.photographic_sensitivity}"
    except AttributeError:
        iso = "N/A"

    try:
        # Try to get the original date time
        date_taken = datetime.strptime(img.datetime_original, '%Y:%m:%d %H:%M:%S')
        date_str = date_taken.strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError:
        try:
            # Fall back to datetime if datetime_original is not available
            date_str = img.datetime
        except AttributeError:
            date_str = "N/A"
    
    # Return two lines of text
    line1 = f"{date_str} | {camera} | {lens}"
    line2 = f"{focal_length} | {f_stop} | {exposure_time} | {iso}"
    return [line1, line2]

def process_image(input_path, output_path):
    # Open and process the image
    img = Image.open(input_path)
    
    # Get EXIF data
    exif_lines = get_exif_data(input_path)
    
    # Create new image with space for the border
    border_height = 110  # Reduced from 120 to 110 pixels to reduce top margin
    new_img = Image.new('RGB', (img.width, img.height + border_height), 'black')
    new_img.paste(img, (0, 0))
    
    # Add text to the border
    draw = ImageDraw.Draw(new_img)
    
    # Try to use Arial with larger font size, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    # Calculate text heights and positions
    text_bbox1 = draw.textbbox((0, 0), exif_lines[0], font=font)
    text_width1 = text_bbox1[2] - text_bbox1[0]
    text_height = text_bbox1[3] - text_bbox1[1]
    
    # Position first line slightly closer to the top (reduced from 1/3 to 0.3 of height)
    text_x1 = (img.width - text_width1) // 2
    text_y1 = img.height + int(border_height * 0.3) - (text_height // 2)
    
    # Keep second line at same relative position to first line
    text_bbox2 = draw.textbbox((0, 0), exif_lines[1], font=font)
    text_width2 = text_bbox2[2] - text_bbox2[0]
    text_x2 = (img.width - text_width2) // 2
    text_y2 = img.height + int(border_height * 0.7) - (text_height // 2)
    
    # Draw both lines
    draw.text((text_x1, text_y1), exif_lines[0], fill='white', font=font)
    draw.text((text_x2, text_y2), exif_lines[1], fill='white', font=font)
    
    # Save the processed image
    new_img.save(output_path, quality=95)

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process images by adding EXIF data in a bottom border')
    parser.add_argument('input_dir', help='Directory containing the JPG images to process')
    parser.add_argument('-o', '--output_dir', 
                      help='Full path to a custom output directory (if you want to save outside the input directory)')
    parser.add_argument('-s', '--subfolder', default='images with exif',
                      help='Name of the subfolder in input directory to save processed images (default: "images with exif")')
    args = parser.parse_args()

    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist")
        return

    # Set output directory - either custom path or subfolder of input directory
    if args.output_dir is not None:
        output_dir = args.output_dir
    else:
        output_dir = os.path.join(args.input_dir, args.subfolder)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Process all jpg files in input directory
    for filename in os.listdir(args.input_dir):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            print(f"Processing {filename}...")
            input_path = os.path.join(args.input_dir, filename)
            output_path = os.path.join(output_dir, f"processed_{filename}")
            try:
                process_image(input_path, output_path)
                print(f"Saved to {output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()