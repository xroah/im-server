from PIL import Image, ImageDraw, ImageFont
from random import randint
from io import BytesIO
from base64 import b64encode
from os import path

img_width = 130
img_height = 60
white = (255, 255, 255)
black = (0, 0, 0)


def get_code():
    ret = []
    code_arr = []

    def char(start, end):
        for n in range(ord(start), ord(end) + 1):
            code_arr.append(chr(n))

    char("0", "9")
    char("a", "z")
    char("A", "Z")

    for i in range(0, 4):
        index = randint(0, len(code_arr) - 1)
        ret.append(code_arr[index])

    return ret


def draw_line(img: Image):
    xy = []

    for _ in range(0, 15):
        xy.append((randint(0, img_width), randint(0, img_height)))

    d = ImageDraw.Draw(img)
    d.line(xy, fill=black, width=1)


def gen_code():
    char_width = 30
    char_height = 40
    chars = get_code()
    code_image = Image.new("RGB", (img_width, img_height), white)
    cur_dir = path.dirname(__file__)
    font_file = path.normpath(path.join(cur_dir, "./fonts/code.ttf"))

    fnt = ImageFont.truetype(font_file, 25)

    for (i, c) in enumerate(chars):
        char_img = Image.new("RGBA", (char_width, char_height), white)
        char = ImageDraw.Draw(char_img)
        deg = randint(-45, 45)

        char.text((8, 0), c, font=fnt, fill=black)

        code_image.paste(
            char_img.rotate(deg, fillcolor=white),
            (char_width * i, 5)
        )

    draw_line(code_image)

    return {
        "code": "".join(chars),
        "image": code_image
    }


def img2base64(image):
    prefix = "data:image/jpeg;base64,"
    file = BytesIO()
    image.save(file, "JPEG")
    img_str = b64encode(file.getvalue()).decode()

    return f"{prefix}{img_str}"
