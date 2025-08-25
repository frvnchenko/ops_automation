from lxml import etree
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import List, Optional, Union, Tuple
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.parser.XmlData import XML_DATA


@dataclass
class SuccessorsRecord:
    """Класс для записи офиса правопреемника"""

    code: str  # код тп
    name: str  # имя правопреемника
    address: str  # адресс правопреемника
    business_line: str  # потомок в определенной бизнес линии например в json salePointCodeDescendantFl


@dataclass
class ScheduleRecord:
    """Класс для записи расписания"""

    day: Tuple[int, str]
    hours: str


@dataclass
class HolidayRecord:
    """Класс для записи праздничного дня"""

    date: str
    hours: str


@dataclass
class BranchRecord:
    """Класс для записи филиала"""

    branch_id: str  # код тп
    branch_code: Tuple[int, str]  # из кодовой таблицы значение посмотреть чего
    branch_business_group: str  # филиал сейчас в json это fullOfficeName
    city: Tuple[int, str]  # из кодовой таблицы значение города
    address: str  # адресс
    metrostation: Tuple[int, str]  # из кодовой таблицы станция метро
    timezone: str
    cashdesk: int  # из кодовой таблицы обслуживание кассы
    msk_time_diff: int  # из кодовой таблицы разница с москвой


@dataclass
class XmlData:
    """Основной класс для десерилизованных данных XML"""

    status: Tuple[int, str]
    branch: BranchRecord
    successors: List[SuccessorsRecord]
    branch_segments: Tuple[int, str]
    branch_services: Tuple[int, str]
    branch_features: Tuple[int, str]
    coordinates: str
    cashdesk_schedule: List[ScheduleRecord]
    prime_schedule: List[ScheduleRecord]
    holidays_individual: List[HolidayRecord]
    holidays_cashbox: List[HolidayRecord]
    personal_schedule: List[ScheduleRecord]
    business_schedule: List[ScheduleRecord]
    temporary_personal: List[ScheduleRecord]
    temporary_business: List[ScheduleRecord]
    temporary_cashdesk: List[ScheduleRecord]
    personal_manager: List[ScheduleRecord]
    temporary_start_date: str
    temporary_end_date: str
    cashdesk_temporary_start: str
    cashdesk_temporary_end: str
    important_notes: str  # ограничения из-за трансформации
    sms_description: str


