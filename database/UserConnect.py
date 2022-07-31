import sqlalchemy
import pandas as pd
import pymysql
import pyupbit

# def with_cursor(original_func):
#     def wrapper(*arg, **kwargs):
#         # db에 연결(json 출력이 편함)
#         db = pymysql.connect(host='
#         rv = original_func(Cursor, *args, **kwargs)
#         db.commit()
#         db.close()
#         return rv
#     return wrapper
#     #     rv = original_func(Cursor, *args, **kwargs)
#     #     db.commit()
#     #     db.close()
#     #     return rv
#     # return wrapper

# def with_tosql(origin_func):
#     def wrapper(*args, **kwargs):
#         db_connection_str = 'mysql+pymysql
#         db_connection = sqlalchemy.create_engine(db_connection_str)
#         conn = db_connection.connect()
#         # to_sql하기위한db 연결 설정
#         rv = origin_func(db_connection, *args, **kwargs)
#         conn.close()
#         return rv
#     return wrapper



def DB_Init(Cursor):

    sql = """CREATE TABLE IF NOT EXISTS `data` (
      `dateCoin` datetime DEFAULT NULL,
      `idCoin` text COLLATE utf8mb3_unicode_ci DEFAULT NULL,
      `open` double DEFAULT NULL,
      `high` double DEFAULT NULL,
      `low` double DEFAULT NULL,
      `close` double DEFAULT NULL,
      `volume` double DEFAULT NULL,
      `value` double DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;"""

    # query 실행
    Cursor.execute(sql)

    #################################################################################


def get_all_list(Cursor):
    Cursor.execute("select * from data")
    # 결과 출력

    return Cursor.fetchall()
    #conn.close()
    #print(result)
    # 결과 확인
    

def Inseart_data_upbit(conn, coin_select, date_select):
	#################################################################################
    df = pyupbit.get_ohlcv(coin_select, interval=date_select, count=500)
    #print(type(df))
    df['idCoin'] = coin_select    # 마켓 정보 추가

    market_date = df.index
    df['dateCoin'] = market_date    # 날짜 정보 추가
    # 열 이름은 테이블의 이름과 같아야한다.

    df = df[['dateCoin','idCoin', 'open', 'high', 'low', 'close', 'volume', 'value']]     # 데이터 순서 변경
    #print(df)

    # 추가할 때 데이터 옵션 변경 가능
    # dtypesql = {'dateCoin':sqlalchemy.DateTime(),
    #     'idCoin':sqlalchemy.types.VARCHAR(30), 
    #     'open':sqlalchemy.types.VARCHAR(30),
    #     'high':sqlalchemy.types.VARCHAR(30),
    #     'low':sqlalchemy.types.VARCHAR(30),
    #     'close':sqlalchemy.types.VARCHAR(30), 
    #     'volume':sqlalchemy.types.VARCHAR(30),
    #     'value':sqlalchemy.types.VARCHAR(30) 
    # }

    df.to_sql(name='data', con=conn, if_exists='replace',index=False)

    print('insert success')
    ###############################################################################