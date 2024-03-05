import pandas as pd
import re

def read_file(path):
    
    with open(path, 'r') as file:
        # Read the contents of the file
        content = file.read()

    # Print the contents exactly as they appear
    lines = content.split('\n')
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    lines.pop(-1)

    base_df = pd.DataFrame({"Front": [], "Back": [], "Tag": []})

    for line in lines:
        line = re.sub(r"<br>", "\n", line)
        line = re.sub(r"<\/?em>", "", line)
        sections = line.split("\t")
        row = pd.Series([sections[0], sections[1], "tag"], index=base_df.columns)
        base_df = pd.concat([base_df, row.to_frame().T], ignore_index=True)
        

    return base_df


def create_hanzi(base_df):
    hanzi_df = pd.DataFrame({"Front": [], "Back": [], "Tag": []})

    for index, row in base_df.iterrows():
        sections = base_df.loc[index, "Back"].split("\n")
        front = sections[0]
        back = sections[1] + "\n" + base_df.loc[index, "Front"] + "\n" + sections[-1]

        row = pd.Series([front, back, "tag"], index=hanzi_df.columns)
        hanzi_df = pd.concat([hanzi_df, row.to_frame().T], ignore_index=True)

    hanzi_df.to_csv(r"/home/david/Documents/Language-Learning/data/sentences_hanzi.csv", encoding="utf-8", sep="\t", index=False, header=False)


def create_sound(base_df):
    sound_df = pd.DataFrame({"Front": [], "Back": [], "Tag": []})

    for index, row in base_df.iterrows():
        sections = base_df.loc[index, "Back"].split("\n")
        front = sections[-1]
        back = sections[0] + "\n" + sections[1] + "\n" + base_df.loc[index, "Front"]

        row = pd.Series([front, back, "tag"], index=sound_df.columns)
        sound_df = pd.concat([sound_df, row.to_frame().T], ignore_index=True)

    sound_df.to_csv(r"/home/david/Documents/Language-Learning/data/sentences_sound.csv", encoding="utf-8", sep="\t", index=False, header=False)
    

if __name__=="__main__":

    path = r"/home/david/Documents/Language-Learning/data/Sentences__Hanzi.txt"
    base_df = read_file(path)
    create_hanzi(base_df)
    create_sound(base_df)