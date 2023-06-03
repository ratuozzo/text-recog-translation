import azure.cognitiveservices.speech as speechsdk
import os, requests, uuid, json

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "4d3cd9722d414c27a32bbf3916c9b05f", "eastus"
text_key, api_url = "189f44eecd264c0d96d58b080ba1a54f", "https://api.cognitive.microsofttranslator.com/detect?api-version=3.0"
translate_url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")


# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
result = speech_recognizer.recognize_once()

# Checks result.
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
    headers = {
    'Ocp-Apim-Subscription-Key': text_key,
    'Ocp-Apim-Subscription-Region': service_region,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': result.text
    }]
    request = requests.post(api_url, headers=headers, json=body)
    response = request.json()
    #print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
    
    path = '/translate?api-version=3.0'
    params = f'&from={response[0]["language"]}&to=en'
    constructed_url = translate_url + params

    headers = {
        'Ocp-Apim-Subscription-Key': text_key,
        'Ocp-Apim-Subscription-Region': service_region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text' : result.text
    }]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    print(response[0]["translations"][0]["text"])

    #print(json.dumps(response, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': ')))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized: {}".format(result.no_match_details))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))