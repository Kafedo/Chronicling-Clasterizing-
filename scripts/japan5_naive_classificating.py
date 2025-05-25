import pandas as pd
import spacy
from nltk.util import ngrams
from tqdm import tqdm


categories_df = pd.read_csv("categories_with_markers.csv")
cat_dict = categories_df.set_index("Название")["Маркеры"].to_dict()
cat_dict = {k: v.split("\n") for k, v in cat_dict.items()}
# Создание словаря {классы: [лекс.маркеры]}

df = pd.read_csv("japan_vectorized2.csv")
df.reset_index(drop=True)
# Подрузка последнего созданного датафрейма 

df = df.drop("borders", axis=1)
# Удаление невостребованного столбца

tqdm.pandas()

# Загрузка модели спейси
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text) -> set:
    """Токенизация, лемматизация, и генерация биграмм"""
    doc = nlp(text.lower())

    lemmas = [token.lemma_ for token in doc if token.is_alpha]  
    bigrams = [' '.join(pair) for pair in ngrams(lemmas, 2)]

    # Объединяем униграммы и биграммы
    return set(lemmas + bigrams)

def classify_row(text, class_dict) -> tuple:
    """Отнесение строки к одному из классов"""
    tokens = preprocess_text(text)
    
    score_dict = {
        class_name: sum(1 for marker in markers if marker.lower() in tokens)
        for class_name, markers in class_dict.items()}

    total_hits = sum(score_dict.values())

    if total_hits == 0:
        return ("no_match", 0.0)
    else:
        best_class = max(score_dict, key=score_dict.get)
        best_score = score_dict[best_class]
        return (best_class, best_score / total_hits)

def naive_classifier(texts, class_dict) -> list:
    """ Классификация списка строк с отслеживанием прогресса"""
    results = []

    for text in tqdm(texts, desc="Classify"):
        text_lower = str(text).lower()
        results.append(classify_row(text_lower, class_dict))

    return results

# Сохранение разметки в файл
class_marker, class_prob = zip(*naive_classifier(df["text"].tolist(), cat_dict))
df["class_marker"] = class_marker
df["class_prob"] = class_prob

df.to_csv("japan_with_classes.csv", index=False)
