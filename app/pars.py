import requests, re, json



HEADERS = {
    'user-agent': 'Mozilla/5.0 (Linux; Android) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 CrKey/1.54.248666',
}


class WbReview:
    def __init__(self, string: str):
        self.sku = self.get_sku(string=string)
        self.root_id = self.get_root_id(sku=self.sku)

    @staticmethod
    def get_sku(string: str) -> str:
        if "wildberries" in string:
            pattern = r"\d{7,15}"
            sku = re.findall(pattern=pattern, string=string)
            if sku:
                return sku[0]
            else:
                return Exception("Не найден артикул!")
        return string
    
    def get_review(self) -> json:
        try:
            response = requests.get(f'https://feedbacks1.wb.ru/feedbacks/v1/{self.root_id}', headers=HEADERS)
            if response.status_code == 200:
                if not response.json()["feedbacks"]:
                    raise Exception("Сервер 1 не подошёл")
                return response.json()
        except Exception as err:
            response = requests.get(f'https://feedbacks2.wb.ru/feedbacks/v1/{self.root_id}', headers=HEADERS)
            if response.status_code == 200:
                return response.json()

    def get_root_id(self, sku: str):

        response = requests.get(
            f'https://card.wb.ru/cards/v2/detail?appType=1&curr=rub&dest=-1257786&hide_dtype=13&spp=30&ab_testing=false&lang=ru&nm={sku}',
            headers=HEADERS,
        )
        if response.status_code != 200:
            raise Exception("Не удалось определить root id")
       
        root_id = response.json()["data"]["products"][0]["root"]
        item_name = response.json()["data"]["products"][0]["name"]
        print(item_name)
        return root_id

    def parse(self):
        data = self.get_review()
        
        return data



# https://www.wildberries.ru/catalog/206392976/detail.aspx