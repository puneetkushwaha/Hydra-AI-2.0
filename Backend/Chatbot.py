from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data\Chatlog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:

    with open(r"Data\Chatlog.json", "w") as f:
        dump([], f)

def RealtimeInformation():
    Current_date_time = datetime.datetime.now()
    day = Current_date_time.strftime("%A")
    date = Current_date_time.strftime("%d")
    month = Current_date_time.strftime("%B")
    year = Current_date_time.strftime("%Y")
    hour = Current_date_time.strftime("%H")
    minute = Current_date_time.strftime("%M")
    second = Current_date_time.strftime("%S")

    data = f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += r"Time: {hour}\ hours: {minute}\ minutes: {second} Seconds. \n"
    return data


def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def ChatBot(Query):
    """This function sends the user's query to the chatbot and returns the AI's response."""

    try:
        with open(r"Data\Chatlog.json", "r") as f:
            messages = load(f)


        messages.append({"role": "user", "content": f"{Query}"})

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")

        messages.append({"role": "assistant", "content": Answer})

        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)


        return AnswerModifier(Answer=Answer)
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data\Chatlog.json", "w") as f:
            dump(messages, f, indent=4)
        return ChatBot(Query)
    

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question:")
        print(ChatBot(user_input))