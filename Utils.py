import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont


class ASCIIConverter:
    def __init__(self, font_path="Fonts/CONSOLA.TTF", font_size=12):
        self.font_path = font_path
        self.font_size = font_size
        self.symbols = {' ': 0, ':': 38, '+': 76, '#': 153, '@': 204}
        self.img2ascii = [min(self.symbols.items(), key=lambda item: abs(item[1] - i))[0] for i in range(256)]
        self.color = False

    def process_img(self, img, res_reduction=30, aspect_ratio_correction=1):
        new_width = int(img.shape[1] / res_reduction / aspect_ratio_correction)
        new_height = int(img.shape[0] / res_reduction)
        resized_img = cv2.resize(img, (new_width, new_height))
        return cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), resized_img

    def convert_to_ascii(self, img):
        return [''.join([self.img2ascii[pixel] for pixel in row]) for row in img]

    def str_to_img(self, ascii_img, resized_img):
        font = ImageFont.truetype(self.font_path, self.font_size)

        bbox = font.getbbox("A")
        char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

        image = Image.new('RGB', (char_width * len(ascii_img[0]), char_height * len(ascii_img)), "black")
        draw = ImageDraw.Draw(image)
        resized_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)

        for y, line in enumerate(ascii_img):
            for x, char in enumerate(line):
                if self.color:
                    col = tuple(resized_img[int(y * len(resized_img) / len(ascii_img)),
                                            int(x * len(resized_img[0]) / len(line))])
                else:
                    col = 'white'
                draw.text((x * char_width, y * char_height), char, fill=col, font=font)

        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    def process_and_convert_frame(self, frame, col=False, res_reduction=30):
        self.color = col
        processed_frame, resized_img = self.process_img(frame, res_reduction)
        ascii_frame = self.convert_to_ascii(processed_frame)

        img = self.str_to_img(ascii_frame, resized_img)
        new_width = int(2560)
        new_height = int(1440)
        resized_img = cv2.resize(img, (new_width, new_height))
        return resized_img

