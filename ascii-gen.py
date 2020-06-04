from PIL import Image, ImageDraw, ImageFont
from statistics import mean
import argparse

parser = argparse.ArgumentParser(description="Converts an image to ASCII characters.")
parser.add_argument('file', help="the original file")
parser.add_argument('--foreach', dest='foreach', action='store_true', default=False, help="converts each pixel to an ASCII character")
args = parser.parse_args()

original = Image.open(args.file).convert('L')
if not args.foreach:
    width = int(original.size[0] / 6)
    height = int(original.size[1] / 12)
else: width, height = original.size[0], original.size[1]
new = Image.new('L', (width * 6, height * 12), color=255)
draw = ImageDraw.Draw(new)
font = ImageFont.truetype('consola.ttf', 11)
out_text = ''

chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
converter = 69 / 255

if not args.foreach:
    for row in range(height):
        for col in range(width):
            letter = []
            for y in range(row * 12, row * 12 + 12):
                for x in range(col * 6, col * 6 + 6):
                    letter.append(original.getpixel((x, y)))
            out_text += chars[round(mean(letter) * converter)]
        out_text += '\n'
else:
    for y in range(height):
        for x in range(width):
            out_text += chars[round(original.getpixel((x, y)) * converter)]
        out_text += '\n'

draw.text((0, 0), out_text, font=font, fill=0, spacing=3)
new.save(args.file + '-ascii.png')
