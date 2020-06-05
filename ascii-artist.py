from PIL import Image, ImageDraw, ImageFont
from statistics import mean
import argparse

parser = argparse.ArgumentParser(description="Converts an image to ASCII characters.")
parser.add_argument('--foreach', dest='foreach', action='store_true', default=False, help="converts *each* pixel to an ASCII character")
parser.add_argument('--dark', dest='dark', action='store_true', default=False, help="creates the image with dark background")
parser.add_argument('file', help="the original file")
args = parser.parse_args()

horizontal = 6
vertical = 10

original = Image.open(args.file).convert('L')
if not args.foreach:
    width = int(original.size[0] / horizontal)
    height = int(original.size[1] / vertical)
else: width, height = original.size[0], original.size[1]
if not args.dark: new = Image.new('L', (width * horizontal, height * vertical), color=255)
else: new = Image.new('L', (width * horizontal, height * vertical), color=0)
draw = ImageDraw.Draw(new)
font = ImageFont.truetype('consola.ttf', 11)
out_text = ''

if not args.dark: chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
else: chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
converter = (len(chars) - 1) / 255

if not args.foreach:
    for row in range(height):
        for col in range(width):
            letter = []
            for y in range(row * vertical, row * vertical + vertical):
                for x in range(col * horizontal, col * horizontal + horizontal):
                    letter.append(original.getpixel((x, y)))
            out_text += chars[round(mean(letter) * converter)]
        out_text += '\n'
else:
    for y in range(height):
        for x in range(width):
            out_text += chars[round(original.getpixel((x, y)) * converter)]
        out_text += '\n'

if not args.dark: draw.text((0, 0), out_text, font=font, fill=0, spacing=1)
else: draw.text((0, 0), out_text, font=font, fill=255, spacing=1)
new.save(args.file + '-ascii.png')
