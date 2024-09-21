# Import the required module for text
# to speech conversion
import playsound
from gtts import gTTS
import mutagen
# This module is imported so that we can
# play the converted audio
import os, random, time, uuid
from mutagen.mp3 import MP3

audio_location=os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'temp'))

# print(audio_location)



# # The text that you want to convert to audio
# mytext = 'More human twins are being born now than ever before.'

# # Language in which you want to convert
# language = 'en'

# # Passing the text and language to the engine,
# # here we have marked slow=False. Which tells
# # the module that the converted audio should
# # have a high speed
# myobj = gTTS(text=mytext, lang='en', tld='co.in', slow=False)

# # Saving the converted audio in a mp3 file named
# # welcome
# audio_file_nam_loc = audio_location+"/VoiceOver"+str(uuid.uuid1())+".mp3"
# print(audio_file_nam_loc)
# myobj.save(audio_file_nam_loc)
# playsound.playsound(audio_file_nam_loc, True)
# # Playing the converted file

def convert_24khz_44khz(input_audio_location,output_audio_location):
    exe = "sox {} -r 44100 {}".format(input_audio_location,output_audio_location)
    stream = os.popen(exe)
    output = stream.read()
    print(output)     	

def voice_gen(text,lang,tld):

	# The text that you want to convert to audio
	mytext = text
	language = 'en'
	time.sleep(random.randint(2,5))
	myobj = gTTS(mytext, lang=lang, tld=tld, slow=False)
	audio_file_nam_loc = audio_location+"/VoiceOver"+str(uuid.uuid1())
	myobj.save(audio_file_nam_loc+"sr24khz.mp3")

	convert_24khz_44khz(audio_file_nam_loc+"sr24khz.mp3",audio_file_nam_loc+"sr44khz.mp3")



	mp3_audio = MP3(audio_file_nam_loc+"sr44khz.mp3")
	mp3_audio_info = mp3_audio.info
	print(mp3_audio_info.length)
	report={}
	report["file_url"]=audio_file_nam_loc+"sr44khz.mp3"
	report["length"]=mp3_audio_info.length
	print(report)
	return report









