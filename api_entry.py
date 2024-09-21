#!/usr/bin/env python3

import logging
import os
import json
import VoiceOver
import slideshow.cli as cli
from slideshow.SlideManager import SlideManager
import os, shutil,subprocess
import srt
from datetime import timedelta


# Logging
logger = logging.getLogger("kburns-slideshow")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/kburns-slideshow.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


ip = {'facts':[
                {
                    'images':[
                            
                            "/home/anishmohan/Pictures/2.jpg"

                            ],
                    'text':'This is a slide of just one picture as you can see.'    
                },
                {
                    'images':[
                            "/home/anishmohan/Pictures/3.jpg",
                            "/home/anishmohan/Pictures/4.jpg"

                            ],
                    'text':'In the following program, we create a list of length 2, there are two pictures here one after another'          
                },
                {
                    'images':[
                            "/home/anishmohan/Pictures/1.jpg",
                            "/home/anishmohan/Pictures/2.jpg",
                            "/home/anishmohan/Pictures/5.jpg"

                            ],
                    'text':'In the last slide, there we have three slide and a lots of textual information. So here we can conclude the presentation as which is the final presentation'         
                }
              ],
       'overlay_png': '/home/anishmohan/Documents/cov1.png',
       'music':'/home/anishmohan/Documents/works/smallmusic.mp3',
       'music_volume':0.25,
       'subtitle_config':{
                            'font_size':20,
                            'font_name':'DejaVu Sans',
                            'font_color':'FF7D39'

                        },
        'intro_video':'/home/anishmohan/Documents/works/intro.mp4',
        'outro_video':'/home/anishmohan/Documents/works/outro.mp4',
        'lang':'en',
        'tld':'co.in'                      
    }

def hex_color_fix(hex_color):
    output="".join(reversed([hex_color[i:i+2] for i in range(0, len(hex_color), 2)]))
    return output

def into_outro_concat(intro_video,content_video,outro_video,output_video):
    my_file = open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'temp'))+"/catlist.txt", "w")
    text_list = ["file '"+intro_video+"'\n", "file '"+content_video+"'\n", "file '"+outro_video+"'\n"]
    my_file.writelines(text_list)
    my_file.close()

    exe = "ffmpeg -f concat -safe 0 -i {} -c copy {}".format(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'temp'))+"/catlist.txt",output_video)
    print(exe)
    subprocess.call(exe, shell=True)

def split_sentence(sentence,split_by_number):

    sentence_list = []
    split_by_nth_word = split_by_number
    chunk = ""
    i=0
    for s in sentence.split():
        chunk=chunk+" "+s
        i+=1
        if i>split_by_nth_word:
            sentence_list.append(chunk)
            chunk=""
            i=0

    if len(chunk)>0:        
        sentence_list.append(chunk)
    return sentence_list

def subtitle_gen(slides):
    subtitles = []
    str_start_time = timedelta(seconds=0)
    str_last_time = timedelta(seconds=0)
    index = 1

    for slide in slides:
        
        slide_duration = slide['duration']
        text = slide['text']
        if len(text)>45:
            slices=split_sentence(text,8)
            for sub_slice in slices:
                subtitles.append(srt.Subtitle(index, str_last_time, str_last_time+timedelta(seconds=slide_duration/len(slices)), sub_slice, proprietary=''))
                str_last_time = str_last_time + timedelta(seconds=slide_duration/len(slices))
                index+=1
        else:
            subtitles.append(srt.Subtitle(index, str_last_time, str_last_time+timedelta(seconds=slide_duration), text, proprietary=''))
            str_last_time = str_last_time + timedelta(seconds=slide_duration)
            index+=1

    srt_file=srt.compose(subtitles, reindex=True, start_index=1, strict=True, eol=None, in_place=False)
    f = open(os.path.dirname(os.path.realpath(__file__)) + '/temp/subtitles.srt', "w")
    f.write(srt_file)
    f.close()

