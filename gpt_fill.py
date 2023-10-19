import openai
import diskcache
import sqlite3
import wave
import pyaudio
import threading

cache = diskcache.Cache('/home/Vyshnavi/Desktop/pytree/talktree/cat_cache')
file_path="/home/Vyshnavi/Desktop/pytree/talktree/audios/Got you.wav"

def fill_play(file_path):
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
thread_play = threading.Thread(target=fill_play, args=(file_path,))

def func(text):
    conn = sqlite3.connect('/home/Vyshnavi/Desktop/pytree/talktree/instance/database.db')
    cursor = conn.cursor()
    select_query = '''
            SELECT shop_name, shop_address
            FROM shopping_list;
        '''
    cursor.execute(select_query)
    list_1= cursor.fetchall()
    print(list_1)
    system="You're a highly smart robot tree assistant that can do calculations like Einstein. you will reply, considering your shopping list"
        #Assistant=None
    var_1=(f"My shop list is = {list_1} \nSYSTEM: {system}\nUSER: {text}\nASSISTANT:")
        
    if text in cache:
        print("retrived from cache!!!!")
        return cache[text]
    else:
              #fill_play("/home/Vyshnavi/Desktop/pytree/talktree/process.wav")
              thread_play = threading.Thread(target=fill_play, args=(file_path,))
              thread_play.start()
              openai.api_key = "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"
              response = openai.Completion.create(
              model="text-davinci-003",
              prompt=var_1,
              temperature=0.3,
              max_tokens=80,
              top_p=1,
              frequency_penalty=0,
              presence_penalty=0
              )
              response_text = response["choices"][0]["text"]
              if "ASSISTANT:" in response_text:
                    response_text=response_text.replace("ASSISTANT:","")
                    cache[text] = response_text
              return response_text
#text="where i can buy necklace"
"""text="where i can buy jil"
system="You are an incredibly intelligent robotic tree assistant with the ability to perform calculations and possessing the brilliance of Einstein's mind."
Assistant=None"""
#var_1=(f"My shop list is = {list_1} \nSYSTEM: {system}\nUSER: {text}\nASSISTANT: {Assistant}\n")
#print(func(text))


