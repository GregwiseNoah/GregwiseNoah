from PIL import Image, ImageDraw, ImageFont
import random
import os

# Words to morph between
word1 = "GregwiseNoah"
word2 = "Ashwin_George"

# Normalize lengths (pad with spaces if needed)
max_len = max(len(word1), len(word2))
w1 = word1.ljust(max_len)
w2 = word2.ljust(max_len)

# Settings
font = ImageFont.load_default()  # swap with a TTF font for nicer look
img_size = (500, 100)
num_steps = 30  # number of steps for morphing

def get_text_size(text, font):
    bbox = font.getbbox(text)  # (x0, y0, x1, y1)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    return w, h

def make_transition(start, end, bg_color, text_color):
    frames = []
    for step in range(num_steps + 1):
        img = Image.new("RGB", img_size, bg_color)
        draw = ImageDraw.Draw(img)
        text_chars = []

        for i in range(max_len):
            if random.random() < step / num_steps:
                text_chars.append(end[i])
            else:
                text_chars.append(start[i])

        text = "".join(text_chars)
        w, h = get_text_size(text, font)
        draw.text(((img_size[0] - w) / 2, (img_size[1] - h) / 2),
                  text, font=font, fill=text_color)
        frames.append(img)
    return frames

def build_animation(bg_color, text_color, filename):
    frames = []
    frames.extend(make_transition(w1, w2, bg_color, text_color))
    frames.extend(make_transition(w2, w1, bg_color, text_color))

    os.makedirs("assets", exist_ok=True)
    output_path = os.path.join("assets", filename)
    frames[0].save(output_path, save_all=True, append_images=frames[1:],
                   duration=150, loop=0)

# Light mode: white bg, black text
build_animation("white", "black", "anagram_light.gif")

# Dark mode: black bg, white text
build_animation("black", "white", "anagram_dark.gif")
