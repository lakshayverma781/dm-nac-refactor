import sqlalchemy
from databases import Database
from dm_nac_service.data.logs_model import applogs
from dm_nac_service.commons import get_env_or_fail


DATABASE_SERVER = 'database-server'

DATABASE_URL = get_env_or_fail(DATABASE_SERVER, 'database-url', DATABASE_SERVER + 'database-url not configured')
database = Database(DATABASE_URL)
sqlalchemy_engine = sqlalchemy.create_engine(DATABASE_URL)


def get_database() -> Database:
    return database


async def insert_logs(url, app_type, request_json, status_code, content, created):
    Database = get_database()
    log_info = {'request': url,
                'request_type': 'POST',
                'app_type': app_type,
                'request_json': request_json,
                'response_status': status_code,
                'response_content': content,
                'created_date': created}
    insert_query = applogs.insert().values(log_info)
    log_id = await Database.execute(insert_query)
    return log_id


async def insert_logs_all(url, request_type, app_type, request_json, status_code, content, created):
    Database = get_database()
    log_info = {'request': url,
                'request_type': request_type,
                'app_type': app_type,
                'request_json': request_json,
                'response_status': status_code,
                'response_content': content,
                'created_date': created}
    insert_query = applogs.insert().values(log_info)
    log_id = await Database.execute(insert_query)
    return log_id
