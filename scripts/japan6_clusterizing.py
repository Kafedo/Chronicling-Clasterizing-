import hdbscan

from sklearn.preprocessing import normalize
import pandas as pd

df = pd.read_csv("japan_with_classes.csv")
df.reset_index()

def clusterize_vectors(df, min_cluster_size, min_samples):
    """
    Кластеризует эмбеддинги с помощью HDBSCAN и возвращает DataFrame с метками кластера
    """
    vectors = normalize([[float(x) for x in str(line).split(" ")] for line in df['vector'].tolist()])
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size, min_samples=min_samples)
    cluster_labels = clusterer.fit_predict(vectors)

    df[f'cluster-{min_cluster_size}-{min_samples}'] = cluster_labels
    probabilities = clusterer.probabilities_
    df[f"membership_prob-{min_cluster_size}-{min_samples}"] = probabilities
    return df, clusterer

illusrating_params = [(67, 23), (20, 10), (10, 6)]
for ip in illusrating_params:
    df, clusterer = clusterize_vectors(df, min_cluster_size=ip[0], min_samples=ip[1])
    print(len(df[f"cluster-{ip[0]}-{ip[1]}"].unique()))
    print(*df[f"cluster-{ip[0]}-{ip[1]}"].unique())
df.to_csv("japan_clusterized.csv", index=False)