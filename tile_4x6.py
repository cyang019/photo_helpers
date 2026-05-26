import argparse
import sys
from PIL import Image

def tile_photo_to_4x6(photo_path, output_path="tiled_print.jpg", margin_px=40):
    # Standard 300 DPI constants
    DPI = 300
    CANVAS_W, CANVAS_H = 6 * DPI, 4 * DPI  # 1800 x 1200 pixels
    
    # Target size: 33mm x 48mm converted to pixels
    PHOTO_W = int((33 / 25.4) * DPI)  # ~390 px
    PHOTO_H = int((48 / 25.4) * DPI)  # ~567 px

    # Create a white 4x6 background
    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), "white")
    
    # Load and resize the source photo
    img = Image.open(photo_path).resize((PHOTO_W, PHOTO_H), Image.Resampling.LANCZOS)

    # Calculate tiling capacity
    # (Canvas dimension - margin) // (Photo dimension + margin)
    cols = (CANVAS_W - margin_px) // (PHOTO_W + margin_px)
    rows = (CANVAS_H - margin_px) // (PHOTO_H + margin_px)
    
    # Calculate starting offsets to center the entire grid
    total_grid_w = (cols * PHOTO_W) + ((cols - 1) * margin_px)
    total_grid_h = (rows * PHOTO_H) + ((rows - 1) * margin_px)
    start_x = (CANVAS_W - total_grid_w) // 2
    start_y = (CANVAS_H - total_grid_h) // 2

    # Loop to fill spaces with copies
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (PHOTO_W + margin_px)
            y = start_y + row * (PHOTO_H + margin_px)
            canvas.paste(img, (x, y))

    # Save with DPI metadata for accurate printing
    canvas.save(output_path, dpi=(DPI, DPI))
    print(f"Success! Created a grid with {rows * cols} copies.")

# Example usage:
# tile_photo_to_4x6("my_photo.jpg")

def main():
    parser = argparse.ArgumentParser(description="Tile a 33x48mm photo onto a 4x6 inch canvas.")
    
    # Position arguments (required)
    parser.add_argument("input_image", help="Path to the source photo image file")
    
    # Optional arguments (with defaults)
    parser.add_argument("-o", "--output", default="tiled_print.jpg", help="Path to save the final 4x6 print (default: tiled_print.jpg)")
    parser.add_argument("-m", "--margin", type=int, default=40, help="Margin spacing between photos in pixels (default: 40)")

    args = parser.parse_args()

    # Execute core logic
    tile_photo_to_4x6(
        photo_path=args.input_image, 
        output_path=args.output, 
        margin_px=args.margin
    )

if __name__ == "__main__":
    main()

