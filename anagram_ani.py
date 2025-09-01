from PIL import Image, ImageDraw, ImageFont
import random, os, string

word1 = "GregwiseNoah"
word2 = "AshwinGeorge"

max_len = max(len(word1), len(word2))
w1 = word1.ljust(max_len)
w2 = word2.ljust(max_len)


font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu[wdth,wght].ttf", 48)  
num_flicker_frames = 5      
padding = 2
alphabet = string.ascii_letters + string.digits + "_!@#$%^&*"

def get_text_size(text, font):
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

def scramble_transition(start, end, text_color):
    frames = []
    current = list(start)

    for i in range(max_len):
        if current[i] != end[i]:
            for _ in range(num_flicker_frames):
                current[i] = random.choice(alphabet)
                text = "".join(current)
                w, h = get_text_size(text, font)
                img_size = (w + padding * 2, h + padding * 2)
                img = Image.new("RGBA", img_size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.text((padding, padding), text, font=font, fill=text_color)
                frames.append(img)

            current[i] = end[i]
            text = "".join(current)
            w, h = get_text_size(text, font)
            img_size = (w + padding * 2, h + padding * 2)
            img = Image.new("RGBA", img_size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.text((padding, padding), text, font=font, fill=text_color)
            frames.append(img)

    return frames

def build_animation(text_color, filename):
    frames = []
    frames.extend(scramble_transition(w1, w2, text_color))
    for _ in range(10):
        frames.append(frames[-1])
    frames.extend(scramble_transition(w2, w1, text_color))
    for _ in range(10):
        frames.append(frames[-1])

    os.makedirs("assets", exist_ok=True)
    output_path = os.path.join("assets", filename)
    frames[0].save(output_path, save_all=True, append_images=frames[1:],
                   duration=80, loop=0, disposal=2, transparency=0)
    print(f"Saved {output_path}")

build_animation("black", "anagram_light.gif")
build_animation("white", "anagram_dark.gif")
