from pathlib import Path
import os.path
import spacy
import re


sep = '/' # '\\' windows, но '/' linux
cur_dir = Path(__file__).resolve().parent
in_dir = Path(f"{cur_dir}{sep}japan_texts")
lust_out_dir = Path(f"{cur_dir}{sep}japan_texts_cleaned2")
out_dir = Path(f"{cur_dir}{sep}japan_texts_cleaned2.1")
if out_dir.exists() is False:
    out_dir = Path.mkdir(out_dir, parents=True)
# чтобы не было проблем с местоположением файлов

nlp = spacy.load("en_core_web_sm")

def cleaned(sentense: list, nlp: spacy, stops=["PUNCT", "SYM", "X"]) -> str:
    to_delit = []
    for ind, word in enumerate(sentense):
        wo = word.rstrip().rstrip()
        if wo:
            postag = [w.pos_ for w in nlp(wo)]
            if len(postag) > 1:
                if set(postag) <= set(stops):
                    to_delit.append(ind)
                    # удаление не-слов
        else:
            to_delit.append(ind)
            # удение пустых строк
    for ind in to_delit[::-1]:
        sentense.pop(ind)
    return " ".join(sentense)

nlp = spacy.load("en_core_web_sm")
pathlist = Path(in_dir).glob('*.txt')
for num, path in enumerate(pathlist):
    str_path = str(path)
    file_name = str_path.split(sep)[-1]
    if os.path.exists(f'{lust_out_dir}{sep}{file_name}') is False:
        with open(str_path, "r", encoding="UTF-8") as infile:
            url, head, *text = infile.readlines()
        text = [re.sub(r"\b[^\w' -]\b", r'', x) for x in text]
        text = [re.sub(r"([.?!])( )?\n", r'\1 ', x) for x in text]
        sentenses_list = " ".join(text).split("\n")
        words_in_sentenses_list = [sentense.split(" ") for sentense in sentenses_list]
        quontity = len(words_in_sentenses_list)
        with open(f"{out_dir}{sep}{file_name}", "a+", encoding="UTF-8") as outfile:
            print(f"{url}{head}\n", file = outfile)
            for quo, sentense in enumerate(words_in_sentenses_list): 
                print(cleaned(sentense, nlp), file = outfile)
                print(f"{num+1}, '{file_name}', {quo+1} line out of {quontity}", end="\r")
                # счётчик
