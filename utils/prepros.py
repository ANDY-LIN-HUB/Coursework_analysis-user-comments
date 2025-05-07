import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer



stop_words = set(stopwords.words("russian"))
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    text = str(text).lower()
    text = re.sub(r"[^а-яё\s]", "", text)  # оставим только русские буквы
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

if __name__ == "__main__":
    df = pd.read_csv("comments.csv")

    # Создание нового датафрейма только с очищенными комментариями
    cleaned_df = pd.DataFrame({
        "cleaned_comment": df["comment"].apply(preprocess)
    })

    print(cleaned_df.head())

    # (опционально) сохранить в файл
    cleaned_df.to_csv("cleaned_comments.csv", index=False, encoding="utf-8")
