import json

from django.shortcuts import render, HttpResponse
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Create your views here.

def index(request):
    print(request.GET['question'])
    q = request.GET['question']

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=q,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response)
    oldStr = response['choices'][0].text
    print(oldStr)
    newStr = oldStr.replace("\n+", "\n")
    print(newStr)
    data = {
        "content": newStr
    }

    return HttpResponse(json.dumps(data))


def test(request):
    return render(request, "index.html")
