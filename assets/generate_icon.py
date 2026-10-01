"""Generate an Apple-inspired dark glassmorphism application icon."""

import os
from PIL import Image, ImageDraw, ImageFont


def create_app_icon(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    size = (512, 512)
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. Outer Squircle / Rounded Rectangle
    corner_radius = 110
    draw.rounded_rectangle(
        [(16, 16), (496, 496)],
        radius=corner_radius,
        fill=(22, 24, 31, 250),
        outline=(70, 75, 95, 180),
        width=4,
    )

    # 2. Subtle glass highlight at the top half
    draw.rounded_rectangle(
        [(24, 24), (488, 250)],
        radius=90,
        fill=(255, 255, 255, 14),
    )

    # 3. Top display screen
    draw.rounded_rectangle(
        [(44, 48), (468, 170)],
        radius=36,
        fill=(14, 15, 20, 240),
        outline=(50, 54, 70, 160),
        width=3,
    )

    # Display text representation (mini numbers & orange result)
    draw.rounded_rectangle(
        [(330, 80), (446, 94)],
        radius=7,
        fill=(140, 145, 165, 180),
    )
    draw.rounded_rectangle(
        [(220, 114), (446, 144)],
        radius=8,
        fill=(255, 159, 10, 240),  # Apple Amber
    )

    # 4. Calculator Keypad Grid
    # 4 rows x 4 columns of keys
    keys = [
        # (row, col, color, is_symbol)
        (0, 0, (65, 70, 88, 220), "AC"),
        (0, 1, (65, 70, 88, 220), "+/-"),
        (0, 2, (65, 70, 88, 220), "%"),
        (0, 3, (255, 159, 10, 255), "÷"),  # Orange

        (1, 0, (48, 52, 65, 220), "7"),
        (1, 1, (48, 52, 65, 220), "8"),
        (1, 2, (48, 52, 65, 220), "9"),
        (1, 3, (255, 159, 10, 255), "×"),

        (2, 0, (48, 52, 65, 220), "4"),
        (2, 1, (48, 52, 65, 220), "5"),
        (2, 2, (48, 52, 65, 220), "6"),
        (2, 3, (255, 159, 10, 255), "−"),

        (3, 0, (48, 52, 65, 220), "1"),
        (3, 1, (48, 52, 65, 220), "2"),
        (3, 2, (48, 52, 65, 220), "3"),
        (3, 3, (48, 209, 88, 255), "="),  # Green equals
    ]

    start_x = 48
    start_y = 196
    key_w = 92
    key_h = 62
    gap_x = 16
    gap_y = 14

    for r, c, color, label in keys:
        x0 = start_x + c * (key_w + gap_x)
        y0 = start_y + r * (key_h + gap_y)
        x1 = x0 + key_w
        y1 = y0 + key_h
        draw.rounded_rectangle(
            [(x0, y0), (x1, y1)],
            radius=18,
            fill=color,
            outline=(255, 255, 255, 30),
            width=1,
        )

    # Save PNG
    png_path = os.path.join(output_dir, "icon.png")
    img.save(png_path, "PNG")

    # Save Multi-resolution ICO for Windows
    ico_path = os.path.join(output_dir, "icon.ico")
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    img.save(ico_path, format="ICO", sizes=icon_sizes)

    print(f"Icons generated:\n  {png_path}\n  {ico_path}")


if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    create_app_icon(out_dir)
