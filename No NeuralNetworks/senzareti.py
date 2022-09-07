import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import time
import subprocess
import wolframalpha
import requests


print('Caricando il tuo assistente personale - Elsa')

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("rate", 190)
engine.setProperty("voice", voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Ciao buongiorno Giorgia")
        print("Ciao Buongiorno Giorgia")
    elif hour>=12 and hour<18:
        speak("Buon pomeriggio Giorgia")
        print("Buon pomeriggio Giorgia")
    else:
        speak("Buonasera Giorgia")
        print("Buonasera Giorgia")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ascoltando...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio , language='it-IT')
            print(f"l'utente ha detto:{statement}\n")

        except Exception as e:
            speak("Scusami non ho capito, puoi ripetere")
            return "None"
        return statement

speak("Caricando il tuo assistente personale ")
wishMe()


if __name__=='__main__':


    while True:
        speak("Cosa posso fare per lei?")
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "addio" in statement or "arrivederci" in statement or "stop" in statement:
            speak('Il tuo assistente personale Elsa si sta spegnendo, addio')
            print('il tuo assistente personale Elsa si sta spegnendo, addio')
            break



        if 'wikipedia' in statement:
            speak('Cercando su Wikipedia...')
            wikipedia.set_lang("it")
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("secondo wikipedia")
            print(results)
            speak(results)

        elif 'apri youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("ho aperto youtube")
            time.sleep(5)

        elif 'apri google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("puoi ora navigare su google")
            time.sleep(5)


        elif "tempo" in statement:
            api_key="38112d7fb6b105c166bc8fa9c19c4a93"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("dimmi il nome della città di cui desideri conoscere il meteo")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" la temperatura in kelvin è  " +
                      str(current_temperature) +
                      "\n l'umidità in percentuale è  " +
                      str(current_humidiy) +
                      "\n e  " +
                      str(weather_description))
                print(" la temperatura in kelvin è  = " +
                      str(current_temperature) +
                      "\n l'umidità in percentuale è  = " +
                      str(current_humidiy))


            else:
                speak(" Città non disponibile ")



        elif 'ore' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sono le ore {strTime}")

        elif 'chi sei' in statement or 'cosa sai fare' in statement:
            speak('Sono Elsa e sono un assistente virtuale creato in Python. sono programmata per eseguire piccoli compiti come'
                  'aprire youtube, google e netflix , dirti che ore sono,scattare una foto,cercare su wikipedia e darti le previsioni del tempo' 
                  'in diverse città, dirti le notizie principali e qualche informazione geografica')


        elif "chi ti ha creato" in statement or "chi è il tuo creatore supremo" in statement:
            speak("Sono stata parzialmente costruita Giorgia")
            print("Sono stata parzialmente costruita da Giorgia")


        elif "apri netflix" in statement:
            webbrowser.open_new_tab("https://www.netflix.com/browse")
            speak("ecco a te Netflix")

        elif 'notizie' in statement:
            news = webbrowser.open_new_tab("https://www.rainews.it/")
            speak('eccoti le notizie principali del giorno in Italia, buona lettura')
            time.sleep(6)


        elif 'cerca' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'cosa posso chiederti' in statement:
            speak('posso rispondere a domande geografiche o di tipo computazionale, chiedimi pure')
            question=takeCommand()
            app_id="6VK778-8JT9VG842E"
            client = wolframalpha.Client('6VK778-8JT9VG842E')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)


        elif "esci dal pc" in statement or "slogga" in statement:
            speak("Ok , il tuo account uscirà tra 10 secondi, controlla di aver chiuso tutte le applicazioni aperte")
            subprocess.call(["shutdown", "/l"])

time.sleep(3)












