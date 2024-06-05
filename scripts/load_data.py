import pandas as pd
from sqlalchemy import create_engine
import os

def load_csv_to_db(table_name):
    db_pw = os.getenv('DB_Project_PW')
    
    if not db_pw:
        raise ValueError("DB_Project_PW 환경 변수를 설정하세요.")

    # 데이터베이스 연결 URL 설정
    server = r'localhost\SQLEXPRESS'  # raw 문자열 사용
    database = 'projectDB'
    username = 'Login'
    password = db_pw

    # SQLAlchemy 엔진 생성
    database_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(database_url)


    # 인코딩 리스트
    encodings = ['euc-kr', 'cp949', 'utf-8', 'latin1']
    
    # CSV 파일 로드
    csv_file_path = 'C:\\Users\\kakao\\Desktop\\Ajou_DatabaseManagement\\data\\' + table_name + ".csv "  # 실제 CSV 파일 경로로 수정
    for encoding in encodings:
        try:
            df = pd.read_csv(csv_file_path, encoding=encoding)  # 여러 인코딩 시도
            break  # 성공하면 반복문 탈출
        except UnicodeDecodeError:
            continue  # 다음 인코딩 시도    # 데이터프레임을 SQL 테이블로 로드
    #table_name = 'Populations'  # 실제 테이블 이름으로 수정
    if 'df' not in locals():
        raise ValueError("CSV 파일의 인코딩 형식을 확인하세요. 예: 'euc-kr', 'cp949', 'utf-8'")

    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    print("CSV 파일이 데이터베이스로 성공적으로 로드되었습니다.")

if __name__ == "__main__":
    print(os.listdir('C:\\Users\\kakao\\Desktop\\Ajou_DatabaseManagement\\data'))
    selected_table = str(input())
    load_csv_to_db(selected_table)
