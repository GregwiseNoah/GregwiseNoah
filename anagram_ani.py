from PIL import Image, ImageDraw, ImageFont
import random, os

# Words to morph between
word1 = "GregwiseNoah"
word2 = "Ashwin_George"

# Normalize lengths
max_len = max(len(word1), len(word2))
w1 = word1.ljust(max_len)
w2 = word2.ljust(max_len)

# Settings
font = ImageFont.truetype("DejaVuSans-Bold.ttf", 48)  # larger, clearer font
num_steps = 30
padding = 10  # shrink margins

def get_text_size(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def make_transition(start, end, bg_color, text_color):
    frames = []
    for step in range(num_steps + 1):
        text_chars = [
            end[i] if random.random() < step / num_steps else start[i]
            for i in range(max_len)
        ]
        text = "".join(text_chars)

        w, h = get_text_size(text, font)
        img_size = (w + padding * 2, h + padding * 2)

        img = Image.new("RGB", img_size, bg_color)
        draw = ImageDraw.Draw(img)
        draw.text((padding, padding), text, font=font, fill=text_color)

        frames.append(img)
    return frames

def build_animation(bg_color, text_color, filename):
    frames = []
    frames.extend(make_transition(w1, w2, bg_color, text_color))
    frames.extend(make_transition(w2, w1, bg_color, text_color))

    os.makedirs("assets", exist_ok=True)
    output_path = os.path.join("assets", filename)
    frames[0].save(output_path, save_all=True, append_images=frames[1:],
                   duration=150, loop=0, disposal=2)
    print(f"Saved {output_path}")

# Generate light & dark versions
build_animation("white", "black", "anagram_light.gif")
build_animation("black", "white", "anagram_dark.gif")
