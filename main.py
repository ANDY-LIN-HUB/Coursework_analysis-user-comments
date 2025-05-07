from app.pars import WbReview
import pandas as pd

class Window:

    def __init__(self):
        pass

def start():
    request = WbReview(string="https://www.wildberries.ru/catalog/206392976/detail.aspx").parse()
    data = []
    for item in request['feedbacks']:
        text = item['text']
        if text:
            data.append(text)

    df = pd.DataFrame(data, columns=["comment"])
    df.to_csv("comments.csv", index=False, encoding="utf-8")  # запись в CSV
    print("Файл comments.csv успешно создан.")
    

if __name__ == "__main__":
    start()