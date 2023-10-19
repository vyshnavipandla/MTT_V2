import diskcache
import boto3
import pyaudio
import mmap
#import time
# Create a disk cache instance with the dedicated folder path
cache_directory = 'cat_cache'
cache = diskcache.Cache(cache_directory)
polly = boto3.client('polly', aws_access_key_id="AKIAZIWBZDX3FK4J4K7K",
                     aws_secret_access_key="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", region_name="us-east-1")

#cache_directory = "cat_cache"
def mapy(text):
    # Check if the result is already in the cache
    if text in cache:
        print("Retrieved from cache")
        audio_data = cache[text]
    else:
        response = polly.synthesize_speech(Text=text, OutputFormat='pcm', VoiceId='Brian')
        audio_data = response['AudioStream'].read()

        # Store the result in the cache
        cache[text] = audio_data

    chunk_size = 4096
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=15000, output=True)
    with mmap.mmap(-1, len(audio_data), mmap.MAP_PRIVATE | mmap.MAP_ANONYMOUS) as mm:
        mm.write(audio_data)
        mm.seek(0)
        while True:
            data = mm.read(chunk_size)
            if not data:
                break
            stream.write(data)

    # Play the audio data directly from the cache
    offset = 0
    while offset < len(audio_data):
        chunk = audio_data[offset:offset + chunk_size]
        #stream.write(chunk)
        offset += chunk_size
         

    stream.close()
    pa.terminate()
    mm.close

# Call the function with the desired text
#while True:
#mapy("my name is dudu")
    #time.sleep(5)
