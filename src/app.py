import pymysql
import pyupbit
import pandas as pd
import sqlalchemy


db_connection_str = 'mysql+pymysql://root:0000@127.0.0.1/upbit_data'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()
# db에 연결


df = pyupbit.get_ohlcv("KRW-BTC", interval='day1', count=5)
#print(type(df))
df['idCoin'] = 'KRW-BTC'    # 마켓 정보 추가

market_date = df.index
df['dateCoin'] = market_date    # 날짜 정보 추가
# 열 이름은 테이블의 이름과 같아야한다.

df = df[['dateCoin','idCoin', 'open', 'high', 'low', 'close', 'volume', 'value']]     # 데이터 순서 변경
#print(df)

# 추가할 때 데이터 옵션 변경 가능
dtypesql = {'dateCoin':sqlalchemy.DateTime(), 
          'idCoin':sqlalchemy.types.VARCHAR(30), 
          'open':sqlalchemy.types.VARCHAR(30),
          'high':sqlalchemy.types.VARCHAR(30),
          'low':sqlalchemy.types.VARCHAR(30),
          'close':sqlalchemy.types.VARCHAR(30), 
          'volume':sqlalchemy.types.VARCHAR(30),
          'value':sqlalchemy.types.VARCHAR(30) 
}

df.to_sql(name='data', con=db_connection, if_exists='replace',index=False)

print('success')

# db에 연결
db = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='upbit_data', charset='utf8')

Cursor = db.cursor()
query = "select * from data"
Cursor.execute(query)

result = Cursor.fetchall()
conn.close()
print(result)
# 결과 확인
