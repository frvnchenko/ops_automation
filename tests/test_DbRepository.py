from src.db.DbConnector import DbConnector
from src.db.DbRepository import DbRepository
import pytest


@pytest.mark.order(2)
def test_get_all_ops_articles(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    tmp = db_req.get_all_ops_articles(db_req.GET_ALL_OPS_ARTICLES)
    print(tmp)


@pytest.mark.order(3)
def test_get_days_value(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    tmp = db_req.get_days_value()
    print(tmp)


#@pytest.mark.skip(reason="Удаление статей временно отключено")
@pytest.mark.order(-1)
def test_delete_articles(db_connect):
    db_con = db_connect
    db_req = DbRepository(db_con)
    db_req.delete_articles()
    db_con.commit()
