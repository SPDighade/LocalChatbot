# chatbot_project/chatbot_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Chatbot, ChatbotTraining
import os
import json

# Initialize training instance
# Usage Example:
translation_model_name = "Helsinki-NLP/opus-mt-en-es"
source_language_code = "es"
target_language_code = "en"
model_name = "/home/sdighade/chatbot/Model" #os.path.join('home', 'sdighde', 'chatbot', 'Model')#
folder_path = '/home/sdighade/chatbot/Data'
embedding_model_name = "sentence-transformers/all-mpnet-base-v2"

chatbot_training = ChatbotTraining(translation_model_name, source_language_code, target_language_code, model_name, folder_path, embedding_model_name)

# Store chatbot instance globally for simplicity


def home(request):
    return render(request, 'home.html')

def chat(request):
    if request.method == 'POST':
        chatbot_instance = Chatbot(translation_model_name, source_language_code, target_language_code,
                          chatbot_training.model, chatbot_training.tokenizer,
                          chatbot_training.retriever, chatbot_training.llm, [])
        #data = request.json()
        data = json.loads(request.body.decode('utf-8'))
        query = data.get('query', '')
        #query = "What is links Panel"
        use_spanish = data.get('use_spanish', '') == 'true'
        print("use_spanish1", use_spanish)
        print("Testing1")
        if use_spanish:
            print("use_spanish0", use_spanish)
            translated_query = chatbot_instance.translate(query)
        else:
            print("use_spanish2", use_spanish)
            translated_query = query
            print("Testing2")

        response, chat_history = chatbot_instance.create_conversation(translated_query)
        print("Testing3")
        print(response)
        print("Testing3.1", chat_history)
        if use_spanish:
            translated_response = chatbot_instance.translate(response)
        else:
            print("Testing4")
            translated_response = response
        print("Testing5")
        return JsonResponse({'response': translated_response, 'chat_history': chat_history})

        #print(jresponse)
        #return render(request,'display.html',{'content':chat_history})
        #print("Testing6")
    #print(jresponse)
    return render(request, 'chat.html')
