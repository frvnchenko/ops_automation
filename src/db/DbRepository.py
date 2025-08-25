from src.db.DbConnector import DbConnector


class DbRepository:
    # простые запросы
    DELETE_ARTICLES = """
        do $$
        declare
            rec record;
        begin

        for rec in SELECT DISTINCT tt.itm_id 
        FROM item_type_tab tt
        WHERE tt.itm_type = 'DOCUMENT'
        AND tt.itm_sub_type = 'T_TEST_TEMPLATE_OPS_TP'

        loop
            delete from item_type_tab where itm_id = rec.itm_id;
            delete from item_status_tab where sts_item_id = rec.itm_id;
            delete from item_version_tab vt where vt.vrs_item_id = rec.itm_id;
            delete from item_to_group_tab itg where itg.itg_item_id = rec.itm_id;
            delete from item_link_tab lt where lt.lnk_source_id = rec.itm_id;
        end loop;
        end;
        $$;
        delete from DIS_OPS_TP_BLOCKED_ITEM;
        delete from DIS_OPS_TP_CHANGED_ITEM;
        delete from DIS_OPS_TP_MESSAGE;
        delete from dis_branch_temporary_schedule_tab_new;
        delete from dis_branch_successor_tab_new;
        delete from dis_branch_services_tab_new;
        delete from dis_branch_segment_tab_new;
        delete from dis_branch_schedule_tab_new;
        delete from dis_branch_mortgage_tab_new;
        delete from dis_branch_index_tab_new;
        delete from dis_branch_autoloan_tab_new;
        ----delete from dis_branch_cashdesk_tab_new;
        delete from dis_branch_contacts_tab_new;
        delete from dis_branch_features_tab_new;
        delete from dis_branch_contacts_tab_new;
        delete from dis_branch_tab_new;
        """
    GET_ALL_OPS_ARTICLES = """select itm_id from item_type_tab where itm_sub_type = 'T_TEST_TEMPLATE_OPS_TP' and itm_type = 'DOCUMENT'"""

    def __init__(self, db_connection: DbConnector):
        self._db_connection = db_connection
        print("INITIAL COMPLETE", self._db_connection)

    # get_all_ops_articles
    def get_all_ops_articles(self, query):
        cursor = self._db_connection.get_cursor()
        cursor.execute(query)
        tmp = [i[0] for i in cursor.fetchall()]
        cursor.close()
        return tmp

    def delete_articles(self):
        cursor = self._db_connection.get_cursor()
        cursor.execute(self.DELETE_ARTICLES)
        cursor.close()
        print("DELETE_ARTICLES COMPLETE")

    # все отделения опс и тп выгружаются в бд
    def insert_json(self, json_string):
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            "INSERT INTO dis_ops_tp_message (message_date, message, status) VALUES (now(), %s, %s)",
            (json_string, "NEW"),  # Передаем параметры как кортеж
        )  # Передаю параметры как кортеж
        cursor.close()

    # получение id статьи по коду тп
    def get_article_id_by_code_tp(self, code_tp):
        xpath_exp = f'//E_BRANCH_ID[text()="{code_tp}"]'
        # print(xpath_exp)
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            """
            select itm_id from (
                select itm_id,  xpath_exists(%s, ivt.vrs_doc::xml) AS code_tp
                from item_type_tab itb
                left join item_version_tab ivt
                on itb.itm_id = ivt.vrs_item_id 
                where itb.itm_sub_type = 'T_TEST_TEMPLATE_OPS_TP' and itm_type = 'DOCUMENT' 
            ) as z_q
            where code_tp = true;
            """,
            (xpath_exp,),
        )
        try:
            article_id = cursor.fetchone()[0]
        except TypeError:
            article_id = None
        cursor.close()
        return article_id

    def get_active_ver(self, article_id):
        print("ACTIVE_VERSION")
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            """SELECT vrs_doc FROM item_version_tab
                    WHERE vrs_activation_date = (
                    SELECT MAX(vrs_activation_date) FROM item_version_tab ivt
                    WHERE vrs_item_id = %s and vrs_activation_date <= CURRENT_TIMESTAMP
            ) and vrs_item_id = %s""",
            (
                article_id,
                article_id,
            ),
        )
        article_active_xml = cursor.fetchone()[0]
        cursor.close()
        return article_active_xml

    def get_previous_active_ver(self, article_id):
        article_prev_xml = ""
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            """select COUNT(vrs_number) from item_version_tab where vrs_item_id = %s""",
            (article_id,),
        )
        count_versions = cursor.fetchone()[0]

        if count_versions > 1:
            cursor.execute(
                """SELECT vrs_doc FROM item_version_tab
                    WHERE vrs_activation_to = (
                    SELECT MAX(vrs_activation_to) FROM item_version_tab ivt
                    WHERE vrs_item_id = %s
            )""",
                (article_id,),
            )
            article_prev_xml = cursor.fetchone()[0]
        cursor.close()
        return article_prev_xml

    # поиск в бд по значению из кодовой таблицы пример Только VIP клиенты
    def get_code_value_by_tag(self, tag):
        tag = tag
        value, domain = tag[0], tag[1]
        code_value = ""
        # print(type(value))
        cursor = self._db_connection.get_cursor()
        if value != 0 and type(value) is tuple:
            cursor.execute(
                """
                select code_name from code_tab
                where code_domain = %s and code_id in %s
                """,
                (domain, value),
            )
        elif value != 0 and type(value) is int:
            cursor.execute(
                """
                select code_name from code_tab
                where code_domain = %s and code_id = %s
                """,
                (domain, value),
            )
        code_value = cursor.fetchall()
        code_value = [i[0] for i in code_value]
        cursor.close()
        return code_value

    # название статьи из бв
    def get_article_name_by_id(self, article_id):
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            """
            SELECT itm_title FROM item_type_tab WHERE itm_id = %s
            """,
            (article_id,),
        )
        article_name = cursor.fetchone()[0]
        cursor.close()
        return article_name

    def get_days_value(self):
        cursor = self._db_connection.get_cursor()
        cursor.execute(
            """
            select code_id,code_name from code_tab where code_domain = 'BRANCH_DAYS'
            """
        )
        result = cursor.fetchall()
        dict_result = dict((x, y) for x, y in result)
        cursor.close()
        return dict_result