def parser1(ip):
    slide=[]
    clear_temp()
    for fact in ip['facts']:
        
        vo_text=fact["text"]
        vo_result=VoiceOver.voice_gen(vo_text,ip['lang'],ip['tld'])
        # fact.add('VoiceOver',vo_result['file_url'])
        # fact.add('duration',vo_result['length'])

        fact['VoiceOver']=vo_result['file_url']
        fact['duration']=vo_result['length']
        slide.append(fact)
    print("SlideManager")
    print(slide)# modified input dict with audio files and durations
    subtitle_gen(slide) # create subtitle andsave in temp folder
    input_files = video_initializer(slide) #pass the op to sm object as input_files

    # output_file = "/home/anishmohan/Documents/abc.mp4"
    output_file = os.path.dirname(os.path.realpath(__file__)) + '/final_out/music_less.mp4'
    audio_files = []
    for fact in slide:
        audio_files.append(fact['VoiceOver'])
    config = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:
        config = json.load(config_file)

    sm = SlideManager(config, input_files, audio_files)
    sm.createVideo(output_file, True, config["save"], config["test"], config["overwrite"])        
    
    music_clear_stat= clear_music(ip['music'],os.path.dirname(os.path.realpath(__file__)) + '/final_out/cleared_music.mp3')
    input_video_loc = os.path.dirname(os.path.realpath(__file__)) + '/final_out/music_less.mp4'
    input_audio_loc = os.path.dirname(os.path.realpath(__file__)) + '/final_out/cleared_music.mp3'
    output_location = os.path.dirname(os.path.realpath(__file__)) + '/final_out/FINAL_MASTER.mp4'
    final_bgm_mix(input_video_loc,input_audio_loc,output_location,ip['music_volume'])

    overlay_output_location = os.path.dirname(os.path.realpath(__file__)) + '/final_out/OVERLAY_FINAL_MASTER.mp4'
    subtitle_location = os.path.dirname(os.path.realpath(__file__)) + '/temp/subtitles.srt'
    # png_location = os.path.dirname(os.path.realpath(__file__)) + '/final_out/FINAL_MASTER.mp4'
    png_location = ip['overlay_png']
    overlay_png_sub(output_location,png_location,subtitle_location,overlay_output_location,ip['subtitle_config']['font_size'],ip['subtitle_config']['font_name'],hex_color_fix(ip['subtitle_config']['font_color']))    
    final_video_ouput_location = os.path.dirname(os.path.realpath(__file__)) + '/final_out/UPLOAD_FINAL_MASTER.mp4'
    into_outro_concat(ip['intro_video'],overlay_output_location,ip['outro_video'],final_video_ouput_location)

def overlay_png_sub(input_video_location,png_location,srt_location, output_location,sub_font_size,sub_font_name,sub_font_color):
    exe = "ffmpeg -i {} -i {} -filter_complex \"[0][1]overlay=0:0,subtitles={}:force_style='Fontsize={},FontName={},PrimaryColour=&H{}&'\" -c:a copy {}".format(input_video_location,png_location,srt_location,sub_font_size,sub_font_name,sub_font_color,output_location)
    stream = os.popen(exe)
    output = stream.read()
    print(output)        

def final_bgm_mix(input_video_loc,input_audio_loc,output_location,audio_volume):
    exe = "ffmpeg -i {} -filter_complex \"amovie={}:loop=0,asetpts=N/SR/TB,volume={}[aud];[0:a][aud]amix[a]\" -map 0:v -map '[a]' -c:v copy -c:a aac -b:a 256k -shortest {}".format(input_video_loc,input_audio_loc,audio_volume,output_location)
    stream = os.popen(exe)
    output = stream.read()
    print(output)
