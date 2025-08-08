from AppOpener import close, open as appopen 
from webbrowser import open as webopen 
from pywhatkit import search, playonyt 
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print 
from groq import Groq
import webbrowser
import subprocess 
import requests 
import keyboard 
import asyncio 
import os 

# Load environment variables
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")


# Classes and headers
classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "gsrt vk_bk FzvWSb Ywphnf", "IZ6rdc", 
           "05uR6d LTKOO", "vlzY6d", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "-webanswers_table_webanswers-table", "Lwkfke", "VQF4g", "qv3Wpe", 
           "kno-rdesc", "SPZz6b", "dDoNo ikb48b gsrt", "sXLa0e"]

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"

client = Groq(api_key=GroqAPIKey)


professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need—don't hesitate to ask.",
]

# Chat memory
messages = []

SystemChatBot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]



# Google Search Function
def GoogleSearch(topic):
    search(topic)  
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.popen([default_text_editor,File])
    def ContententWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model = "mictral-8*7b-32768",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer =""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                answer += chunk.choices[0].delta.content
        answer = answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": answer})
        return answer

    Topic: str = Topic.replaced("Content", "")
    ContentByAI =ContententWriterAI(Topic)

      
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad("Data\{topic_clean.lower().replace(' ','')}.txt")
    return True



# YouTube Search Functionj
def YouTubeSearch(topic):
    UrlSearch = f"https://www.youtube.com/results?search_query={topic}"
    webbrowser.open(UrlSearch)
    return True

# Play YouTube Function
def PlayYoutube(query):
    playonyt(query)
    return True

# Open App Function
def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except :

        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'wckrlb'})
            return [link.get('href') for link in links]


        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = requests.get(url, headers=headers)
            
            if  response.status_code == 200:
                 return response.text
            else:
                print("Failed to recive search results.")
            return None
        html = search_google(app)
        if html:
            link = extract_links(html)[0]
            webopen(link)
        return True
    
def CloseAPP(app):
    if"chrome" in app:
        pass
    else:
        try:
            close(app, match_closer=True, output=True, throw_error=True)
            return True
        except :
            return False 
        
def System(command):
    
    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume unmute")

    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")

    if command == "mute":
        mute()
    
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":   
        volume_down() 
    
    return True
    

async def TranslateAndExecute(commands: list[str]):

    funcs = [] # List to store asynchronous tasks.

    for command in commands:
        if command.startswith("open"): # Handle "open" commands.

            if "open it" in command: # Ignore "open it" commands.
                 pass

            if "open file" == command: # Ignore "open file" commands.
                pass

            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "): 
            pass
        elif command.startswith("realtime "): 
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(PlayYoutube,command.removeprefix("close "))
            funcs.append(fun)
        
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content ") :
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube seach "): 
            fun = asyncio.to_thread(YouTubeSearch,command.removeprefix("youtube search "))
            funcs.append(fun)
        
        elif command.startswith("system "):
            fun = asyncio.to_thread(System,command.removeprefix("systen "))
            funcs.append(fun)

        else:
            print(f"No Function Found. For {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result
        

async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True
    
if __name__ == "__main__":
    pass