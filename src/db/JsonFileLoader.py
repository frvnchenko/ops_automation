import os
import json
from pathlib import Path

src_dir = Path(__file__).parent.parent
jsons_create = os.listdir(src_dir.parent / "data" / "create_articles")
target_dir_create = src_dir.parent / "data" / "create_articles"

jsons_update = os.listdir(src_dir.parent / "data" / "change_articles")
target_dir_update = src_dir.parent / "data" / "change_articles"

class JsonFileLoader:

    def __init__(self, target_dir=None, jsons=None) -> None:
        if jsons is None:
            jsons = jsons_create
        if target_dir is None:
            target_dir = target_dir_create
        self.target_dir = target_dir
        self.jsons = jsons
    def load_json_files(self):
        json_body = []
        salepoint_codes = []
        for item in self.jsons:
            with open(
                os.path.join(self.target_dir, item), "r", encoding="utf-8"
            ) as json_file:
                json_data = json.load(json_file)
                json_string = json.dumps(json_data)
                json_body.append(json_string)  # без этого json не жрется бд
                print(f"Данные из {item} добавлены")
                salepoint_codes.append(
                    json_data["salePointCode"]
                )  # все коды тп из всех файлов, подумай зачем оно может потребоваться
                json_file.close()
        # print(salepoint_codes)
        return (
            json_body,
            salepoint_codes,
        )  # был расширен метод чтобы возвращались еще все коды тп из json


