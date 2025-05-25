import pandas as pd
#from sentence_transformers import SentenceTransformer
#from tqdm import tqdm
from pathlib import Path

# Настраиваем пути 
# NOTE изменить разделители при надобности
cur_dir = Path(__file__).resolve().parent
in_dir = Path(f"{cur_dir}/japan_texts_cleaned2")
out_file = Path(f'{cur_dir}/japan_articles2.csv')


# Функция, достающая из файла "статьи" про Японию
def create_df(path: str):

    def get_borders(idx, lena):
        start = idx-5 if idx > 5 else 0
        end = idx+5 if idx+5 < lena else lena
        return {"start":start, "end":end}
    try:
        with open(path, "r", encoding='UTF-8') as infile:
            url, head, _, _, *lines = infile.read().split("\n")
        file_name = path.split("/")[-1] # NOTE В аналогичной строке в прошлый раз была проблема
        articles = [[url, head, file_name, line] for line in lines]
        article_df = pd.DataFrame(articles, columns=['url', 'name', 'file_name', 'line'])
        article_df["borders"] = None
        borders = []
        cur_text = {}
        lena = len(lines)
        for idx, line in enumerate(lines):
            if "japan" in line.lower():
                if cur_text == {}:
                    cur_text = get_borders(idx, lena)
                else:
                    new_text = get_borders(idx, lena)
                    if cur_text.get("end") <= new_text.get("start"):
                        borders.append([cur_text.get("start"), cur_text.get("end")])
                        cur_text = new_text
                    else:
                        cur_text["end"] = new_text.get("end")    
        idxes = []
        for pair in borders:
            idxes.extend([n for n in range(pair[0], pair[1])])
            article_df.iloc[pair[0], 4] = pair[1] - pair[0]           
        article_df = article_df.iloc[idxes]
        article_df.to_csv(out_file, mode='a', header=False, index=False)
    except: 
        print(path)

pathlist = Path(in_dir).glob('*.txt')
for num, path in enumerate(pathlist):
    create_df(str(path))
    print(f"{num+1} is done", end="\r") # счётчик
