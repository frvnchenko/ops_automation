
from src.db.DbRepository import DbRepository
from src.db.JsonFileLoader import JsonFileLoader, jsons_update,target_dir_update
import pytest


#@pytest.mark.skip(reason="Загрузка json create файлов временно отключена")
@pytest.mark.order(1)
def test_upload_json_create(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    loader = JsonFileLoader()
    json_data_list = loader.load_json_files()[0]

    for json_string in json_data_list:
        db_req.insert_json(json_string)
    db_con.commit()

@pytest.mark.skip(reason="Загрузка json update файлов временно отключена")
@pytest.mark.order(2)
def test_upload_json_update(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    loader = JsonFileLoader(target_dir_update,jsons_update)
    json_data_list = loader.load_json_files()[0]

    for json_string in json_data_list:
        db_req.insert_json(json_string)
    db_con.commit()