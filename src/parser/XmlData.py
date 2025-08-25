# Парсинг XML
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Union, Optional
from dataclasses import dataclass, field
from datetime import datetime

XML_DATA = """
    <ITEM>
        <E_SUC_OFFICE_CONT fix_header="1" height="" viewmode="-1">
            <RECORD id="2" order="2">
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>ФЛ</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="10" order="10">
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>ЗП проекты</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="11" order="11">
                <E_SUC_OF_BUSINESS_LINE>ЗП проекты</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>0101</E_SUC_OF_COD_TP>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="13" order="13">
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>ЗП проекты</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="18" order="18">
                <E_SUC_OF_BUSINESS_LINE>Ипотека ОКСИК</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
            </RECORD>
            <RECORD id="8" order="8">
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>КИБ</E_SУC_OF_BUSINESS_LINE>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="5" order="5">
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>ЮЛ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="22" order="22">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ЦИК/ОИК</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="25" order="25">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ЦИК/ОИК</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="19" order="19">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_COD_TP>0101</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ОКСИК</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="1" order="1">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>ФЛ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
            </RECORD>
            <RECORD id="23" order="23">
                <E_SUC_OF_COD_TP>0101</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ЦИК/ОИК</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="16" order="16">
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>Привилегия</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="15" order="15">
                <E_SUC_OF_BUSINESS_LINE>Привилегия</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>0101</E_SUC_OF_COD_TP>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="9" order="9">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>КИБ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
            </RECORD>
            <RECORD id="3" order="3">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>ФЛ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
            </RECORD>
            <RECORD id="4" order="4">
                <E_SUC_OF_BUSINESS_LINE>ЮЛ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_ADRESS/>
            </RECORD>
            <RECORD id="17" order="17">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>Привилегия</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="14" order="14">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>Привилегия</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
            <RECORD id="20" order="20">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ОКСИК</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="7" order="7">
                <E_SUC_OF_COD_TP>1720</E_SUC_OF_COD_TP>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>КИБ</E_SUC_OF_BUSINESS_LINE>
            </RECORD>
            <RECORD id="21" order="21">
                <E_SUC_OF_BUSINESS_LINE>Ипотека ОКСИК</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
            </RECORD>
            <RECORD id="6" order="6">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_BUSINESS_LINE>ЮЛ</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>21319</E_SUC_OF_COD_TP>
            </RECORD>
            <RECORD id="24" order="24">
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
                <E_SUC_OF_BUSINESS_LINE>Ипотека ЦИК/ОИК</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_ADRESS/>
            </RECORD>
            <RECORD id="12" order="12">
                <E_SUC_OF_ADRESS/>
                <E_SUC_OF_COD_TP>0001</E_SUC_OF_COD_TP>
                <E_SUC_OF_BUSINESS_LINE>ЗП проекты</E_SUC_OF_BUSINESS_LINE>
                <E_SUC_OF_NAME>Отделение не найдено</E_SUC_OF_NAME>
            </RECORD>
        </E_SUC_OFFICE_CONT>
        <E_TEMPORARY_END_DATE day="14" month="12" viewmode="-1" year="2024">14/12/2024</E_TEMPORARY_END_DATE>
        <E_TEMPORARY_PERSONAL2 fix_header="1" height="" viewmode="-1">
            <RECORD id="2" order="2">
                <E_TEMPORARY_DAY_WORKING_HOURS2>1</E_TEMPORARY_DAY_WORKING_HOURS2>
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="6" order="6">
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
                <E_TEMPORARY_DAY_WORKING_HOURS2>6</E_TEMPORARY_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="4" order="4">
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
                <E_TEMPORARY_DAY_WORKING_HOURS2>4</E_TEMPORARY_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="1" order="1">
                <E_TEMPORARY_DAY_WORKING_HOURS2>2</E_TEMPORARY_DAY_WORKING_HOURS2>
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="7" order="7">
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
                <E_TEMPORARY_DAY_WORKING_HOURS2>7</E_TEMPORARY_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="3" order="3">
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
                <E_TEMPORARY_DAY_WORKING_HOURS2>3</E_TEMPORARY_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="5" order="5">
                <E_TEMPORARY_WORKING_HOURS2>12:06-20:00</E_TEMPORARY_WORKING_HOURS2>
                <E_TEMPORARY_DAY_WORKING_HOURS2>5</E_TEMPORARY_DAY_WORKING_HOURS2>
            </RECORD>
        </E_TEMPORARY_PERSONAL2>
        <E_PERSINAL_MANAGER fix_header="1" height="" viewmode="1">
            <RECORD id="6" order="6">
                <E_WORKING_HOURS6>выходной</E_WORKING_HOURS6>
                <E_DAY_WORKING_HOURS6>6</E_DAY_WORKING_HOURS6>
            </RECORD>
            <RECORD id="5" order="5">
                <E_DAY_WORKING_HOURS6>5</E_DAY_WORKING_HOURS6>
                <E_WORKING_HOURS6>13:03-18:00</E_WORKING_HOURS6>
            </RECORD>
            <RECORD id="4" order="4">
                <E_DAY_WORKING_HOURS6>4</E_DAY_WORKING_HOURS6>
                <E_WORKING_HOURS6>13:02-18:00</E_WORKING_HOURS6>
            </RECORD>
            <RECORD id="1" order="1">
                <E_WORKING_HOURS6>13:01-18:00</E_WORKING_HOURS6>
                <E_DAY_WORKING_HOURS6>2</E_DAY_WORKING_HOURS6>
            </RECORD>
            <RECORD id="7" order="7">
                <E_DAY_WORKING_HOURS6>7</E_DAY_WORKING_HOURS6>
                <E_WORKING_HOURS6>выходной</E_WORKING_HOURS6>
            </RECORD>
            <RECORD id="2" order="2">
                <E_DAY_WORKING_HOURS6>1</E_DAY_WORKING_HOURS6>
                <E_WORKING_HOURS6>13:01-18:00</E_WORKING_HOURS6>
            </RECORD>
            <RECORD id="3" order="3">
                <E_WORKING_HOURS6>13:01-18:00</E_WORKING_HOURS6>
                <E_DAY_WORKING_HOURS6>3</E_DAY_WORKING_HOURS6>
            </RECORD>
        </E_PERSINAL_MANAGER>
        <E_BRANCH_FEATURES selectdisplaymode="list" viewmode="-1"/>
        <E_BUSINESS fix_header="1" height="" viewmode="1">
            <RECORD id="3" order="3">
                <E_DAY_WORKING_HOURS3>3</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>10:00-19:00</E_WORKING_HOURS3>
            </RECORD>
            <RECORD id="6" order="6">
                <E_WORKING_HOURS3>выходной</E_WORKING_HOURS3>
                <E_DAY_WORKING_HOURS3>6</E_DAY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="4" order="4">
                <E_DAY_WORKING_HOURS3>4</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>10:00-19:00</E_WORKING_HOURS3>
            </RECORD>
            <RECORD id="1" order="1">
                <E_DAY_WORKING_HOURS3>2</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>10:30-19:30</E_WORKING_HOURS3>
            </RECORD>
            <RECORD id="2" order="2">
                <E_DAY_WORKING_HOURS3>1</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>09:00-19:00</E_WORKING_HOURS3>
            </RECORD>
            <RECORD id="5" order="5">
                <E_DAY_WORKING_HOURS3>5</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>10:00-19:00</E_WORKING_HOURS3>
            </RECORD>
            <RECORD id="7" order="7">
                <E_DAY_WORKING_HOURS3>7</E_DAY_WORKING_HOURS3>
                <E_WORKING_HOURS3>выходной</E_WORKING_HOURS3>
            </RECORD>
        </E_BUSINESS>
        <E_DATE_OF_APPROVAL day="" month="" year=""/>
        <E_PERSONAL2 fix_header="1" height="" viewmode="1">
            <RECORD id="3" order="3">
                <E_WORKING_HOURS2>13:01-18:00</E_WORKING_HOURS2>
                <E_DAY_WORKING_HOURS2>3</E_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="2" order="2">
                <E_WORKING_HOURS2>13:01-18:00</E_WORKING_HOURS2>
                <E_DAY_WORKING_HOURS2>1</E_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="4" order="4">
                <E_DAY_WORKING_HOURS2>4</E_DAY_WORKING_HOURS2>
                <E_WORKING_HOURS2>13:02-18:00</E_WORKING_HOURS2>
            </RECORD>
            <RECORD id="5" order="5">
                <E_WORKING_HOURS2>13:03-18:00</E_WORKING_HOURS2>
                <E_DAY_WORKING_HOURS2>5</E_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="6" order="6">
                <E_WORKING_HOURS2>выходной</E_WORKING_HOURS2>
                <E_DAY_WORKING_HOURS2>6</E_DAY_WORKING_HOURS2>
            </RECORD>
            <RECORD id="7" order="7">
                <E_DAY_WORKING_HOURS2>7</E_DAY_WORKING_HOURS2>
                <E_WORKING_HOURS2>выходной</E_WORKING_HOURS2>
            </RECORD>
            <RECORD id="1" order="1">
                <E_DAY_WORKING_HOURS2>2</E_DAY_WORKING_HOURS2>
                <E_WORKING_HOURS2>13:01-18:00</E_WORKING_HOURS2>
            </RECORD>
        </E_PERSONAL2>
        <E_MORTGAGE_DEPARTMENT_2 field_caption="" fix_header="1" height="" viewcaption="on" viewcaptionhidden="yes" viewmode="-1"/>
        <E_BRUNCH fix_header="1" height="" viewmode="-1">
            <RECORD id="1" order="1">
                <E_BRINCH>110</E_BRINCH>
                <E_BUSINESS_GROUP>РОО «сладкий»</E_BUSINESS_GROUP>
                <E_METROSTATION>345</E_METROSTATION>
                <E_TIMEZONE>UTC +06:00</E_TIMEZONE>
                <E_BRANCH_ID>000001</E_BRANCH_ID>
                <E_CASHDESK>
                    <VALUE>2</VALUE>
                </E_CASHDESK>
                <E_CITY>929</E_CITY>
                <E_ADRESS>г. Астрахань, ул. Яблочковe, д. 51 лит.</E_ADRESS>
                <E_MSK_TIME_DIFF>4</E_MSK_TIME_DIFF>
            </RECORD>
        </E_BRUNCH>
        <E_TEMPORARY_START_DATE day="09" month="12" viewmode="-1" year="2024">09/12/2024</E_TEMPORARY_START_DATE>
        <E_TEMPORARY_CASHDESK1 fix_header="1" height="" viewmode="1">
            <RECORD id="1" order="1">
                <E_TEMPORARY_DAY_WORKING_HOURS12>2</E_TEMPORARY_DAY_WORKING_HOURS12>
                <E_TEMPORARY_WORKING_HOURS12>13:01-20:00</E_TEMPORARY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="3" order="3">
                <E_TEMPORARY_DAY_WORKING_HOURS12>3</E_TEMPORARY_DAY_WORKING_HOURS12>
                <E_TEMPORARY_WORKING_HOURS12>13:01-20:00</E_TEMPORARY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="7" order="7">
                <E_TEMPORARY_DAY_WORKING_HOURS12>7</E_TEMPORARY_DAY_WORKING_HOURS12>
                <E_TEMPORARY_WORKING_HOURS12>13:05-20:00</E_TEMPORARY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="4" order="4">
                <E_TEMPORARY_WORKING_HOURS12>13:02-20:00</E_TEMPORARY_WORKING_HOURS12>
                <E_TEMPORARY_DAY_WORKING_HOURS12>4</E_TEMPORARY_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="2" order="2">
                <E_TEMPORARY_WORKING_HOURS12>13:01-20:00</E_TEMPORARY_WORKING_HOURS12>
                <E_TEMPORARY_DAY_WORKING_HOURS12>1</E_TEMPORARY_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="6" order="6">
                <E_TEMPORARY_WORKING_HOURS12>13:04-20:00</E_TEMPORARY_WORKING_HOURS12>
                <E_TEMPORARY_DAY_WORKING_HOURS12>6</E_TEMPORARY_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="5" order="5">
                <E_TEMPORARY_DAY_WORKING_HOURS12>5</E_TEMPORARY_DAY_WORKING_HOURS12>
                <E_TEMPORARY_WORKING_HOURS12>13:03-20:00</E_TEMPORARY_WORKING_HOURS12>
            </RECORD>
        </E_TEMPORARY_CASHDESK1>
        <E_CASHDESK_TEMPORARY_END_DATE day="14" month="12" viewmode="-1" year="2024">14/12/2024</E_CASHDESK_TEMPORARY_END_DATE>
        <E_SAFE_BOXES fix_header="1" height="" viewmode="1"/>
        <E_TEMPORARY_BUSINESS fix_header="1" height="" viewmode="-1">
            <RECORD id="2" order="2">
                <E_TEMPORARY_DAY_WORKING_HOURS3>1</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="3" order="3">
                <E_TEMPORARY_DAY_WORKING_HOURS3>3</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="1" order="1">
                <E_TEMPORARY_DAY_WORKING_HOURS3>2</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="5" order="5">
                <E_TEMPORARY_DAY_WORKING_HOURS3>5</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="4" order="4">
                <E_TEMPORARY_DAY_WORKING_HOURS3>4</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="6" order="6">
                <E_TEMPORARY_DAY_WORKING_HOURS3>6</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
            <RECORD id="7" order="7">
                <E_TEMPORARY_DAY_WORKING_HOURS3>7</E_TEMPORARY_DAY_WORKING_HOURS3>
                <E_TEMPORARY_WORKING_HOURS3>14:06-20:00</E_TEMPORARY_WORKING_HOURS3>
            </RECORD>
        </E_TEMPORARY_BUSINESS>
        <RESTRICT>
            <BUTTON>
                <NAME>Email</NAME>
            </BUTTON>
            <BUTTON>
                <NAME>Link</NAME>
            </BUTTON>
            <BUTTON>
                <NAME>Bookmark</NAME>
            </BUTTON>
            <BUTTON>
                <NAME>Print</NAME>
            </BUTTON>
            <BUTTON>
                <NAME>SMS</NAME>
            </BUTTON>
            <BUTTON>
                <NAME>Feedback</NAME>
            </BUTTON>
        </RESTRICT>
        <E_TEMPORARY_SAFE_BOXES fix_header="1" height="" viewmode="1"/>
        <E_BRANCH_SEGMENT selectdisplaymode="list" viewmode="-1">
            <VALUE>5</VALUE>
            <VALUE>6</VALUE>
            <VALUE>4</VALUE>
        </E_BRANCH_SEGMENT>
        <E_AUTOLOAN_SCHEDULE fix_header="1" height="" viewmode="1"/>
        <E_MORTGAGE_DEPARTMENT_1 field_caption="" fix_header="1" height="" viewcaption="on" viewcaptionhidden="yes" viewmode="-1"/>
        <E_CASHDESK1 fix_header="1" height="" viewmode="1">
            <RECORD id="4" order="4">
                <E_DAY_WORKING_HOURS12>4</E_DAY_WORKING_HOURS12>
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
            </RECORD>
            <RECORD id="3" order="3">
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
                <E_DAY_WORKING_HOURS12>3</E_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="1" order="1">
                <E_DAY_WORKING_HOURS12>2</E_DAY_WORKING_HOURS12>
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
            </RECORD>
            <RECORD id="5" order="5">
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
                <E_DAY_WORKING_HOURS12>5</E_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="6" order="6">
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
                <E_DAY_WORKING_HOURS12>6</E_DAY_WORKING_HOURS12>
            </RECORD>
            <RECORD id="2" order="2">
                <E_DAY_WORKING_HOURS12>1</E_DAY_WORKING_HOURS12>
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
            </RECORD>
            <RECORD id="7" order="7">
                <E_DAY_WORKING_HOURS12>7</E_DAY_WORKING_HOURS12>
                <E_WORKING_HOURS12>10:00-20:00</E_WORKING_HOURS12>
            </RECORD>
        </E_CASHDESK1>
        <E_DATABASE_TP>
            <URL/>
            <CAPTION/>
        </E_DATABASE_TP>
        <E_TEMPORARY_PFM_PRIME fix_header="1" height="" viewmode="1"/>
        <COLLABORATION item="true"/>
        <E_HOLIDAYS_COMMENT viewmode="-1"/>
        <E_TEMPORARY_SALARY fix_header="1" height="" viewmode="1"/>
        <E_TEMPORARY_COMMENT viewmode="-1"/>
        <E_COMMENT_STATUS viewmode="-1"/>
        <E_EFF_SEARCH viewmode="-1"/>
        <E_SALARY fix_header="1" height="" viewmode="1"/>
        <E_HOLIDAYS_INDIVIDUAL fix_header="1" height="" viewmode="-1">
            <RECORD id="1" order="1">
                <E_HOLIDAYS_WORKING_HOURS1>выходной</E_HOLIDAYS_WORKING_HOURS1>
                <E_HOLIDAYS_DATE1>24.09.2024</E_HOLIDAYS_DATE1>
            </RECORD>
        </E_HOLIDAYS_INDIVIDUAL>
        <E_COORDINATES>59.1234500, 57.1234500</E_COORDINATES>
        <E_TEMPORARY_CASHDESK_CONT viewmode="0"/>
        <E_HOLIDAYS_CASHBOX fix_header="1" height="" viewmode="1">
            <RECORD id="1" order="1">
                <E_HOLIDAYS_WORKING_HOURS>10:00-19:00</E_HОЛIDAYS_WORKING_HOURS>
                <E_HОЛIDAYS_DATE>24.09.2024</E_HОЛIDAYS_DATE>
            </RECORD>
        </E_HOLIDAYS_CASHBOX>
        <E_BRANCH_SERVICES selectdisplaymode="list" viewmode="-1">
            <VALUE>19</VALUE>
            <VALUE>3</VALUE>
        </E_BRANCH_SERVICES>
        <E_AUTOLOAN field_caption="" fix_header="1" height="" viewcaption="on" viewcaptionhidden="yes" viewmode="-1"/>
        <E_TEMPORARY_PERSINAL_MANAGER fix_header="1" height="" viewmode="1"/>
        <E_CONTACTS fix_header="1" height="" viewmode="-1"/>
        <E_DATABASE_SIS_DKO viewmode="-1">
            <CAPTION/>
            <URL/>
        </E_DATABASE_SIS_DKO>
        <E_STATUS_3 viewmode="-1"/>
        <E_COMMENT height="" viewmode="-1"/>
        <E_CASHDESK_TEMPORARY_START_DATE day="09" month="12" viewmode="-1" year="2024">09/12/2024</E_CASHDESK_TEMPORARY_START_DATE>
        <E_TEMPORARY_WORKING_HOURS1 viewmode="-1"/>
        <E_CHECK_SCHEDULE viewmode="-1"/>
        <E_MORTGAGE_TOPIC1 viewmode="-1"/>
        <E_WARNINGS_1 viewmode="-1"/>
        <E_TEMPORARY_CASHDESK_COMMENT viewmode="-1"/>
        <E_AUTOLOAN_TOPIC viewmode="-1"/>
        <E_TEMPORARY_CHECK_SCHEDULE viewmode="-1"/>
        <SMS_DESCRIPTION viewmode="-1">Астрахань, ул. Яблочковe, д. 51 лит.
    ФЛ: Пн-Ср: 13:01-18:00, Чт: 13:02-18:00, Пт: 13:03-18:00
    ЮЛ: Пн: 09:00-19:00, Вт: 10:30-19:30, Ср-Пт: 10:00-19:00
    Касса: Пн-Вс: 10:00-20:00</SMS_DESCRIPTION>
        <E_STATUS viewmode="-1">2</E_STATUS>
        <ITEM_IMAGE new_window="on" subtitles=""/>
        <E_EDITOR_FIELD_2 viewmode="-1"/>
        <E_WARNINGS_3 viewmode="-1"/>
        <E_MORTGAGE_SCHEDULE11 fix_header="1" height="" viewmode="1"/>
        <E_PFM_PRIME fix_header="1" height="" viewmode="1"/>
        <E_HOLIDAYS_SCHEDULE viewmode="0"/>
        <E_MORTGAGE_SCHEDULE14 fix_header="1" height="" viewmode="1"/>
        <E_RATING viewmode="-1"/>
        <E_COMMENTS_3 viewmode="-1"><![CDATA[<iframe src="/branch/servlet?branchId=000001&head=1&java=1" scrolling="no" frameborder="0" width="600" height="950" align="left"> </iframe>]]></E_COMMENTS_3>
        <GLOSSARY>
            <TERMS><![CDATA[[]]]></TERMS>
        </GLOSSARY>
        <E_REFERENCE_FILE/>
        <E_COMMENTS_2 viewmode="-1"/>
        <E_MOR_LINK viewmode="-1"/>
        <E_CONTENT_MANAGER_APPROVER/>
        <E_WORKING_HOURS1 viewmode="-1"/>
        <E_MORTGAGE_TOPIC2 viewmode="-1"/>
    </ITEM>"""
