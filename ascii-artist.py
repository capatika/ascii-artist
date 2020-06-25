from PIL import Image, ImageDraw, ImageFont
from statistics import mean
import argparse, ffmpeg, sys

def get_fps(original, progress=0.0):
    print("Getting video information... | {:.0f}%".format(progress), end='\r')

    if '.mp4' not in original[-4:]:
        print("The file specified is not a video.")
        raise SystemExit
    
    try:
        probe = ffmpeg.probe(original)
    except ffmpeg.Error as e:
        print(e.stderr)
        raise SystemExit

    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    if video_stream is None:
        print('                                                      ', end='\r')
        print('The file specified does not exist.')
        raise SystemExit

    try:
        avg_frame_rate = video_stream['avg_frame_rate']
    except KeyError:
        print('                                                      ', end='\r')
        print("The file specified is not a video.")
        raise SystemExit
    fps_list = avg_frame_rate.split('/')
    fps = round(float(fps_list[0]) / float(fps_list[1]), 2)

    print('                                                      ', end='\r')
    return fps


def get_images(original): pass


def convert_image(args, convertable: str, progress=0.0):
    try:
        original = Image.open(convertable).convert('L')
    except FileNotFoundError:
        print("The file specified does not exist.")
        raise SystemExit
    width = int(original.size[0] / horizontal)
    height = int(original.size[1] / vertical)
    if not args.dark: new = Image.new('L', (width * horizontal, height * vertical), color=255)
    else: new = Image.new('L', (width * horizontal, height * vertical), color=0)
    draw = ImageDraw.Draw(new)
    font = ImageFont.truetype('consola.ttf', 11)
    out_text = ''
    if not args.foreach:
        for row in range(height):
            for col in range(width):
                letter = []
                for y in range(row * vertical, row * vertical + vertical):
                    for x in range(col * horizontal, col * horizontal + horizontal):
                        letter.append(original.getpixel((x, y)))
                out_text += chars[round(mean(letter) * converter)]
            out_text += '\n'
            if args.video: print('Progress: {:.0f}% | {:.0f}%'.format((row * col) / (height * width) * 100, progress), end='\r')
            else: print('Progress: {:.0f}%'.format((row * col) / (height * width) * 100), end='\r')
    else:
        print("This feature is currently disabled.")
    print('                                                                                      ', end='\r')
    if args.video: print('Saving... | {:.0f}%'.format(progress), end='\r')
    else: print('Saving...')
    if not args.dark: draw.text((0, 0), out_text, font=font, fill=0, spacing=1)
    else: draw.text((0, 0), out_text, font=font, fill=255, spacing=1)
    if not args.video: new_filename = args.file + '-ascii.png'
    else: new_filename = args.file
    new.save(new_filename)
    if not args.video: print("The converted image can be found at: %s" % new_filename)

parser = argparse.ArgumentParser(description="Converts an image to ASCII characters.")
parser.add_argument('--foreach', dest='foreach', action='store_true', default=False, help="converts *each* pixel to an ASCII character (disabled).")
parser.add_argument('--dark', dest='dark', action='store_true', default=False, help="creates the image with dark background")
parser.add_argument('--video', dest='video', action='store_true', default=False, help="converts a video instead")
parser.add_argument('file', help="the original file")
args = parser.parse_args()

horizontal = 6
vertical = 10



if not args.dark: chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
else: chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
converter = (len(chars) - 1) / 255

print("Converting %s to ASCII art..." % args.file)

if not args.video:
    convert_image(args, args.file)
else:
    fps = get_fps(args.file)


