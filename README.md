# ascii-artist

## Overview
This is a little program that can convert an image or an .mp4 video file to ASCII-art. I made it primarily for myself so don't expect the code to be very well-documented, readable or consistent. 

## Requirements
This program only runs on Windows and requires the [ffmpeg program](https://ffmpeg.org/) installed and added to PATH. The ffmpeg-python and Pillow packages are also needed.

## Usage
This program runs in cmd. For more information, you can use the built-in help option.

    ...\ascii-artist> py ascii-artist.py -h

### Recommendations
 - Don't use very high resolution images. It's pointless. See [limitations.](#limitations)
 - Using small, very low-resolution images doesn't make much sense either.
 - The program works best with high contrast, not too high resolution images.
 - "Dark mode" usually produces clearer images.

## Limitations
This program is really simple, so it has some fair limitations:
 - The higher the resolution, the more characters the generated image will have, up to the point where the individual characters may not be visible. (THe program can't rescale images.)
 - It takes a lot of time to generate videos, especially if they are long or have high resolution.
 - The program is *really* inefficient.
