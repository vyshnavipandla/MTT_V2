''' Newly updated code of testing file,used fuzzy method for weather,database
added wifi & ip address.
last tested and edited on 13/10/2023''' 

import RPi.GPIO as GPIO
import pyaudio
from polly_triles import mapy
import time
import websockets
import asyncio
import base64
import json
import datetime
import pvporcupine
import struct
import pyaudio
import asyncio
import threading
import wave
import sqlite3
import webbrowser
import os
import datetime
import subprocess
from sample_fuzzy import*
from fuzzywuzzy import fuzz
from gpt_fill import*
#from var_1 import*
GPIO.setmode(GPIO.BCM)
FRAMES_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
conn = sqlite3.connect('/home/Vyshnavi/Desktop/pytree/talktree/instance/database.db') 
cur = conn.cursor()

p = pyaudio.PyAudio()
audio_stream=None
var=0
GPIO.setwarnings(False)

led_blue = 17
led_green=27
led_red=22

GPIO.setup(led_blue, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(led_red, GPIO.OUT)


def wifi_connected():
    text = subprocess.check_output(["iwconfig", "wlan0"]).decode("utf-8")
    if "ESSID:off/any" in text:
        print("wifi not connected!!")
        GPIO.output(led_red,GPIO.HIGH)
        return True
    else:
        essid_line = [line for line in text.split('\n') if "ESSID:" in line][0]
        essid = essid_line.split('ESSID:')[1].split('"')[1]
        GPIO.output(led_red,GPIO.LOW)
        print("wifi is connected and ESSID is: ",essid)
        return False
        
while(wifi_connected()):
	continue
      
def play_audio_file(file_path):
    wf = wave.open(file_path, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)
    
    stream.close()  
    p.terminate()

def start_audio_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=3200)
    return p, stream
def stop_audio_stream():
    global p, audio_stream  
    if p and audio_stream:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        p = None
        audio_stream = None
    
def start_audio_stream_pro():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=3200)
    return p, stream
def stop_audio_stream_pro():
    global p, audio_stream  
    if p and audio_stream:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()
        p = None
        audio_stream = None

auth_key='33897f62cddd4a0cae379195659d39c4'


URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"
runner=False 
async def send_receive():
   global p,audio_stream
   p, audio_stream = start_audio_stream()
   print(f'Connecting websocket to url ${URL}')
   global runner
   async with websockets.connect(
       URL,
       extra_headers=(("Authorization", auth_key),),
       ping_interval=5,
       ping_timeout=20
   ) as _ws:
       print("While socket :",runner)
       
       await asyncio.sleep(0.1)
       runner=True
       print("Receiving SessionBegins ...")
       session_begins = await _ws.recv()
       print(session_begins)
       print("Sending messages ...")
       async def send():
           global runner
           global p,audio_stream
           while runner:
               try:
                   data = audio_stream.read(FRAMES_PER_BUFFER)
                   data = base64.b64encode(data).decode("utf-8")
                   json_data = json.dumps({"audio_data":str(data)})
                   await _ws.send(json_data)
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
               await asyncio.sleep(0.01)
           print("in Send fun :",runner)
           return True
       async def receive():
           global runner
           global var
           global stopper
           inc=0
           kut=0
           global p,audio_stream, var
           print("Recive fun :",runner)
           while runner:
               try:
                   result_str = await _ws.recv()
                   if(json.loads(result_str)['message_type']=='PartialTranscript'):
                            kut=kut+1
                            if kut==50:
                                runner=False
                                stopper=False
                                return "no data found"
                   elif(json.loads(result_str)['message_type']=='FinalTranscript'):
                       print(json.loads(result_str)['text'])
                       if(json.loads(result_str)['text'])=="":
                           print("No Data Found")
                           inc=inc+1
                           if inc==2:
                               runner=False
                               stopper=False
                               return "no data found"
                       
                            
                       else:
                            text=(json.loads(result_str)['text'])
                            txt=text.split()
                            if len(txt)<2:
                                continue
                            text=text.lower().replace(",", "").replace(".", "").replace("how can i help you","").replace("yes how can i help you","").replace("yes how can i help","").replace("?", "").strip()
                            print("user asked.....................",text)
                            stop_audio_stream()
                            runner=False
                            inc=0
                            
                            query = f"SELECT Question FROM core"
                            cur.execute(query)
                            data= cur.fetchall()
                            query_1=f"SELECT Question FROM user"
                            cur.execute(query_1)
                            data_user=cur.fetchall()
                            for i in data:
                                 match_rate=fuzz.ratio(i[0],text)
                                 #print("from core = ",match_rate)
                                 if match_rate>85:
                                     cur.execute("SELECT Answer FROM core WHERE Question=?", (i[0],))
                                     refer = cur.fetchone()
                                     #print(refer)
                                     if refer is not None:
                                         sample = refer[0]
                                         #print(sample)
                                         return sample
                                 
                                    
                            for j in data_user:
                                 match_rate=fuzz.ratio(j[0],text)
                                 #print ("from user = ",match_rate)
                                 if match_rate>85:
                                     cur.execute("SELECT Answer FROM user WHERE Question=?", (j[0],))
                                     result = cur.fetchone()
                                     #print(result)
                                     if result is not None:
                                         sample = result[0]
                                         #print(sample)
                                         return sample
                            else:
                              print("nodata found")
                              data=None
                              data_user=None
                              if 'play' in text:
                                  var=True
                                  cur.execute("SELECT id FROM vid_tab")
                                  IDs=cur.fetchall()
                                  for i in IDs:
                                      cur.execute('SELECT username FROM vid_tab WHERE id = ?', (i[0],))
                                      row=cur.fetchone()
                                      print(row)
                                      if row[0] in text:
                                        cur.execute("SELECT videoPath FROM vid_tab WHERE username = ?",(row[0],))
                                        video_path=cur.fetchone()
                                        os.system("open "+video_path[0])
                                        stopper=False
                                        var=1
                                        return "As you wish"
                              elif 'come back' in text:
                                  os.system("killall chromium-browser")
                                  os.system("pkill vlc")
                                  os.system("amixer sset Master 100%+")
                                  var=0
                                  stopper = False
                                  return "As you wish"
                              elif text=='stop':
                                  os.system("killall chromium-browser")
                                  os.system("pkill vlc")
                                  stopper=False
                                  return "As you wish"
                              elif ("image" or "images") in text:
                                webbrowser.open("https://www.google.com/search?q="+text+"&tbm=isch")
                                stopper=False
                                return "As you wish"
                              elif "time" in text:
                                timE=datetime.datetime.now()
                                return f"{timE.strftime('time is %H:%M and date is %B-%D')}"
                              elif "weather" or "forecast" or "whether" in text:
                                for syntax in list_weather:
                                    match_rate=fuzz.ratio(syntax,text)
                                    if match_rate>80:
                                      print(match_rate)
                                      return(weather_provider(text))
                              elif "currency" in text :
                                return "soon i will be updated with currency updates"
                              if text:
                                return(func(text))
                                inc=2
                            
               except websockets.exceptions.ConnectionClosedError as e:
                   print(e)
                   assert e.code == 4008
                   break
               except Exception as e:
                   assert False, "Not a websocket 4008 error"
       send_result, receive_result = await asyncio.gather(send(), receive())
       await _ws.close()
       return receive_result
