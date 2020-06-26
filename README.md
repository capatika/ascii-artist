# ascii-artist

## Overview
This is a little program that can convert an image or an .mp4 video file to ASCII-art. 

## Requirements
This program only runs on Windows and requires the ffmpeg program installed and added to PATH.

## Usage
This program runs in cmd. For more information, you can use the built-in help option.

    ...\ascii-artist> py ascii-artist.py -h

### Recommendations
 - Don't use very high resolution images. It's pointless. See [limitations.](#limitations) 
 - The program works best with high contrast, not too high resolution images.
 - "Dark mode" usually produces clearer images.

## Limitations
This program is really simple, so it has some fair limitations:
 - The higher the resolution, the more characters the generated image will have, up to the point where the individual characters may not be visible.
 - It takes a lot of time to generate videos, especially if they are long or have high resolution.
