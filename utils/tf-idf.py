import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
df = pd.read_csv("cleaned_comments.csv")

# Удаляем первую строку, если это шапка дублируется в данных
if df.iloc[0, 0] == 'cleaned_comment':
    df = df.iloc[1:]

# Переименовываем столбец, если нужно
df.columns = ['text']

# Удаляем NaN
df = df.dropna(subset=['text'])

russian_stopwords = [
    'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то',
    'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за',
    'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще',
    'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг',
    'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас',
    'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя',
    'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо',
    'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без',
    'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда',
    'кто', 'этот'
]

# Векторизация
vectorizer = TfidfVectorizer(max_features=1000, stop_words=russian_stopwords)
X_tfidf = vectorizer.fit_transform(df['text'])

# Сохраняем, если нужно
print("TF-IDF shape:", X_tfidf.shape)

n_clusters = 30
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters = kmeans.fit_predict(X_tfidf)

# Уменьшаем размерность до 2D для визуализации
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_tfidf.toarray())

# Добавим данные в датафрейм
df['cluster'] = clusters
df['x'] = X_pca[:, 0]
df['y'] = X_pca[:, 1]

# Визуализация
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='x', y='y', hue='cluster', palette='tab10')
plt.title('Кластеры отзывов (K-Means + PCA)')
plt.xlabel('PCA 1')
plt.ylabel('PCA 2')
plt.legend(title='Кластер')
plt.grid(True)
plt.show()

# Выводим примеры отзывов по каждому кластеру
for cluster_id in range(n_clusters):
    print(f"\n=== Кластер {cluster_id} ===")
    examples = df[df['cluster'] == cluster_id]['text'].head(5)
    for i, comment in enumerate(examples, 1):
        print(f"{i}. {comment}")