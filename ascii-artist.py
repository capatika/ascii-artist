from PIL import Image, ImageDraw, ImageFont
from statistics import mean
import argparse, ffmpeg, os, subprocess, shutil

def get_info(original):
    print("Getting video information...")

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
        frame_num = int(video_stream['nb_frames'])
    except KeyError:
        print('                                                      ', end='\r')
        print("The file specified is not a video.")
        raise SystemExit
    fps_list = avg_frame_rate.split('/')
    fps = round(float(fps_list[0]) / float(fps_list[1]), 2)

    print('                                                      ', end='\r')
    return {'fps': fps, 'frame_num': frame_num}


def get_frames(original: str, fps: float):
    print('                                                      ')
    print('Extracting frames...')

    output = 'data\\frames\\' + original.split('\\')[-1].split('.')[0] + '\\'
    if not os.path.exists(output): os.makedirs(output)

    query = "ffmpeg -i " + original + " -vf fps=" + str(fps) + " " + output + "%06d.png"
    response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
    s = str(response).encode('utf-8')
    '' + str(s)  # this is just here so that vscode doesn't detect s as 'unused'. it doesn't actually do anything.

    return output


def get_audio(original: str):
    print('                                                      ', end='\r')
    print('Extracting audio...')
    output = 'data\\audio\\' + original.split('\\')[-1].split('.')[0]
    if not os.path.exists(output): os.makedirs(output)
    subprocess.call(['ffmpeg', '-i', original, '-codec:a', 'pcm_s16le', '-ac', '1', output + '\\audio.wav'])
    return output + '\\audio.wav'


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
            if args.video: print('Converting frames: Progress: {:.0f}% | {:.0f}%'.format((row * col) / (height * width) * 100, progress), end='\r')
            else: print('Progress: {:.0f}%'.format((row * col) / (height * width) * 100), end='\r')
    else:
        print("This feature is currently disabled.")
    print('                                                                                      ', end='\r')
    if args.video: print('Converting frames: Saving... | {:.0f}%'.format(progress), end='\r')
    else: print('Saving...', end='\r')
    if not args.dark: draw.text((0, 0), out_text, font=font, fill=0, spacing=1)
    else: draw.text((0, 0), out_text, font=font, fill=255, spacing=1)
    if not args.video: new_filename = args.file + '-ascii.png'
    else: new_filename = convertable
    new.save(new_filename)
    if not args.video: print("The converted image can be found at: %s" % new_filename)

def construct_video(args, frame_loc: str, audio_loc: str, fps: float):
    print('                                                                                      ', end='\r')
    print('Constructing video...')
    video_loc = 'data\\video\\' + args.file.split('\\')[-1].split('.')[0]
    if not os.path.exists(video_loc): os.makedirs(video_loc)
    subprocess.call(['ffmpeg', '-framerate', str(fps), '-i', frame_loc + '%06d.png', '-pix_fmt', 'yuv420p', video_loc + '\\video.mp4'])
    new_filename = args.file + '-ascii.mp4'
    subprocess.call(['ffmpeg', '-an', '-i', video_loc + '\\video.mp4', '-vn', '-i', audio_loc, '-c:v', 'copy', new_filename])
    print('The video can be found at: %s' % new_filename)


def clean_up():
    shutil.rmtree('data')


parser = argparse.ArgumentParser(description="Converts an image to ASCII characters.")
parser.add_argument('--foreach', dest='foreach', action='store_true', default=False, help="Converts *each* pixel to an ASCII character (disabled).")
parser.add_argument('--dark', dest='dark', action='store_true', default=False, help="Creates the image with dark background")
parser.add_argument('--video', dest='video', action='store_true', default=False, help="Converts a video instead. This may take a while.")
parser.add_argument('file', help="the original file")
args = parser.parse_args()

horizontal = 6
vertical = 10

if not args.dark: chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
else: chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
converter = (len(chars) - 1) / 255

print("Converting %s to ASCII art..." % args.file)

if not args.video:
    try:
        convert_image(args, args.file)
    except KeyboardInterrupt:
        print('\nCancelled.')
        clean_up()
        raise SystemExit
else:
    try:
        fps, frame_num = get_info(args.file)['fps'], get_info(args.file)['frame_num']
        frame_location = get_frames(args.file, fps)
        audio_location = get_audio(args.file)
        for frame in range(frame_num):
            convert_image(args, frame_location + '{:06d}'.format(frame + 1) + '.png', frame / frame_num * 100)
        construct_video(args, frame_location, audio_location, fps)
        clean_up()
    except KeyboardInterrupt:
        print('\nCancelled.')
        clean_up()
        raise SystemExit
