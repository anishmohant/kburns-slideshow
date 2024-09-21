#!/usr/bin/env python3

import logging
import os
import json

import slideshow.cli as cli
from slideshow.SlideManager import SlideManager

# Logging
logger = logging.getLogger("kburns-slideshow")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/kburns-slideshow.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == "__main__":

    config = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:
        config = json.load(config_file)

    command_line = cli.CLI(config)
    config, input_files, audio_files, output_file = command_line.parse()


    print('XAXAXAXAX')
    print('config')
    print(config)
    print('input_files')
    print(input_files)
    print('audio_files')
    print(audio_files)
    print('output_file')
    print(output_file)
    print('command_line')
    print(command_line)
    print('____________________')

    sm = SlideManager(config, input_files, audio_files)
    print('????????????????????')
    print(config)
    print(input_files)
    print(audio_files)


    baked_config={'ffmpeg': 'ffmpeg', 'ffprobe': 'ffprobe', 'aubio': 'aubioonset', 'IMAGE_EXTENSIONS': ['jpg', 'jpeg', 'png'], 'VIDEO_EXTENSIONS': ['mp4', 'mpg', 'avi'], 'AUDIO_EXTENSIONS': ['mp3', 'ogg', 'flac'], 'output_width': 1280, 'output_height': 800, 'output_codec': 'libx264', 'output_parameters': '-preset ultrafast -tune stillimage', 'slide_duration': 4, 'slide_duration_min': 1, 'fade_duration': 1, 'transition': 'random', 'transition_bars_count': 10, 'transition_cell_size': 100, 'fps': 60, 'zoom_rate': 0.1, 'zoom_direction': 'random', 'scale_mode': 'auto', 'loopable': False, 'overwrite': False, 'generate_temp': False, 'delete_temp': False, 'temp_file_folder': 'temp', 'temp_file_prefix': 'temp-kburns-', 'sync_to_audio': False, 'save': None, 'test': False, 'is_synced_to_audio': False}
    baked_input_files=['/home/anishmohan/Documents/Workspace/kburns-slideshow/data/1.jpg', '/home/anishmohan/Documents/Workspace/kburns-slideshow/data/2.jpg', '/home/anishmohan/Documents/Workspace/kburns-slideshow/data/3.jpg']
    baked_audio_files=[]

    if config["sync_to_audio"]:
        logger.info("Sync slides durations to audio")
        sm.adjustDurationsFromAudio()

    sm.createVideo(output_file, True, config["save"], config["test"], config["overwrite"])
