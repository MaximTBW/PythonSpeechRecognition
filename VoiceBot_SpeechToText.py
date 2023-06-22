import speech_recognition as sr
import subprocess
import re
import json

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
        if(re.search(".*внимание.{0,7}команда(.{0,4}бот.*)?.{0,7}(выкл|откл).*", text.lower()).group() == text.lower()):
            exit()

        """
        Пробегаем по все выражениям. Если выражение будет верно,
        будет вызван subprocess(консоль) с параметрами,
        прописанными в json по ключу
        """
        print('Match witch cases of json...')
        for key in variants:
            try:
                if(re.search(key.lower(), text.lower()).group() == text.lower()):
                    print('Run process')
                    subprocess.run(variants[key])
                    break
        """
        Могут вылетать ошибки несоответствия выражения,
        необработанного голоса и прочее по мелочи. Можно сделать без
        except-ов, но надо-ли?
        """
            except Exception as e:
                pass
    except Exception as e:
        pass
    


