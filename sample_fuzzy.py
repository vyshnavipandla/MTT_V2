''' New method for weather, "fuzzywuzzy" is used'''


from fuzzywuzzy import fuzz
from requests_html import*
import threading
from polly_triles import mapy
s= HTMLSession()


list_weather=["what is the weather in","what is the current weather in"
"what is the weather at","weather in","what's the weather forecast for",
"how is the weather looking in","do you have information about weather in",
"could you give me an update about weather in","what's the weather in",
"what is the weather forecast in","what is tomorrow's weather in","weather in","wheather in",
"whether in","give the weather in","tell me the weather in"]
	
def weather_provider(text):
	try:
		url= f"https://www.google.com/search?q={text}"
		r= s.get(url, headers={'User-Agent' : 'Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
		return(f"""hmm..its {r.html.find('span#wob_tm.wob_t.q8U8x',first=True).text}°C and a moderate level of humidity {r.html.find('span#wob_hm',first=True).text}
 while the wind speed is {r.html.find('span#wob_ws.wob_t',first=True).text}""")
	
	except AttributeError:
		return("sorry i am not understand your question")
	except requests.exceptions.ConnectionError:
		return("Am facing difficility in network")

def Get_weather(text):
	for i in list_weather:
		match_rate=fuzz.ratio(i,text)
    #print(f"{text} and elements is == {fuzz.ratio(i,text)}")
		if match_rate>80:
			#print(match_rate,text)
			print("processed text...",text)
			break
	if match_rate:
		return weather_provider(text)
	else:
		return "Please use proper syntax"
#Get_weather("what is weather in chenniah")
    


'''def weath(text):
	try:
		url= f"https://www.google.com/search?q={text}"
		r= s.get(url, headers={'User-Agent' : 'Mozilla/5.0 (X11; CrOS aarch64 13597.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'})
		print("hmm.."+text+ r.html.find('span#wob_tm.wob_t.q8U8x',first=True).text+
        " °C and a moderate level of humidity "+r.html.find('span#wob_hm',first=True).text+
        " while the wind speed is "+
        r.html.find('span#wob_ws.wob_t',first=True).text)
	
	except AttributeError:
		return("The attribute my_attribute does not exist on my_object")
	except requests.exceptions.ConnectionError:
		print("Network error")
#weath(text)'''
