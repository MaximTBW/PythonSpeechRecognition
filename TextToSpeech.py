import playsound #playsound всегда должен быть в начале иначе даже не запустится файл

# Должно работать без инета
import pyttsx3 # использование внетреннего голосового помощника Windows
engine = pyttsx3.init() 
voices = engine.getProperty('voices')
text = input()
"""
for voice in voices:    # голоса и их параметры
    print('------')
    print(f'Имя: {voice.name}')
    print(f'ID: {voice.id}')
    print(f'Язык(и): {voice.languages}')
    print(f'Пол: {voice.gender}')
    print(f'Возраст: {voice.age}')
"""
ru_voice_id = voices[0].id # выбор русской Ирины в стандартной Windows 10
engine.setProperty('voice', ru_voice_id) # ставим настройку голса
engine.say(text) # добавляем в очередь текст
engine.runAndWait() # запускаем и слушаем

# работает только с инетом
"""
import gtts
import time
tts = gtts.gTTS(text, lang="ru") # обращаясь к интернету, запрашиваем голосовую версию текста
tts.save("voice.mp3") # сохраняем голосовую версию
playsound.playsound('voice.mp3') # слушаем чо
# выдаёт ошибку о невозможности закрыть файл
# можно испольовать vlc
"""

