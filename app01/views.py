import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, HttpResponse
import os
import openai
from dotenv import load_dotenv
import replicate

load_dotenv()
model = replicate.models.get("openai/whisper")
version = model.versions.get("23241e5731b44fcb5de68da8ebddae1ad97c5094d24f94ccb11f7c1d33d661e2")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")


# Create your views here.

@csrf_exempt
def index(request):
    print(request.GET)
    q = request.GET['question']
    codex_model = request.GET['model']
    print(codex_model)
    max_token = int(request.GET['maxToken'])
    temperature = float(request.GET['temperature'])
    response = openai.Completion.create(
        model=codex_model,
        prompt=q,
        temperature=temperature,
        max_tokens=max_token,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response)
    oldStr = response['choices'][0].text
    # print(oldStr)
    newStr = oldStr.replace("\n+", "\n")
    print(newStr)
    data = {
        "content": newStr
    }

    return HttpResponse(json.dumps(data))

@csrf_exempt
def test(request):
    return render(request, "index.html")


@csrf_exempt
def whisper(request):
    print(request.GET['name'])
    filepath = "C:\\CloudMusic\\"+request.GET['name']
    whisper_model = request.GET['model']

    inputs = {
        # Audio file
        'audio': open(filepath, "rb"),

        # Choose a Whisper model.
        'model': whisper_model,

        # Choose the format for the transcription
        'transcription': "plain text",

        # Translate the text to English when set to True
        'translate': False,

        # language spoken in the audio, specify None to perform language
        # detection
        # 'language': ...,

        # temperature to use for sampling
        'temperature': 0,

        # optional patience value to use in beam decoding, as in
        # https://arxiv.org/abs/2204.05424, the default (1.0) is equivalent to
        # conventional beam search
        # 'patience': ...,

        # comma-separated list of token ids to suppress during sampling; '-1'
        # will suppress most special characters except common punctuations
        'suppress_tokens': "-1",

        # optional text to provide as a prompt for the first window.
        # 'initial_prompt': ...,

        # if True, provide the previous output of the model as a prompt for
        # the next window; disabling may make the text inconsistent across
        # windows, but the model becomes less prone to getting stuck in a
        # failure loop
        'condition_on_previous_text': True,

        # temperature to increase when falling back when the decoding fails to
        # meet either of the thresholds below
        'temperature_increment_on_fallback': 0.2,

        # if the gzip compression ratio is higher than this value, treat the
        # decoding as failed
        'compression_ratio_threshold': 2.4,

        # if the average log probability is lower than this value, treat the
        # decoding as failed
        'logprob_threshold': -1,

        # if the probability of the <|nospeech|> token is higher than this
        # value AND the decoding has failed due to `logprob_threshold`,
        # consider the segment as silence
        'no_speech_threshold': 0.6,
    }
    output = version.predict(**inputs)
    # output = {'segments': [{'id': 0, 'end': 2.62, 'seek': 0, 'text': '123', 'start': 0, 'tokens': [50405, 4762, 18, 50495],
    #                      'avg_logprob': -1.6537687301635742, 'temperature': 1, 'no_speech_prob': 0.16527383029460907,
    #                      'compression_ratio': 0.2727272727272727}], 'translation': None, 'transcription': '123',
    #        'detected_language': 'chinese'}
    #
    # print(output['segments'][0]['text'])
    print(output)
    outStr = ''
    for out in output['segments']:
        outStr = outStr + out['text']
    data = {
        "content": outStr
    }

    return HttpResponse(json.dumps(data))
