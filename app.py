import os 
import telebot
from flask import Flask, request, jsonify

TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(token=TOKEN)

app = Flask(__name__)



def morse_translator(input_string):
    MORSE_CODE_DICT = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '0': '-----', ',': '--..--',
        '.': '.-.-.-', '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-', ' ': '/'  
    }

    REVERSE_MORSE_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

    is_morse = all(char in ['.', '-', ' ', '/'] for char in input_string)

    if is_morse:
        # Terjemahkan Morse ke Teks
        try:
            words = input_string.strip().split(' / ')
            decoded_text = []
            for word in words:
                chars = word.split(' ')
                decoded_word = []
                for char in chars:
                    if char in REVERSE_MORSE_CODE_DICT:
                        decoded_word.append(REVERSE_MORSE_CODE_DICT[char])
                    else:
                        return "Error: Morse code not found.", ""
                decoded_text.append("".join(decoded_word))
            return " ".join(decoded_text)
        except Exception as e:
            return f"Error: {e}", ""
    else:
        # Terjemahkan Teks ke Morse
        try:
            input_string = input_string.upper()
            morse_code = []
            for char in input_string:
                if char == ' ':
                    morse_code.append('/')  # Representasi spasi dalam Morse
                elif char in MORSE_CODE_DICT:
                    morse_code.append(MORSE_CODE_DICT[char])
                else:
                    return f"Error: Cannot translate character '{char}'", ""
            return " ".join(morse_code)
        except Exception as e:
            return "An unexpected error occurred", ""



@bot.message_handler(commands=['start'])
def start_message(M):
    bot.send_message(M.chat.id, "Hello! I'm a Morse code translator!\n\nI can translate text to Morse code and vice versa.\n\nSo, feel free to type anything and I'll translate your text!👌")

@bot.message_handler(func=lambda message: True)
def echo_message(M):
    result = morse_translator(M.text)
    bot.reply_to(M, result)
    
def process_webhook(json_string):
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])

@app.route('/')
def home():
    return jsonify(message="Halo dari Flask API!")

@app.route('/telegram' + TOKEN, methods=['POST'])
def webhook_from_telegram():
    json_string = request.get_data().decode('utf-8')
    process_webhook(json_string)
    return "OK", 200

if __name__ == "__main__":
    app.run()