class XmlParser:
    def __init__(self, vrs_doc_active: str, vrs_doc_prev: str = "") -> None:
        self.vrs_doc_active = vrs_doc_active  # активная версия статьи
        self.vrs_doc_prev = vrs_doc_prev  # прошлая версия статьи

        try:
            self.tree = etree.fromstring(self.vrs_doc_active)
        except etree.XMLSyntaxError as e:
            logger.error(f"Ошибка парсинга XML: {e}")
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при инициализации парсера: {e}")
            raise

    def get_xpath_value(self, xpath: str) -> Union[List[str], str, None]:
        """Безопасное получение значения по XPath"""
        try:
            result = self.tree.xpath(xpath)

            if isinstance(result, list) and result:
                return [res.text for res in result if res.text is not None]
            elif result:
                return result[0].text
            else:
                return None
        except Exception as e:
            logger.warning(f"Ошибка при получении XPath {xpath}: {e}")
            return None

    def safe_find_text(self, element, tag: str, default: str = "") -> str:
        """Безопасное извлечение текста из элемента"""
        found = element.find(tag)
        return found.text if found is not None and found.text else default

    def safe_find_int(self, element, tag: str, default: int = 0) -> int:
        """Безопасное извлечение целого числа из элемента"""
        try:
            found = element.find(tag)
            return int(found.text) if found is not None and found.text else default
        except (ValueError, TypeError):
            return default

    def get_successors(
        self, path: str = "./E_SUC_OFFICE_CONT/RECORD"
    ) -> List[SuccessorsRecord]:
        """Получение списка офисов правопреемников"""
        main_lst = []
        try:
            for record in self.tree.findall(path):
                record_data = SuccessorsRecord(
                    code=self.safe_find_text(record, "E_SUC_OF_COD_TP"),
                    name=self.safe_find_text(record, "E_SUC_OF_NAME"),
                    address=self.safe_find_text(record, "E_SUC_OF_ADRESS"),
                    business_line=self.safe_find_text(record, "E_SUC_OF_BUSINESS_LINE"),
                )
                main_lst.append(record_data)
        except Exception as e:
            logger.error(f"Ошибка при получении successors: {e}")

        return main_lst

    def get_schedule_records(self, path: str) -> List[ScheduleRecord]:
        """Универсальный метод для получения записей расписания"""
        main_lst = []
        try:
            for record in self.tree.findall(path):
                day_tag = None
                hours_tag = None

                # Определяем теги для дней и часов
                for child in record:
                    if "DAY" in child.tag and "WORKING" in child.tag:
                        day_tag = child.tag
                    elif "WORKING" in child.tag and "HOURS" in child.tag:
                        hours_tag = child.tag

                if day_tag and hours_tag:
                    schedule_record = ScheduleRecord(
                        day=self.safe_find_int(record, day_tag),
                        hours=self.safe_find_text(record, hours_tag),
                    )
                    main_lst.append(schedule_record)
        except Exception as e:
            logger.error(f"Ошибка при получении расписания {path}: {e}")

        return main_lst

    def get_holiday_records(self, path: str) -> List[HolidayRecord]:
        """Универсальный метод для получения праздничных записей"""
        main_lst = []
        try:
            for record in self.tree.findall(path):
                date_tag = None
                hours_tag = None

                # Определяем теги для даты и часов
                for child in record:
                    if "DATE" in child.tag:
                        date_tag = child.tag
                    elif "WORKING" in child.tag and "HOURS" in child.tag:
                        hours_tag = child.tag

                if date_tag and hours_tag:
                    holiday_record = HolidayRecord(
                        date=self.safe_find_text(record, date_tag),
                        hours=self.safe_find_text(record, hours_tag),
                    )
                    main_lst.append(holiday_record)
        except Exception as e:
            logger.error(f"Ошибка при получении праздничных записей {path}: {e}")

        return main_lst

    def get_branch_record(self) -> BranchRecord:
        """Получение записи филиала"""
        try:
            branch_path = "/ITEM/E_BRUNCH/RECORD"
            branch_element = self.tree.xpath(branch_path)[0]

            return BranchRecord(
                branch_id=self.safe_find_text(branch_element, "E_BRANCH_ID"),  # код тп
                branch_code=(self.safe_find_int(branch_element, "E_BRINCH"), "BRUNCHE"),
                branch_business_group=self.safe_find_text(
                    branch_element, "E_BUSINESS_GROUP"
                ),
                city=(self.safe_find_int(branch_element, "E_CITY"), "CITY_BRANCH"),
                address=self.safe_find_text(branch_element, "E_ADRESS"),
                metrostation=(
                    self.safe_find_int(branch_element, "E_METROSTATION"),
                    "METROSTATION",
                ),
                timezone=self.safe_find_text(branch_element, "E_TIMEZONE"),
                cashdesk=(
                    self.safe_find_int(branch_element, "E_CASHDESK/VALUE"),
                    "CASHDESK",
                ),
                msk_time_diff=self.safe_find_int(branch_element, "E_MSK_TIME_DIFF"),
            )
        except Exception as e:
            logger.error(f"Ошибка при получении записи филиала: {e}")
            return None

    def safe_int_conversion(self, xpath_value: str) -> Tuple[int, str]:
        """Безопасное преобразование в целые числа"""
        try:
            values = self.get_xpath_value(xpath_value)
            if values:
                int_tuple = tuple(map(int, values))
                return int_tuple
            return (0,)
        except (TypeError, ValueError) as e:
            logger.warning(f"Ошибка преобразования в int для {xpath_value}: {e}")
            return (0,)

    def deserialize(self) -> XmlData:
        """XML в структурированный объект"""
        try:
            return XmlData(
                status=(self.safe_int_conversion("/ITEM/E_STATUS"), "STATUS"),
                branch=self.get_branch_record(),
                successors=self.get_successors(),
                branch_segments=(
                    self.safe_int_conversion("/ITEM/E_BRANCH_SEGMENT/VALUE"),
                    "BRANCH_SEGMENT",
                ),
                branch_services=(
                    self.safe_int_conversion("/ITEM/E_BRANCH_SERVICES/VALUE"),
                    "BRANCH_SERVICES",
                ),
                branch_features=(
                    self.safe_int_conversion("/ITEM/E_BRANCH_FEATURES/VALUE"),
                    "BRANCH_FEATURES",
                ),
                coordinates=self.get_xpath_value("/ITEM/E_COORDINATES") or "",
                cashdesk_schedule=(
                    self.get_schedule_records("./E_CASHDESK1/RECORD"),
                    "BRANCH_DAYS",
                ),
                holidays_individual=self.get_holiday_records(
                    "./E_HOLIDAYS_INDIVIDUAL/RECORD"
                ),
                holidays_cashbox=self.get_holiday_records(
                    "./E_HOLIDAYS_CASHBOX/RECORD"
                ),
                personal_schedule=(
                    self.get_schedule_records("./E_PERSONAL2/RECORD"),
                    "BRANCH_DAYS",
                ),
                business_schedule=(
                    self.get_schedule_records("./E_BUSINESS/RECORD"),
                    "BRANCH_DAYS",
                ),
                temporary_personal=(
                    self.get_schedule_records("./E_TEMPORARY_PERSONAL2/RECORD"),
                    "BRANCH_DAYS",
                ),
                temporary_business=(
                    self.get_schedule_records(
                        "./E_TEMPORARY_BUSINESS/RECORD",
                    ),
                    "BRANCH_DAYS",
                ),
                temporary_cashdesk=(
                    self.get_schedule_records("./E_TEMPORARY_CASHDESK1/RECORD"),
                    "BRANCH_DAYS",
                ),
                personal_manager=self.get_schedule_records(
                    "./E_PERSINAL_MANAGER/RECORD"
                ),
                temporary_start_date=self.get_xpath_value(
                    "/ITEM/E_TEMPORARY_START_DATE"
                )
                or "",
                temporary_end_date=self.get_xpath_value("/ITEM/E_TEMPORARY_END_DATE")
                or "",
                cashdesk_temporary_start=self.get_xpath_value(
                    "/ITEM/E_CASHDESK_TEMPORARY_START_DATE"
                )
                or "",
                cashdesk_temporary_end=self.get_xpath_value(
                    "/ITEM/E_CASHDESK_TEMPORARY_END_DATE"
                )
                or "",
                prime_schedule=(
                    self.get_schedule_records("./E_PFM_PRIME/RECORD"),
                    "BRANCH_DAYS",
                ),
                sms_description=self.get_xpath_value("SMS_DESCRIPTION") or "",
                important_notes=self.get_xpath_value("./E_WARNINGS_3") or "",
            )
        except Exception as e:
            logger.error(f"Ошибка при десерилизации: {e}")
            raise

    # Утилитарные методы для получения отдельных значений
    def get_status(self) -> Tuple[int, str]:
        """Получение статуса"""
        return self.safe_int_conversion("/ITEM/E_STATUS"), "STATUS"

    # код тп
    def get_branch_id(self) -> str:
        """Получение Кода ТП"""
        result = self.get_xpath_value("/ITEM/E_BRUNCH/RECORD/E_BRANCH_ID")
        return result[0] if result else ""

    def get_coordinates(self) -> str:
        """Получение координат"""
        return self.get_xpath_value("/ITEM/E_COORDINATES") or ""

    def get_sms_description(self) -> str:
        """Получение SMS описания"""
        result = self.get_xpath_value("SMS_DESCRIPTION")
        return result[0] if result else ""
