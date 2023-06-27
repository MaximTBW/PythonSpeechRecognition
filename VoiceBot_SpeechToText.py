import speech_recognition as sr
import subprocess
import re
import json
import os
import nltk
import pyttsx3 # использование внетреннего голосового помощника Windows
engine = pyttsx3.init() 
voices = engine.getProperty('voices')
ru_voice_id = voices[0].id # выбор русской Ирины в стандартной Windows 10
engine.setProperty('voice', ru_voice_id) 

def matching(text,withtext):
    return nltk.edit_distance(text.lower(),withtext.lower())/min(len(text),len(withtext))

"""
Выгрузка информации с файла в виде
'Выражение для pattern re.search': 'команда в командной строке'
"""
with open("Information.json","r") as f:
    variants = json.load(f)

"""
Инициализация обработчика и микрофона
"""
r = sr.Recognizer()
mic = sr.Microphone()
sr.LANGUAGE = 'ru-RU'
"""
Само действие
"""
while 1==1:
    """
    Прослушка микрофона
    """
    with mic as src:
        r.adjust_for_ambient_noise(src)
        print('Rec...')
        audio = r.listen(src)
    print('End of recording')
    try:
        """
        Обработка сказанного, перевод в текст
        """
        print('Parse to string')
        text = r.recognize_google(audio, language = 'ru-RU')
        print(f"Text: {text}")
        
        """
        Команда - выражение для выхода
        """
        print('Match witch cases of comands...')
        try:
            if(re.search(".*внимание.{0,7}команда(.{0,4}бот.*)?.{0,7}(выкл|откл).*", text.lower()).group() == text.lower()):
                exit()
        except:
            pass
        """
        Пробегаем по все выражениям. Если выражение будет верно,
        будет вызван subprocess(консоль) с параметрами,
        прописанными в json по ключу
        """
        print('Match witch cases of json...')
        for key in variants:
            print("  "+key)
            matched = re.search(key.lower(), text.lower())
            """
            Проверка на существование шаблона и
            на совпадение текста с шаблоном с погрешностью в 5%
            """
            if(matched!=None and matching(matched.group(),text.lower())<0.05):
                if(variants[key][0] == "subproc"):
                    print(f'Run subprocess {variants[key][1]}')
                    engine.say('запуск процесса')
                    engine.runAndWait()
                    subprocess.run(variants[key][1])
                elif(variants[key][0] == "gensay"):
                    engine.say(variants[key][1])
                    engine.runAndWait()
                elif(variants[key][0] == "start"):
                    print(f'Start program {variants[key][2]}')
                    engine.say('запуск программы')
                    engine.runAndWait()
                    os.startfile(variants[key][1]+variants[key][2])
                elif(variants[key][0] == "startparam"):
                    print(f'Start program {variants[key][2]} with params {variants[key][3]}')
                    engine.say('запуск программы с параметром')
                    engine.runAndWait()
                    os.system(f'start '+(f'/d "{variants[key][1]}" ' if len(variants[key][1])>0 else '')+f'{variants[key][2]} {variants[key][3]}')
                elif(variants[key][0] == "comand"):
                    engine.say('запуск команды')
                    engine.runAndWait()
                    print(f'Run comand {variants[key][1]}')
                    os.system(variants[key][1])
                else:
                    print(matched.group())
                
                break
            """
            Могут вылетать ошибки необработанного голоса и прочее по мелочи. Можно сделать без
            except-ов, но надо-ли?
            # Надо .-.
            """
    except Exception as e:
        print(e)
    


