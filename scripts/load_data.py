import pandas as pd
from sqlalchemy import create_engine

def load_csv_to_db():
    # 데이터베이스 연결 URL 설정
    server = 'projectdb.c5gsiqqsu08i.ap-northeast-2.rds.amazonaws.com'  # raw 문자열 사용
    database = 'projectdb'
    username = 'Login'
    password = 'Yuyu6888!!'

    # SQLAlchemy 엔진 생성
    database_url = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(database_url)

    # CSV 파일 로드
    csv_file_path = '../data/연령인구시도.csv'  # 실제 CSV 파일 경로로 수정
    try:
        df = pd.read_csv(csv_file_path, encoding='euc-kr')  # 한글 인코딩을 지정
    except UnicodeDecodeError:
        raise ValueError("CSV 파일의 인코딩 형식을 확인하세요. 예: 'euc-kr', 'cp949', 'utf-8'")
    # 데이터프레임을 SQL 테이블로 로드
    table_name = 'Populations'  # 실제 테이블 이름으로 수정
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

    print("CSV 파일이 데이터베이스로 성공적으로 로드되었습니다.")

if __name__ == "__main__":
    load_csv_to_db()
