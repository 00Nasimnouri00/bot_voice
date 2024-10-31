#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os
from telebot import TeleBot
from dotenv import load_dotenv
from pydub import AudioSegment


# In[ ]:


# Load environment variables from the .env file
load_dotenv()

bot = TeleBot(os.environ.get("TELEGRAM_BOT_TOKEN"))

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me an audio file recorded in Telegram.")

@bot.message_handler(content_types=['audio', 'voice'])
def handle_audio(message):
    try:
        # Notify user that the voice message was received
        bot.reply_to(message, "We received your voice message.")

        # Get the file ID of the audio message
        file_id = message.audio.file_id if message.content_type == 'audio' else message.voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the OGG file temporarily
        ogg_path = "user_audio.ogg"
        with open(ogg_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Notify user that the conversion is in progress
        bot.reply_to(message, "Converting audio to .wav format...")

        # Convert OGG to WAV
        wav_path = "user_audio.wav"
        audio = AudioSegment.from_ogg(ogg_path)
        audio.export(wav_path, format="wav")
        os.remove(ogg_path)  # Clean up the OGG file

        # Notify user that the plot will be generated
        bot.reply_to(message, "We will send you a plot of the pitch variation.")

        # Analyze the audio and plot pitch
        plot_pitch_variation(wav_path, message)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

def plot_pitch_variation(audio_file, message):
    try:
        # Load audio file
        y, sr = librosa.load(audio_file)

        # Extract pitches and magnitudes
        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

        # Process to find F0 (pitch) over time
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Filtering out zero or undefined pitches
                pitch_values.append(pitch)
            else:
                pitch_values.append(np.nan)  # Mark as NaN for visualization purposes

        # Plot the pitch variations over time
        plt.figure(figsize=(14, 5))
        plt.plot(pitch_values, label='Pitch (F0)')
        plt.xlabel('Time (frames)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Pitch Variation in Speech')
        plt.legend()

        # Save the plot as an image file
        plot_path = "pitch_plot.png"
        plt.savefig(plot_path)
        plt.close()

        # Send the plot to the user
        with open(plot_path, 'rb') as plot_file:
            bot.send_photo(message.chat.id, plot_file)

        # Clean up the image file
        os.remove(plot_path)
    except Exception as e:
        bot.reply_to(message, f"An error occurred while plotting: {str(e)}")

if __name__ == "__main__":
    bot.polling()

