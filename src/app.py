from flask import Flask
from flask import request
from flask import jsonify
import sys
import sqlalchemy
import config
import pandas as pd
import pymysql
import pyupbit

app = Flask(__name__)

#db 초기 설정 부분( 다른 파일로 변경 )
#################################################################

db_connection_str = 'mysql+pymysql://사용자명:비밀번호@엔드포인트:3306/데이터베이스명'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()
# db 연결 설정

# db에 연결
db = pymysql.connect(host='엔드포인트', user='사용자명', password='비밀번호', db='데이터베이스명', charset='utf8')

# database 사용하기 위한 cursor 세팅
Cursor = db.cursor()


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







@app.route("/")
def hello():
    return "Hello goorm!"

@app.route('/home')
def home():
    coin_select = request.args.get('coin', default = 'KRW-BTC', type = str)
    date_select = request.args.get('date', default = 'day1', type = str)
    print(coin_select, date_select)
    # route로 스트링을 받아 해당 선택 코인, 날짜에 따라
    # 변경하여 업비트에서 데이터 받아와 테이블에 저장
    # /home?coin=KRW-BTC&date=day1
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

    df.to_sql(name='data', con=db_connection, if_exists='replace',index=False)

    print('insert success')
    ###############################################################################
    
    # 결과 출력
    ###############################################################################
    query = "select * from data"
    Cursor.execute(query)

    result = Cursor.fetchall()
    #conn.close()
    #print(result)
    # 결과 확인
    
    res = jsonify(result)
    
    return res


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    