porcupine = None
stopper=True
keyword_paths = ['/home/Vyshnavi/Desktop/pytree/talktree/hey-dudu_en_raspberry-pi_v2_2_0.ppn','/home/Vyshnavi/.local/lib/python3.9/site-packages/pvporcupine/resources/keyword_files/raspberry-pi/blueberry_raspberry-pi.ppn']

while True:
    try:
        porcupine = pvporcupine.create(keyword_paths=keyword_paths,
                                    access_key="yr01j3n+MWxpWdfnPXrpymyfql0/vyunQGd/mkVKUd7MMPLLzI5QXA==")
        p,audio_stream = start_audio_stream_pro()
        print("Listening...")
        
        while True:
            GPIO.output(led_blue,GPIO.HIGH)
            GPIO.output(led_green,GPIO.LOW)
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)

            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index == 1:
                text = subprocess.check_output(["iwconfig", "wlan0"]).decode("utf-8")
                if "ESSID:off/any" in text:
                    print("wifi not connected!!")
                    #return False
                else:
                    essid_line = [line for line in text.split('\n') if "ESSID:" in line][0]
                    essid = essid_line.split('ESSID:')[1].split('"')[1]
                    print("wifi is connected and ESSID is: ",essid)
                    play_audio_file("/home/Vyshnavi/Desktop/pytree/talktree/audios/Am connected to.wav")
                    for i in essid:
                        if i=='_':
                            play_audio_file("/home/Vyshnavi/Desktop/pytree/talktree/audios/undo.wav")
                        elif i==" ":
                            continue
                        else:
                            play_audio_file(f"/home/Vyshnavi/Desktop/pytree/talktree/audios/{i.upper()}.wav")
                play_audio_file("/home/Vyshnavi/Desktop/pytree/talktree/audios/And IP adress is.wav")
                result = subprocess.check_output("hostname -I | awk '{print $1}'", shell=True, text=True)
                print("ip address is....",result)
                for j in  result.strip():
                    print(j)
                    if j==".":
                            play_audio_file("/home/Vyshnavi/Desktop/pytree/talktree/audios/dot.wav")
                    else:
                            play_audio_file(f"/home/Vyshnavi/Desktop/pytree/talktree/audios/{j.upper()}.wav")
            elif keyword_index == 0:
                #print(runner)
                print("Keyword detected!")
                GPIO.output(led_green, GPIO.HIGH)
                GPIO.output(led_blue, GPIO.LOW)
                play_audio_file("/home/Vyshnavi/Desktop/pytree/talktree/audios/Messgae _alertwav.wav")
                if var==1:
                    os.system("amixer sset Master 60%-")
                    print("volume decreased")                  
                stopper=True
                while stopper:
                    x=asyncio.run(send_receive())
                    print("Response is..............",x)
                    mapy(x)
                    print("runner after asyn function",runner)
                    if audio_stream is None:
                        p,audio_stream = start_audio_stream_pro()
					
    except KeyboardInterrupt:
        print("\nStopping...")
        break
    finally:
        stop_audio_stream_pro()
        GPIO.cleanup()
        if porcupine is not None:
            porcupine.delete()






  


