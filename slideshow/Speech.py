# Import the required module for text
# to speech conversion
import playsound
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os, random

audio_location=os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'temp'))





# The text that you want to convert to audio
mytext = 'More human twins are being born now than ever before.'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang='en', tld='co.in', slow=False)

# Saving the converted audio in a mp3 file named
# welcome
audio_file_nam_loc = audio_location+str(random.randint(3,9))
myobj.save(audio_file_nam_loc)
playsound.playsound(audio_file_nam_loc, True)
# Playing the converted file

