import json

from django.shortcuts import render, HttpResponse
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Create your views here.

def index(request):
    q = json.loads(request.GET.get("question"))

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=q['content'],
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    data = {
        "content": response['choices'][0].text
    }
    return HttpResponse(json.dumps(data))
