import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from pathlib import Path

# Настраиваем пути (изменить разделители при надобности)
cur_dir = Path(__file__).resolve().parent
in_file = Path(f"{cur_dir}\\japan_articles2.csv")
out_file = Path(f"{cur_dir}\\japan_vectorized2.csv")

# Импорт модели
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# Импорт датасета с предложениями
jap_df = pd.read_csv(in_file, names=['url', 'name', 'file_name', 'line', 'borders'])
jap_df = jap_df.reset_index()

def get_embeddings(df, model, out_file, batch_size=64):
    df["vector"] = None
    # бродим по датасету по батчам
    for i in tqdm(range(0, len(df), batch_size), desc="Vectorizing by batches"):
        batch_df = df.iloc[i:i + batch_size] # делаем датасет батча  
        batch_texts = batch_df['line'].tolist()
        batch_embeddings = model.encode(batch_texts, convert_to_tensor=True, output_value='sentence_embedding', batch_size=batch_size)
        batch_embeddings = batch_embeddings.numpy().tolist() # получаем эмбединги
        for j, embedding in enumerate(batch_embeddings):
            batch_df.at[i + j, "vector"] = " ".join(map(str, embedding)) # вносим значения в датафрейм
        batch_df.to_csv(out_file, mode='a', index=False, header=False)
        # закидываем в файл, чтобы в любой момент можно было остановиться

get_embeddings(jap_df, model, out_file)