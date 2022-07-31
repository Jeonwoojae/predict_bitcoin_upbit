from flask import Flask
from flask import request
from flask import jsonify
import sys
import sqlalchemy
import config
import pandas as pd
import pymysql

from database import UserConnect

app = Flask(__name__)

db = pymysql.connect(host='엔드포인트', user='사용자명', password='비밀번호', db='데이터베이스명', charset='utf8')
Cursor = db.cursor()

db_connection_str = 'mysql+pymysql://사용자명:비밀번호@엔드포인트:3306/데이터베이스명'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()


@app.route("/")
def hello():
    # 초기 DB 생성
    UserConnect.DB_Init(Cursor)
    return "Hello goorm!"

@app.route('/home')
def home():
    coin_select = request.args.get('coin', default = 'KRW-BTC', type = str)
    date_select = request.args.get('date', default = 'day1', type = str)
    print(coin_select, date_select)
    # route로 스트링을 받아 해당 선택 코인, 날짜에 따라
    # 변경하여 업비트에서 데이터 받아와 테이블에 저장
    # /home?coin=KRW-BTC&date=day1
    UserConnect.Inseart_data_upbit(conn, coin_select, date_select)
    
    # 결과 출력
    result = UserConnect.get_all_list(Cursor)

    #print(result)
    # 결과 확인
    res = jsonify(result)
    
    return res


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    
