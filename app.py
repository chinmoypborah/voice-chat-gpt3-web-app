import openai
import pyttsx3
import speech_recognition as sr

from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = "YOUR-OPENAI-API-KEY-HERE" #Enter_your_openai_api_key

engine = pyttsx3.init()

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

conversation = ""

@app.route('/')
def home():
  return '''
  <html>
  <head>
    <title>Voice Chatbot</title>
    <style>
      body {
        background-color: black;
        color: white;
      }
      h1 {
        text-align: center;
        font-size: 20px;
      }
      h2 {
        text-align: center;
        font-size: 16px;
      }
      #mic-button {
        display: block;
        margin: 0 auto;
        background-color: yellow;
        border-radius: 50px;
        box-shadow: 0 0 4px white;
        color: black;
        font-weight: bold;
      }
      #message-box {
        width: 50%;
        margin: 0 auto;
        border: 2px solid white;
        border-radius: 4px;
        padding: 16px;
        text-align: center;
      }
      #response-window {
        width: 50%;
        margin: 32px auto;
        border: 2px solid white;
        border-radius: 4px;
        padding: 16px;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <div style="position: absolute; top: 0; right: 0;">
    <img src="https://www.protaqnia.com/wp-content/uploads/2022/06/Web-1920-%E2%80%93-12.png" alt="Logo" height="50">
    </div>
    <br>
    <br>
    <br>
    <br>
    <h1>Voice Chat using GPT-3 Demo 1</h1>
    <h2>Created by Chinmoy Pratim Borah from ProTaqnia</h2>
    <button id="mic-button">Give command</button>
    <div id="message-box">
      <!-- user's voice input will be displayed here -->
    </div>
    <div id="response-window">
      <!-- response will be displayed here -->
    </div>
    <script>
      const micButton = document.getElementById('mic-button');
      const messageBox = document.getElementById('message-box');
      const responseWindow = document.getElementById('response-window');
  
      micButton.addEventListener('click', () => {
        // start listening for voice input
        const recognition = new webkitSpeechRecognition();
        recognition.start();
  
        // when the voice input is recognized, display it and send it to the server
        recognition.onresult = (event) => {
          const text = event.results[0][0].transcript;
          messageBox.innerText = text;
          fetch('/process_text', {
            method: 'POST',
            body: JSON.stringify({ text }),
            headers: { 'Content-Type': 'application/json' },
          })
            .then(response => response.json())
            .then((data) => {
              // display the response and speak it out loud
              responseWindow.innerText = data.response;
              const speech = new SpeechSynthesisUtterance(data.response);
              window.speechSynthesis.speak(speech);
            });
        };
      });
    </script>
  </body>
</html>
  '''

@app.route('/process_text', methods=['POST'])
def process_text():
  data = request.get_json()
  text = data['text']

  # generate a response using the OpenAI API
  response = openai.Completion.create(engine='text-davinci-003', prompt=text, max_tokens=100)
  response_str = response["choices"][0]["text"]

  return jsonify({ 'response': response_str })

if __name__ == '__main__':
  app.run()
