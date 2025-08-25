import xml
import pytest
from datetime import datetime
from src.db.DbRepository import DbRepository
from utils.TestUtils import TestUtils

from src.parser.XmlParser import (
    XmlParser,
    XmlData,
    SuccessorsRecord,
    ScheduleRecord,
    HolidayRecord,
    BranchRecord,
)

from src.parser.JsonParser import JsonParser


# для значений из кодовых таблиц обязательно используешь tuple где (значения, тэг)


@pytest.mark.order(5)
# 1 открытый тип офиса
def test_get_status_value_open(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000001")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Открыт" == db_req.get_code_value_by_tag(tmp.status)[0]


@pytest.mark.order(6)
# 2 открытый тип офиса, доступ в офис ограничен
def test_get_status_value_closed_office_type(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000002")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Доступ в офис ограничен" in (
        db_req.get_code_value_by_tag(tmp.branch_features)
    )


@pytest.mark.order(7)
# 3 офис со статусом закрыт
def test_get_status_value_closed(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000003")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Закрыт" == db_req.get_code_value_by_tag(tmp.status)[0]


@pytest.mark.order(9)
# 4 статья со статусом скоро откроется
def test_get_status_value_planned(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000004")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Скоро откроется" == db_req.get_code_value_by_tag(tmp.status)[0]


@pytest.mark.order(10)
# 5 статья со статусом временно закрыт
def test_get_status_value_temp_closed(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000005")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Временно закрыт" == db_req.get_code_value_by_tag(tmp.status)[0]


@pytest.mark.skip(reason="Уточнение требований по сокращению (ПАО)")
@pytest.mark.order(11)
# 6 статья с филиалом fullofficename
def test_get_fullofficename(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000006")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "№ 2352 Банка ВТБ (публичное акционерное общество) в г. Краснодаре"
        == db_req.get_code_value_by_tag(tmp.branch.branch_code)[0]
    )


@pytest.mark.order(12)
# 7 статья с филиалом тестовый филиал rooBg
def test_get_bisness_group(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000007")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "РОО «сладкий тест»" == tmp.branch.branch_business_group


@pytest.mark.order(13)
# 8 статья с городом city
def test_get_city(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000008")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "бади" == (db_req.get_code_value_by_tag(tmp.branch.city))[0]


@pytest.mark.order(14)
# 9 статья с shortadress
def test_get_adress(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000009")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "г. Астрахань, ул. Яблочковe, д. 51 лит. Desert" == tmp.branch.address


@pytest.mark.order(15)
# 10 станция метро, есть вопросы т.к сетим первое подходящее (на уточнении, тест исправлен под тестовые данные опс)
def test_get_metrostation(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000009")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "метро метро метро оооо"
        == (db_req.get_code_value_by_tag(tmp.branch.metrostation))[0]
    )


# [+] TODO доработать сравнение с файлом json
# 11 кассовое обслуживание , наличие графика кассы, касса в доп услугах
@pytest.mark.order(16)
def test_check_cashdesk(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000011")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Касса" in db_req.get_code_value_by_tag(tmp.branch_services)
    assert (
        f'Режим обслуживания "Касса"'
        == db_req.get_code_value_by_tag(tmp.branch.cashdesk)[0]
    )

    cashdesk_schedule = TestUtils.create_schedule_dict(
        tmp.cashdesk_schedule[0], db_req, tmp.cashdesk_schedule[-1]
    )

    tmp_json = JsonParser("create_articles/11.json")

    # создание словаря из JSON для прямого сравнения
    json_schedule = tmp_json.json_schedule_dict("cashboxOpenHours")

    assert True == TestUtils.compare_schedules(cashdesk_schedule, json_schedule)


# 12 статья без кассового обслуживания
@pytest.mark.order(17)
def test_check_without_cashdesk(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000012")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Касса" not in db_req.get_code_value_by_tag(tmp.branch_services)
    assert (
        f"Без кассового обслуживания"
        == db_req.get_code_value_by_tag(tmp.branch.cashdesk)[0]
    )
    assert [] == tmp.cashdesk_schedule[0]


# 13 статья с часовым поясом UTC +06:00
@pytest.mark.order(18)
def test_utc_time_zone(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000013")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "UTC +06:00" == tmp.branch.timezone


# 14 статья с офисом массового сегмента
@pytest.mark.order(19)
def test_mass_segment(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000014")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Массовый сегмент" in db_req.get_code_value_by_tag((tmp.branch_segments))


# 15 статья Обслуживает ФЛ
# Сегменты клиентов Обслуживает ФЛ + График ФЛ
@pytest.mark.order(20)
def test_served_bussines_fl(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000015")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/15.json")
    json_schedule = tmp_json.json_schedule_dict("openHoursIndividual")

    personal_schedule = TestUtils.create_schedule_dict(
        tmp.personal_schedule[0], db_req, tmp.personal_schedule[-1]
    )
    # print("XML расписание:", personal_schedule)
    # print("JSON расписание:", json_schedule)
    assert True == TestUtils.compare_schedules(personal_schedule, json_schedule)
    assert "Обслуживает ФЛ" in db_req.get_code_value_by_tag((tmp.branch_segments))


# 16 Статья Обслуживает ЮЛ
# Сегменты клиентов Обслуживает ЮЛ + Наличие графика ЮЛ
@pytest.mark.order(21)
def test_served_bussines_ul(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000016")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/16.json")
    json_schedule = tmp_json.json_schedule_dict("openHours")

    business_schedule = TestUtils.create_schedule_dict(
        tmp.business_schedule[0], db_req, tmp.business_schedule[-1]
    )
    assert True == TestUtils.compare_schedules(business_schedule, json_schedule)
    assert "Обслуживает ЮЛ" in db_req.get_code_value_by_tag(tmp.branch_segments)


# 17 статья есть РКО , ЮЛ. Новые клиенты в сегментах клиентов
@pytest.mark.order(22)
def test_hasRKO(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000017")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "ЮЛ. Новые клиенты" in db_req.get_code_value_by_tag(tmp.branch_segments)


# 18 статья Привилегия (РБ) Проверить Только Привилегия + проверить график Персонального менеджера как у ФЛ
@pytest.mark.order(23)
def test_privilege(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000018")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    personal_schedule = TestUtils.create_schedule_dict(
        tmp.personal_schedule[0], db_req, tmp.personal_schedule[-1]
    )
    tmp_json = JsonParser("create_articles/18.json")
    json_schedule = tmp_json.json_schedule_dict("openHoursIndividual")

    assert True == TestUtils.compare_schedules(personal_schedule, json_schedule)
    assert "Только Привилегия" in db_req.get_code_value_by_tag(tmp.branch_segments)


# 19 статья Прайм (РБ) Проверить Только VIP Клиенты
# где 19 "salePointFormat": "Прайм (РБ)"
# где 21 "salePointFormat": "Прайм (РБ) БФКО"
@pytest.mark.order(24)
@pytest.mark.parametrize("code_tp", ["000019", "000021"])
def test_vip(db_connect, code_tp):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp(code_tp)
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "Только VIP клиенты" in db_req.get_code_value_by_tag(tmp.branch_segments)


# 20 статья premium: Прайм , проверить наличие ПФМ Прайм в доп услугах + график как у ФЛ
@pytest.mark.order(25)
def test_prime(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000020")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    prime_schedule = TestUtils.create_schedule_dict(
        tmp.prime_schedule[0], db_req, tmp.prime_schedule[-1]
    )
    tmp_json = JsonParser("create_articles/20.json")
    json_schedule = tmp_json.json_schedule_dict("openHoursIndividual")
    assert "ПФМ Прайм" in db_req.get_code_value_by_tag(tmp.branch_services)
    assert True == TestUtils.compare_schedules(prime_schedule, json_schedule)

# [] TODO добавить это в параметризацию tmp.branch_services
# 22 статья ВТБ Мобайл Проверить ВТБ Мобайл в доп услугах
@pytest.mark.order(26)
def test_vtb_mobile(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000022")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "ВТБ Мобайл" in db_req.get_code_value_by_tag(tmp.branch_services)

# 23 статья "premium" : Зона Привилегия
# 24 статья "premium" : Зона Привилегия
# Проверить ПМ Привилегии в доп услугах
# Проверить график ПМ как ФЛ
@pytest.mark.order(27)
@pytest.mark.parametrize("code_tp", ["000022", "000023"])
def test_zone_privilege(db_connect, code_tp):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp(code_tp)
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    personal_schedule = TestUtils.create_schedule_dict(
        tmp.personal_schedule[0], db_req, tmp.personal_schedule[-1]
    )
    tmp_json = JsonParser("create_articles/18.json")
    json_schedule = tmp_json.json_schedule_dict("openHoursIndividual")
    assert "ПМ Привилегии" in db_req.get_code_value_by_tag(tmp.branch_services)
    assert True == TestUtils.compare_schedules(personal_schedule, json_schedule)

# [] TODO добавить это в параметризацию tmp.branch_services
# 25 json ИБС hasSafeDepositBox:Y Проверить ИБС в доп услугах
@pytest.mark.order(28)
def test_ibs(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000025")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert "ИБС" in db_req.get_code_value_by_tag(tmp.branch_services)

#@pytest.mark.skip(reason = "доработка параметризации для tmp.branch_features")
@pytest.mark.order(29)
@pytest.mark.parametrize("code_tp,feature",[
        ("000026", "Работает в субботу"),
        ("000027", "Работает в будни после 19:00"),
        ("000028","Подходит для маломобильных клиентов"),
        ("000029", "Работает в воскресенье"),
        ("000030", "Доступ в офис ограничен"),
    ],
    ids=["sat", "after19","hasRamp", "sun", "closed_office_type"])
def test_branch_feature(db_connect,code_tp,feature):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp(code_tp)
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert feature in db_req.get_code_value_by_tag(tmp.branch_features)



# ДОБАВИТЬ ВСЕ СТАТЬИ В БФКО БЛОКИ ПОЗЖЕ БУДЕТ ОБНОВЛЕНО С ЗАКАЗЧИКОМ  доработать
# 31.json - УРМ ВТБ В БФКО 000031
# Проверить приписку УРМ ВТБ В БФКО
# Проверить заполненное примечание
# Проверить особенность обслуживания  УРМ ВТБ В БФКО
# @pytest.mark.skip(reason="пропущен бфко тест")
@pytest.mark.order(34)
def test_yrm_vtb_bfko(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000031")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "Правила навигации" in tmp.important_notes[0]
    )  # подумать как улучшить проверку с гиперссылкой
    assert "УРМ ВТБ в БФКО" in (db_req.get_article_name_by_id(article_id))
    assert "УРМ ВТБ в БФКО" in (db_req.get_code_value_by_tag(tmp.branch_features))


# 32.json - ЭКС БФКО 000032
# Проверить заполненное примечание
# Проверить особенность обслуживания Офис с ПО БФКО
@pytest.mark.order(35)
def test_ex_vtb_bfko(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000032")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "Правила навигации" in tmp.important_notes[0]
    )  # подумать как улучшить проверку с гиперссылкой

    assert "Офис с ПО БФКО" in (db_req.get_code_value_by_tag(tmp.branch_features))


# 33.json - УРМ ВТБ В РНКБ 000033
# Проверить приписку УРМ ВТБ В РНКБ
# Проверить заполненное примечание
# Проверить особенность обслуживания  УРМ ВТБ В РНКБ
@pytest.mark.order(36)
def test_yrm_vtb_rnkb(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000033")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "Правила навигации" in tmp.important_notes[0]
    )  # подумать как улучшить проверку с гиперссылкой
    assert "УРМ ВТБ в РНКБ" in (db_req.get_article_name_by_id(article_id))
    assert "УРМ ВТБ в РНКБ" in (db_req.get_code_value_by_tag(tmp.branch_features))


# 34.json - ЭКС РНКБ 000034 +
# Проверить заполненное примечание
# Проверить особенность обслуживания Офис с ПО РНКБ


@pytest.mark.order(37)
def test_ex_vtb_rnkb(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000034")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    assert (
        "Правила навигации" in tmp.important_notes[0]
    )  # подумать как улучшить проверку с гиперссылкой

    assert "Офис с ПО РНКБ" in (db_req.get_code_value_by_tag(tmp.branch_features))


# 35.json - УРМ ВТБ В ПОЧТА БАНКЕ 000035
# Проверить приписку УРМ ВТБ В ПОЧТА БАНКЕ
# Проверить особенность обслуживания  УРМ ВТБ В ПОЧТА БАНКЕ
@pytest.mark.order(38)
def test_yrm_vtb_pochta_bank(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000035")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    assert "УРМ ВТБ в Почта Банке" in (db_req.get_article_name_by_id(article_id))
    assert "УРМ ВТБ в Почта Банке" in (
        db_req.get_code_value_by_tag(tmp.branch_features)
    )


# 36.json - ОФИС С ПО ПОЧТА БАНКА 000036
# Проверить особенность обслуживания  ОФИС С ПО ПОЧТА БАНКА
@pytest.mark.order(39)
def test_office_vtb_pochta_bank(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000036")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    assert "Офис с ПО Почта Банка" in (
        db_req.get_code_value_by_tag(tmp.branch_features)
    )


# где 37.json - Режим обслуживания Касса
# HasPPRKO: Y
# Проверить
# Добавляется в Режим кассового обслуживания Режим обслуживания "Касса"+ в Доп услуги добавляется Касса
@pytest.mark.order(40)
def test_hasPPRKO_Y(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000037")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    assert 'Режим обслуживания "Касса"' in (
        db_req.get_code_value_by_tag(tmp.branch.cashdesk)
    )
    assert "Касса" in (db_req.get_code_value_by_tag(tmp.branch_services))


# где 38.json - Режим обслуживания Касса
# HasPPRKO: N
# Добавляется в Режим кассового обслуживания "Без кассового обслуживания"


@pytest.mark.order(41)
def test_hasPPRKO_N(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000038")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    assert "Без кассового обслуживания" in (
        db_req.get_code_value_by_tag(tmp.branch.cashdesk)
    )
    assert "Касса" not in (db_req.get_code_value_by_tag(tmp.branch_services))


# 000045 +
# где 45.json Все правопреемники с нужной бизнес линией и кодом тп "000001"
@pytest.mark.order(42)
@pytest.mark.parametrize(
    "business_line",
    ["ФЛ", "ЮЛ", "КИБ", "ЗП проекты", "Привилегия", "Ипотека ОКСИК", "Ипотека ЦИК/ОИК"],
)
def test_salePointCodeDescendants(db_connect, business_line):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000045")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()

    assert True == TestUtils.check_successor(tmp.successors, business_line, "000001")


# 000046 +
# где 46.json - Координаты
# {latitude: "57.1234500"} + {longitude: "59.1234500"}
# Проверить долготу и широту
@pytest.mark.order(43)
def test_coordinates(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000046")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/46.json")
    coordinates = tmp.coordinates[0].split(",")
    latitude, longitude = coordinates[0].strip(), coordinates[1].strip()
    assert longitude == tmp_json.longitude
    assert latitude == tmp_json.latitude


# 000047 +
# где 47.json - Временный режим работы кассы (Действующим)
@pytest.mark.order(44)
def test_cashbox_temporary_schedule(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000047")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/47.json")

    xml_cashdesk_schedule = TestUtils.create_schedule_dict(
        tmp.temporary_cashdesk[0], db_req, tmp.temporary_cashdesk[-1]
    )

    cashdesk_start_xml = tmp.cashdesk_temporary_start[0]
    cashdesk_end_xml = tmp.cashdesk_temporary_end[0]
    format_xml = "%d/%m/%Y"
    format_json = "%d.%m.%Y"
    datetime_obj_start_json = datetime.strptime(
        tmp_json.cashboxStartDateTemporary, format_json
    )
    datetime_obj_start_xml = datetime.strptime(cashdesk_start_xml, format_xml)

    datetime_obj_end_json = datetime.strptime(
        tmp_json.cashboxEndDateTemporary, format_json
    )
    datetime_obj_end_xml = datetime.strptime(cashdesk_end_xml, format_xml)

    json_schedule_temporaryCashboxOpenHours = tmp_json.json_schedule_dict(
        "temporaryCashboxOpenHours"
    )
    # print(json_schedule_temporaryCashboxOpenHours)
    # print(xml_cashdesk_schedule)
    assert datetime_obj_start_json == datetime_obj_start_xml
    assert datetime_obj_end_json == datetime_obj_end_xml
    assert True == TestUtils.compare_schedules(
        xml_cashdesk_schedule, json_schedule_temporaryCashboxOpenHours
    )


# 000048 +
# где 48.json - Временный режим работы кассы (Истекшим)
@pytest.mark.order(45)
def test_cashbox_temporary_schedule_expired(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000048")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/48.json")

    xml_cashdesk_schedule = TestUtils.create_schedule_dict(
        tmp.temporary_cashdesk[0], db_req, tmp.temporary_cashdesk[-1]
    )

    cashdesk_start_xml = tmp.cashdesk_temporary_start[0]
    cashdesk_end_xml = tmp.cashdesk_temporary_end[0]
    format_xml = "%d/%m/%Y"
    format_json = "%d.%m.%Y"
    datetime_obj_start_json = datetime.strptime(
        tmp_json.cashboxStartDateTemporary, format_json
    )
    datetime_obj_start_xml = datetime.strptime(cashdesk_start_xml, format_xml)

    datetime_obj_end_json = datetime.strptime(
        tmp_json.cashboxEndDateTemporary, format_json
    )
    datetime_obj_end_xml = datetime.strptime(cashdesk_end_xml, format_xml)

    json_schedule_temporaryCashboxOpenHours = tmp_json.json_schedule_dict(
        "temporaryCashboxOpenHours"
    )
    # print(json_schedule_temporaryCashboxOpenHours)
    # print(xml_cashdesk_schedule)
    assert datetime_obj_start_json == datetime_obj_start_xml
    assert datetime_obj_end_json == datetime_obj_end_xml
    assert True == TestUtils.compare_schedules(
        xml_cashdesk_schedule, json_schedule_temporaryCashboxOpenHours
    )


@pytest.mark.order(46)
def test_cashbox_temporary_schedule_not_found(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000049")
    assert None == article_id


# 000050 +
# где 50.json - Временный режим работы ФЛ (Действующий)
@pytest.mark.order(47)
def test_temporary_openHoursIndividual(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000050")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/50.json")
    start_date_xml, end_date_xml = (
        tmp.temporary_start_date[0],
        tmp.temporary_end_date[0],
    )
    format_xml = "%d/%m/%Y"
    format_json = "%d.%m.%Y"
    datetime_obj_start_xml = datetime.strptime(start_date_xml, format_xml)
    datetime_obj_end_xml = datetime.strptime(end_date_xml, format_xml)

    datetime_obj_start_json = datetime.strptime(
        tmp_json.temporaryOHStartDate, format_json
    )
    datetime_obj_end_json = datetime.strptime(tmp_json.temporaryOHEndDate, format_json)

    # print(tmp_json.openHoursIndividual)

    xml_openHoursIndividual_schedule = TestUtils.create_schedule_dict(
        tmp.temporary_personal[0], db_req, tmp.temporary_personal[-1]
    )

    json_schedule_openHoursIndividual = tmp_json.json_schedule_dict(
        "temporaryOpenHoursIndividual"
    )

    assert True == (
        TestUtils.compare_schedules(
            xml_openHoursIndividual_schedule, json_schedule_openHoursIndividual
        )
    )
    assert datetime_obj_start_xml == datetime_obj_start_json
    assert datetime_obj_end_xml == datetime_obj_end_json


# 000051 +
# где 51.json - Временный режим работы ФЛ (Истекший)
@pytest.mark.order(48)
def test_temporary_schedule_expired(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000051")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/51.json")
    start_date_xml, end_date_xml = (
        tmp.temporary_start_date[0],
        tmp.temporary_end_date[0],
    )
    format_xml = "%d/%m/%Y"
    format_json = "%d.%m.%Y"
    datetime_obj_start_xml = datetime.strptime(start_date_xml, format_xml)
    datetime_obj_end_xml = datetime.strptime(end_date_xml, format_xml)

    datetime_obj_start_json = datetime.strptime(
        tmp_json.temporaryOHStartDate, format_json
    )
    datetime_obj_end_json = datetime.strptime(tmp_json.temporaryOHEndDate, format_json)

    # print(tmp_json.openHoursIndividual)

    xml_openHoursIndividual_schedule = TestUtils.create_schedule_dict(
        tmp.temporary_personal[0], db_req, tmp.temporary_personal[-1]
    )

    json_schedule_openHoursIndividual = tmp_json.json_schedule_dict(
        "temporaryOpenHoursIndividual"
    )

    assert True == (
        TestUtils.compare_schedules(
            xml_openHoursIndividual_schedule, json_schedule_openHoursIndividual
        )
    )
    assert datetime_obj_start_xml == datetime_obj_start_json
    assert datetime_obj_end_xml == datetime_obj_end_json


# 000052 +
# где 52.json - Временный режим работы ФЛ (null дата начала , дата окончания)
@pytest.mark.order(49)
def test_temporary_schedule_not_found(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000052")
    assert None == article_id


# 000053
# где 53.json - работа в праздники фл  (при обновлении перепроверить)
@pytest.mark.order(50)
def test_holidayOpenHoursIndividuals(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000053")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/53.json")

    xml_holiday_schedule = TestUtils.create_holiday_schedule_dict(tmp.holidays_individual)
    json_holiday_schedule = tmp_json.json_schedule_dict("holidayOpenHoursIndividuals")

    assert True == TestUtils.compare_schedules(xml_holiday_schedule,json_holiday_schedule)
    assert "Обслуживает ФЛ" in db_req.get_code_value_by_tag(tmp.branch_segments)


# 000054 +
# где 54.json - работа в праздники касса
@pytest.mark.order(51)
def test_holidayCashboxOpenHours(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    article_id = db_req.get_article_id_by_code_tp("000054")
    active_ver_xml = db_req.get_active_ver(article_id)
    xml_article = XmlParser(active_ver_xml)
    tmp = xml_article.deserialize()
    tmp_json = JsonParser("create_articles/54.json")

    xml_holiday_schedule = TestUtils.create_holiday_schedule_dict(tmp.holidays_cashbox)

    json_holiday_schedule = tmp_json.json_schedule_dict("holidayCashboxOpenHours")

    assert True == TestUtils.compare_schedules(xml_holiday_schedule, json_holiday_schedule)
    assert "Касса" in db_req.get_code_value_by_tag(tmp.branch_services)
    assert (
            f'Режим обслуживания "Касса"'
            == db_req.get_code_value_by_tag(tmp.branch.cashdesk)[0]
    )