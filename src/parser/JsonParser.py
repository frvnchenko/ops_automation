import json
import pathlib


# добавлены расписания, при необходимости можешь добавить другие атрибуты
class JsonParser:
    def __init__(self, json_folder) -> None:

        self.json_path = self._get_articles_path(json_folder)
        self.__data = None

    def _load_json_file(self):
        with open(self.json_path, "r", encoding="utf-8") as json_file:
            json_file = json.load(json_file)
            # result = json.dumps(json_file, ensure_ascii=False, indent=4)
        return json_file

    def _get_articles_path(self, val):
        # путь к текущему файлу
        current_file = pathlib.Path(__file__)
        # (src/parser -> src -> корень проекта)
        project_root = current_file.parent.parent.parent
        # путь к data/create_articles
        articles_path = project_root / "data" / f"{val}"
        return articles_path

    def _get_data(self):
        if self.__data is None:
            self.__data = self._load_json_file()
        return self.__data

    def json_schedule_dict(self, schedule_type):
        data = self._get_data()
        schedule_data = data.get(schedule_type, [])

        if isinstance(schedule_data, list):
            print(schedule_data)
            try:
                return {item["days"]: item["hours"] for item in schedule_data}
            except KeyError:
                return {item["day"]: item["hours"] for item in schedule_data}
        else:
            return {}

    @property
    def openHours(self):
        data = self._get_data()
        return data.get("openHours", "openHours не найдены")

    @property
    def openHoursIndividual(self):
        data = self._get_data()
        return data.get("openHoursIndividual", "openHoursIndividual не найдены")

    @property
    def cashboxOpenHours(self):
        data = self._get_data()
        return data.get("cashboxOpenHours", "cashboxOpenHours не найдены")

    @property
    def temporaryOpenHours(self):
        data = self._get_data()
        return data.get("temporaryOpenHours", "temporaryOpenHours не найдены")

    @property
    def temporaryOpenHoursIndividual(self):
        data = self._get_data()
        return data.get(
            "temporaryOpenHoursIndividual", "temporaryOpenHoursIndividual не найдены"
        )

    @property
    def temporaryCashboxOpenHours(self):
        data = self._get_data()
        return data.get(
            "temporaryCashboxOpenHours", "temporaryCashboxOpenHours не найдены"
        )

    @property
    def holidayCashboxOpenHours(self):
        data = self._get_data()
        return data.get("holidayCashboxOpenHours", "holidayCashboxOpenHours не найдены")

    @property
    def holidayOpenHoursIndividuals(self):
        data = self._get_data()
        return data.get(
            "holidayOpenHoursIndividuals", "holidayOpenHoursIndividuals не найдены"
        )

    @property
    def longitude(self):
        data = self._get_data()
        return data.get("longitude")

    @property
    def latitude(self):
        data = self._get_data()
        return data.get("latitude")

    @property
    def cashboxStartDateTemporary(self):
        data = self._get_data()
        return data.get("cashboxStartDateTemporary")

    @property
    def cashboxEndDateTemporary(self):
        data = self._get_data()
        return data.get("cashboxEndDateTemporary")

    @property
    def temporaryOHStartDate(self):
        data = self._get_data()
        return data.get("temporaryOHStartDate")

    @property
    def temporaryOHEndDate(self):
        data = self._get_data()
        return data.get("temporaryOHEndDate")