# baked_slide = [    {        "images": ["/home/anishmohan/Pictures/2.jpg"],        "text": "In the following program, we create a list of length 3",        "VoiceOver": "/home/anishmohan/Documents/Workspace/kburns-slideshow/temp/VoiceOver520817f0-b96f-11eb-8d19-9381e23dc401.mp3",        "duration": 4.632,    },    {        "images": [            "/home/anishmohan/Pictures/3.jpg",            "/home/anishmohan/Pictures/4.jpg",        ],        "text": "In the following program, we create a list of length 3, where all the three elements are of type dict.",        "VoiceOver": "/home/anishmohan/Documents/Workspace/kburns-slideshow/temp/VoiceOver537955cc-b96f-11eb-8d19-9381e23dc401.mp3",        "duration": 7.896,    },    {        "images": [            "/home/anishmohan/Pictures/1.jpg",            "/home/anishmohan/Pictures/2.jpg",            "/home/anishmohan/Pictures/5.jpg",        ],        "text": "In the following program, we create a list of length 3, where all the three elements are of type dict.",        "VoiceOver": "/home/anishmohan/Documents/Workspace/kburns-slideshow/temp/VoiceOver55fac59c-b96f-11eb-8d19-9381e23dc401.mp3",        "duration": 7.896,    },]
def clear_music(input_music_location,output_music_location):
    exe="ffmpeg -i {} -af \"silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=1:start_threshold=-60dB:detection=peak,aformat=dblp,areverse\" {}".format(input_music_location,output_music_location)
    print("XXXXXXXXXXXXXXXX problem is here")
    print(exe)
    stream = os.popen(exe)
    output = stream.read()
    print(output)
    return output

def clear_temp():
    try: 
        dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'temp'))
        print(dir)
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
        dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'final_out'))
        print(dir)
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)        
           
                 
    except:
        pass    


def image_clip_designer(image_loc,clip_duration):
    template_dict={
                    "file": "/home/anishmohan/Documents/Workspace/kburns-slideshow/data/2.jpg",
                    "slide_duration": 6.0,
                    "slide_duration_min": 1.0,
                    "fade_duration": 2,
                    "zoom_direction": "random",
                    "zoom_rate": 0.2,
                    "scale_mode": "crop_center",
                    "transition": "fade",
                }
    template_dict['file']=image_loc
    template_dict['slide_duration']=round(clip_duration,1)
    return template_dict   

def video_initializer(baked_slide):
    whole=[]
    for fact in baked_slide:
        fact_duration = fact['duration']

        per_slide_duration = fact_duration/len(fact['images'])
        for image in fact['images']:
            whole.append(image_clip_designer(image,per_slide_duration))
    return(whole)    


parser1(ip)
# input_video_loc = os.path.dirname(os.path.realpath(__file__)) + '/final_out/music_less.mp4'
# input_audio_loc = os.path.dirname(os.path.realpath(__file__)) + '/final_out/cleared_music.mp3'
# output_location = os.path.dirname(os.path.realpath(__file__)) + '/final_out/FINAL_MASTER.mp4'
# final_bgm_mix(input_video_loc,input_audio_loc,output_location) 
         
# input_files=video_initializer(baked_slide)
# output_file = "/home/anishmohan/Documents/abc.mp4"
# audio_files = []
# config = {}
# with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:
#         config = json.load(config_file)

# sm = SlideManager(config, input_files, audio_files)
# sm.createVideo(output_file, True, config["save"], config["test"], config["overwrite"])        



# if __name__ == "__main__":

#     config = {}
#     with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:
#         config = json.load(config_file)

#     command_line = cli.CLI(config)
#     config, input_files, audio_files, output_file = command_line.parse()


#     print('XAXAXAXAX')
#     print('config')
#     print(config)
#     print('input_files')
#     print(input_files)
#     print('audio_files')
#     print(audio_files)
#     print('output_file')
#     print(output_file)
#     print('command_line')
#     print(command_line)
#     print('____________________')

#     sm = SlideManager(config, input_files, audio_files)
#     print('????????????????????')
#     print(config)
#     print(input_files)
#     print(audio_files)


#     if config["sync_to_audio"]:
#         logger.info("Sync slides durations to audio")
#         sm.adjustDurationsFromAudio()

#     sm.createVideo(output_file, True, config["save"], config["test"], config["overwrite"])
