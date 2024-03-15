import customtkinter as ctk
import pandas as pd
import os
from PIL import Image
from playsound import playsound
from random import randint

ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")

audio_width = 100
audio_height = 100
symbol_width = 50
symbol_height = 50
font_type = ("helvetica", 20)


class App(ctk.CTk):


    def __init__(self, data_path):

        super().__init__()

        self.data_folder = data_path
        self.image_path = data_path + r"/Images/"
        self.audio_path = data_path + r"/Audios/"

        self.title("Minimal Pairs")
        self.geometry("500x600")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_home_screen()


    def clear_screen(self):
        children = self.winfo_children()
        for child in children:
            child.destroy()


    def create_home_screen(self):

        self.clear_screen()

        self.master_frame = ctk.CTkFrame(master=self, fg_color="black")
        self.master_frame.pack(pady=0, padx=0, fill="both", expand=True)

        self.symbol_text = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", text="Choose a play mode", font=font_type)
        self.symbol_text.pack(pady=40, padx=0)

        self.tones_button = ctk.CTkButton(master=self.master_frame, command=self.tones_mode, text="Tones")
        self.tones_button.pack(pady=20, padx=0)

        self.sounds_button = ctk.CTkButton(master=self.master_frame, command=self.sounds_mode, text="Sounds")
        self.sounds_button.pack(pady=20, padx=0)


    def tones_mode(self):
        self.data_path = self.data_folder + r"/tones.csv"
        self.df = pd.read_csv(self.data_path)
        self.create_working_screen()


    def sounds_mode(self):
        self.data_path = self.data_folder + r"/minimal_pairs.csv"
        self.df = pd.read_csv(self.data_path)
        self.create_working_screen()


    def create_working_screen(self):

        self.clear_screen()

        self.word = self.select_word()

        self.master_frame = ctk.CTkFrame(master=self, fg_color="black")
        self.master_frame.pack(pady=0, padx=0, fill="both", expand=True)

        self.sound = ctk.CTkImage(Image.open(os.path.join(self.image_path, "audio.png")), size=(audio_width, audio_height))
        self.correct = ctk.CTkImage(Image.open(os.path.join(self.image_path, "correct.png")), size=(symbol_width, symbol_height))
        self.incorrect = ctk.CTkImage(Image.open(os.path.join(self.image_path, "incorrect.png")), size=(symbol_width, symbol_height))
        self.blank = ctk.CTkImage(Image.open(os.path.join(self.image_path, "blank.png")), size=(symbol_width, symbol_height))

        self.play_button = ctk.CTkButton(master=self.master_frame, command=self.play_sound, image=self.sound, text="", fg_color="black", bg_color="black", width=audio_width, height=audio_height)
        self.play_button.pack(pady=20, padx=0)

        self.symbol = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", width=symbol_width, height=symbol_height, text="")
        self.symbol.pack(pady=20, padx=0)
        
        self.symbol_text = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", text="", font=font_type)
        self.symbol_text.pack(pady=0, padx=0)

        self.answer = ctk.CTkLabel(master=self.master_frame, fg_color="transparent", text="", font=font_type)
        self.answer.pack(pady=20, padx=0)

        self.entry_box = ctk.CTkEntry(master=self.master_frame, placeholder_text="")
        self.entry_box.pack(pady=20, padx=0)

        self.submit_button = ctk.CTkButton(master=self.master_frame, command=self.check_input, text="Submit")
        self.submit_button.pack(pady=0, padx=0)

        self.next_button = ctk.CTkButton(master=self.master_frame, command=self.next_input, text="Next")
        self.next_button.pack(pady=10, padx=0)

        self.return_button = ctk.CTkButton(master=self.master_frame, command=self.create_home_screen, text="Return Home")
        self.return_button.pack(pady=10, padx=0)


    def select_word(self):

        min_val = min(self.df["Appearances"])
        not_appeared = self.df.loc[self.df["Appearances"] == min_val]
        index = randint(0, not_appeared.shape[0] - 1)
        row = not_appeared.iloc[index, :]
        word = row["Word"]
        
        df_index = self.df.index[self.df['Word'] == word].tolist()[0]
        self.df.loc[df_index, "Appearances"] = self.df.loc[df_index, "Appearances"] + 1
        self.df.to_csv(self.data_path, index=False)

        return word
    

    def next_input(self):
        self.symbol_text.configure(text="")
        self.symbol.configure(image=self.blank)
        self.answer.configure(text="")
        self.word = self.select_word()
        self.play_sound()
    

    def update_symbol(self, correct):
        if correct == True:
            self.symbol.configure(image=self.correct)
            self.symbol_text.configure(text="Correct")
        else:
            self.symbol.configure(image=self.incorrect)
            self.symbol_text.configure(text="Incorrect")

        self.entry_box.delete(0, len(self.entry_box.get()))
        self.answer.configure(text=self.word)  


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