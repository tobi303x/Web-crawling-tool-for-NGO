import os
import openai
import json
from dotenv import load_dotenv
import os


load_dotenv()




def Chat_GPT_API (GPT_Opis_Użytkownika, konkursy):
  openai.api_key = (os.getenv('CHAT_GPT_API_KEY'))

  response = openai.Completion.create(
    model="text-davinci-003",
    prompt="Na podstawie opisu użytkownika ->{GPT_Opis_Użytkownika}. Lista konkursów ->{konkursy}.Lista zawiera tytuły i opisy konkursów oddzielone znakami \";\"  tzn. (tytuł;opis).Na podstawie opisu użytkownika wybierz 5 najlepszych konkursów i podaj dlaczego to akurat lda niego zostały wybrane jako najlepsze, pamietaj o linkach do konkursów",
    temperature=1,
    max_tokens=1800,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )
  response = str(response)
  response_data = json.loads(response)
  completion_text = response_data['choices'][0]['text']
  return completion_text