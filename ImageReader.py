from gtts import gTTS
import random
import pytesseract
import os
import configparser

import azure.cognitiveservices.speech as speechsdk

#Need set-up env variables
#setx SPEECH_KEY your_speech_key
#setx SPEECH_REGION brazilsouth


speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
speech_config.speech_synthesis_voice_name = 'pt-BR-JulioNeural'

config = configparser.ConfigParser()
config.read('cnf.ini')
pytesseract.pytesseract.tesseract_cmd = config.get('tesseract', 'path')



class ImageReader:
    image = None
    text = None
    text_array = None
    q = None
    lang = None


    def __init__(self, image):
        self.image = image
        self.lang = config.get('language', 'lang')

    def read_from_img(self):
        lng = self.lang
        if self.lang == 'pt':
            lng = 'por'
        text = pytesseract.image_to_string(self.image, lang=lng, config='--psm 6 --oem 3')

        # this part was created to improve the phoneme, tested only in pt-BR
        if self.lang == 'pt':
            for r in (("Gimli","Guimle"),("Warg","Uoarg")):
                text = text.replace(*r)
        # end better phoneme
        self.text = text
        self.replace_special_signs(self)
        print(self.text) # Prints on terminal
        return self.text

    def read_sentence_by_sentence(self, text_list):
        #This list creates "memory" to not read some repeated phrases that appear in the game, tested on pt-BR
        prohibited_words = ["Você ou um herói próximo ganha uma inspiração!",
                              "Coloque uma ficha de busca conforme indicado.",
                              "Explorar?",
                              "Descarte a ficha de exploração.",
                              "Coloque uma ficha de pessoa conforme indicado.",
                              "Coloque uma ficha de busca conforme indicado.",
                              "Coloque uma ficha de exploração.",
                              "Sua jornada continua...",
                              "Coloque fichas de exploração."]
        for string in prohibited_words:
            self.text = self.text.replace(string, '', 1)


        if (self.text not in text_list):
            #TODO: Adicionar outras vozes para ler textos de personagens
            if "Coloque a peça" in self.text or "As sombras" in self.text:
                return
            elif len(self.text) > 5:
                speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
                speech_synthesis_result = speech_synthesizer.speak_text_async(self.text).get()
                print("API called")
                # This list creates "memory" to not read some phrases already read before
                text_list.append(self.text)

    @staticmethod
    def replace_special_signs(self):
        self.clean_up_text(self)

        if self.lang == 'pol':
            self.text = self.text.replace('1.', 'jeden')
            self.text = self.text.replace('2.', 'dwa')
            self.text = self.text.replace('3.', 'trzy')
            self.text = self.text.replace('4.', 'cztery')
            self.text = self.text.replace('5.', 'pięć')

            self.text = self.text.replace('©', 'symbol przeznaczenia')
            self.text = self.text.replace('&', 'symbol sukcesu')
            self.text = self.text.replace('$', 'atak dystansowy')
            self.text = self.text.replace('£', 'rana')
            self.text = self.text.replace('%', 'strach')
            self.text = self.text.replace('€', 'przedmiot: ')

            if 'test' in self.text:
                self.text = self.text.replace(']', 'siły')
                self.text = self.text.replace('=', 'mądrości')
                self.text = self.text.replace('+', 'zręczności')
                self.text = self.text.replace('[', 'ducha')
                self.text = self.text.replace('*', 'sprytu')
            else:
                self.text = self.text.replace(']', 'siła')
                self.text = self.text.replace('=', 'mądrość')
                self.text = self.text.replace('+', 'zręczność')
                self.text = self.text.replace('[', 'duch')
                self.text = self.text.replace('*', 'spryt')
        elif self.lang == 'pt':
            self.text = self.text.replace('>', 'destino')
            self.text = self.text.replace('&', 'sucesso')
            self.text = self.text.replace('$', 'ataque à distância')
            self.text = self.text.replace('£', 'dano')
            self.text = self.text.replace('%', 'medo')
            self.text = self.text.replace('€', 'consumível: ')

            self.text = self.text.replace(']', 'vigor')
            self.text = self.text.replace('=', 'sabedoria')
            self.text = self.text.replace('+', 'agilidade')
            self.text = self.text.replace('/', 'espírito')
            self.text = self.text.replace('<', 'esperteza')
        else:
            self.text = self.text.replace('©', 'fate')
            self.text = self.text.replace('&', 'success')
            self.text = self.text.replace('$', 'ranged')
            self.text = self.text.replace('£', 'damage')
            self.text = self.text.replace('%', 'fear')
            self.text = self.text.replace('€', 'trinket: ')

            self.text = self.text.replace(']', 'might')
            self.text = self.text.replace('=', 'wisdom')
            self.text = self.text.replace('+', 'agility')
            self.text = self.text.replace('[', 'spirit')
            self.text = self.text.replace('*', 'wit')

    @staticmethod
    def clean_up_text(self):
        self.text = self.text.replace('\n', ' ').strip()
        self.text = self.text.replace(';', '')
        self.text = self.text.replace('\'', '')
        self.text = self.text.replace('\"', '')
