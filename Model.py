import cohere

from rich import print
from dotenv import dotenv_values 
 
env_vars = dotenv_values(".env")

CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

funcs = [
    "exit","general","realtime","open","close","play",
    "generate","image","sytem","content","google search","youtube search","reminder"]

message= []

preamble= """
 You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task or automation like 'open facebook, ins
***Do not answer any query, just decide what kind of query is given to you***
→ Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date info.
→ Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data and requires up to date
→ Respond with 'open (application name or website name)' if a query is asking to open any application like 'open facebook', 'open telegram', etc.
→ Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the
→ Respond with 'play (song name)' if a query is asking to play any song like 'play afsanay by ys', 'play let her go', etc. but if the query is a
→ Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a Lion',
→ Respond with 'system (task name)' if a query is asking to mute, unmute, volume up, volume down, etc. but if the query is asking
→ Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a spec
→ Respond with 'google search (topic)' if a query is asking to search a specific topic on google but if the query is asking to search multiple
→ Respond with 'youtube search (topic)' if a query is asking to search a specific topic on youtube but if the query is asking to search multiple
If the query is asking to perform multiple tasks like 'open facebook, telegram and close whatsapp' respond with 'open facebook, open telegram 

if the user is saying goodbye or want to end coversation like 'bye jarvis. ' respond with 'exit'.
respond with 'general (querey)' if you can't decide the kind of query or if a query is asking to perform a tasl which is not   mentioned above.

"""

ChatHistory=[
    {"role": "User", "message": "how are you?"},
    {"role": "Chatbot", "message": "general how are you?"},
    {"role": "User", "message": "do you like pizza?"},
    {"role": "Chatbot", "message": "general do you like pizza?"},
    {"role": "User", "message": "open chrome and tell me about mahatma gandhi."},
    {"role": "Chatbot", "message": "open chrome, general tell me about mahatma gandhi."},
    {"role": "User", "message": "open chrome and firefox"},
    {"role": "Chatbot", "message": "open chrome, open firefox"},
    {"role": "User", "message": "what is today's date and by the way remind me that i have a dancing performance on 5th aug at 11pm"},
    {"role": "Chatbot", "message": "general what is today's date, reminder 11:00pm 5th aug dancing performance"},
    {"role": "User", "message": "chat with me."},
    {"role": "Chatbot", "message": "general chat with me."}
]


def FirstLayerDMM(prompt: str="test"):

    message.append({"role":"user","content": f"{prompt}"})

    stream= co.chat_stream(
        model='command-r-plus',
        message =prompt,
        temperature=0.7,
        chat_history=ChatHistory,
        prompt_truncation='OFF',
        connectors=[],
        preamble=preamble
    )


    response=""

    for event in stream:
        if event.event_type == "text-generation" :  
           response += event.text
    
    
    response = response.replace("\n","")
    response = response.split(",")

    response = [i.strip() for i in response]

    temp = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)


    response = temp

    if "(query)" in response  :
        newresponse = FirstLayerDMM(Prompt=prompt)  
        return newresponse
    else:
        return response

if __name__ == "__main__" :
    while True:
        print(FirstLayerDMM(input(">>>  "))) 
