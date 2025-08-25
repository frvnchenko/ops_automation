from src.parser.XmlParser import (
    XmlParser,
    XmlData,
    SuccessorsRecord,
    ScheduleRecord,
    HolidayRecord,
    BranchRecord,
)

class TestUtils:

    @staticmethod
    def create_schedule_dict(schedule_data, db_repository, schedule_type):
        """
        Унифицированный метод для создания словаря расписания из XML данных

        Args:
            schedule_data: Список данных расписания из XML (например, tmp.personal_schedule[0])
            db_repository: Экземпляр DbRepository для работы с базой данных
            schedule_type: Тэг из кодовой таблицы, я оформляю его базово как  tmp.personal_schedule[-1]
        Returns:
            dict: Словарь с расписанием, где ключ - день недели, значение - часы работы
        """
        schedule_dict = {}

        if not schedule_data:
            print(f"Предупреждение: {schedule_type} расписание пустое или некорректное")
            return schedule_dict

        # Получаем тег для расшифровки дней недели (обычно последний элемент)
        day_tag = schedule_type if len(schedule_data) > 1 else None

        for item in schedule_data:
            if type(item) == ScheduleRecord:
                try:
                    # Получаем название дня недели из кодовой таблицы
                    day_key = db_repository.get_code_value_by_tag((item.day, day_tag))[
                        0
                    ].lower()
                    schedule_dict[day_key] = item.hours
                except (IndexError, AttributeError) as e:
                    print(f"Ошибка при обработке записи расписания {item}: {e}")
                    continue
            else:
                print(f"Пропущена запись неверного типа: {type(item)}")

        return schedule_dict

    @staticmethod
    def create_holiday_schedule_dict(schedule_data):
        schedule_dict = {}

        if not schedule_data:
            print(f"Предупреждение: {schedule_data} расписание пустое или некорректное")
            return schedule_dict
        for item in schedule_data:
            if type(item) == HolidayRecord:
                try:
                    # Получаем название дня недели из кодовой таблицы
                    day_key = item.date
                    schedule_dict[day_key] = item.hours
                except (IndexError, AttributeError) as e:
                    print(f"Ошибка при обработке записи расписания {item}: {e}")
                    continue
            else:
                print(f"Пропущена запись неверного типа: {type(item)}")

        return schedule_dict

    @staticmethod
    def compare_schedules(xml_schedule, json_schedule):
        if not (xml_schedule or json_schedule):
            print(f"расписание пустое")
            return False

        for day in xml_schedule:
            if day in json_schedule:
                if xml_schedule[day] != json_schedule[day]:
                    print(
                        f"Различные {day}: XML={xml_schedule[day]}, JSON={json_schedule[day]}"
                    )
                    return False
            else:
                print(f"{day}: отсутствует в JSON")
        return True
    @staticmethod
    def check_successor(successors, business_line, suc_code):
        print(business_line)
        fl = False
        for i in successors:
            if i.business_line == business_line:
                if (
                        i.code == suc_code
                        and i.name != "Отделение не найдено"
                        and i.address != ""
                ):
                    fl = True
                    return fl
        return fl
