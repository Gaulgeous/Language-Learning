import customtkinter as ctk
import pandas as pd
import os
from PIL import Image
from playsound import playsound
from random import randint

ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")

audio_width = 26
audio_height = 26
symbol_width = 26
symbol_height = 26


class App(ctk.CTk):


    def __init__(self, data_path):

        super().__init__()

        self.data_path = data_path + "/minimal_pairs.csv"
        self.image_path = data_path + r"/Images/"
        self.audio_path = data_path + r"/Audios/"

        self.df = pd.read_csv(self.data_path)

        self.title("Minimal Pairs")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.master_frame = ctk.CTkFrame(master=self, fg_color="black")
        self.master_frame.pack(pady=0, padx=0, fill="both", expand=True)

        self.sound = ctk.CTkImage(Image.open(os.path.join(self.image_path, "audio.png")), size=(audio_width, audio_height))
        self.correct = ctk.CTkImage(Image.open(os.path.join(self.image_path, "correct.png")), size=(26, 26))
        self.incorrect = ctk.CTkImage(Image.open(os.path.join(self.image_path, "incorrect.png")), size=(26, 26))

        self.play_button = ctk.CTkButton(master=self.master_frame, command=self.play_sound, image=self.sound, text="", fg_color="black", bg_color="black", width=audio_width, height=audio_height)
        self.play_button.pack(pady=0, padx=0)

        self.symbol = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", width=symbol_width, height=symbol_height, text="")
        self.symbol.pack(pady=0, padx=0)
        
        self.symbol_text = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", text="")
        self.symbol_text.pack(pady=0, padx=0)

        self.answer = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", text="")
        self.answer.pack(pady=0, padx=0)

        self.entry_box = ctk.CTkEntry(master=self.master_frame, placeholder_text="")
        self.entry_box.pack(pady=0, padx=0)

        self.submit_button = ctk.CTkButton(master=self.master_frame, command=self.check_input, text="Submit")
        self.submit_button.pack(pady=0, padx=0)

        self.word = self.select_word()
        # self.play_sound()


    def select_word(self):

        min_val = min(self.df["Appearances"])
        not_appeared = self.df.loc[self.df["Appearances"] == min_val]
        index = randint(0, not_appeared.shape[0] - 1)
        row = not_appeared.iloc[index, :]
        word = row["Word"]
        
        df_index = self.df.index[self.df['Word'] == word].tolist()[0]
        self.df.loc[df_index, "Appearances"] = self.df.loc[df_index, "Appearances"] + 1
        self.df.to_csv(self.data_path)

        return word
    

    def update_symbol(self, correct):
        if correct == True:
            self.symbol.configure(image=self.correct)
            self.symbol_text.configure(text="Correct")
        else:
            self.symbol.configure(image=self.incorrect)
            self.symbol_text.configure(text="Incorrect")

        self.entry_box.delete(0, len(self.entry_box.get()))
        self.answer.configure(text=self.word)
        self.word = self.select_word()
        # self.play_sound()


    def check_input(self):
        input = self.entry_box.get()
        self.update_symbol(input==self.word)


    def play_sound(self):
        sound_path = self.audio_path + self.word + ".mp3"
        playsound(sound_path)


if __name__=="__main__":

    print("Starting")

    data_path = r"/home/david/Documents/Language-Learning/data"

    app = App(data_path)
    app.mainloop()