import pyodbc
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    server = 'projectdb.c5gsiqqsu08i.ap-northeast-2.rds.amazonaws.com'  # raw 문자열 사용
    database = 'projectdb'
    username = 'Login'
    password = 'Yuyu6888!!'
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          f'SERVER={server};'
                          f'DATABASE={database};'
                          f'UID={username};'
                          f'PWD={password};')
    return cnxn

@app.get("/")
async def root(request: Request):    
    message = "Nice 2 meet U"
    body = "Ajou Univ Engineering Database Management"
    return templates.TemplateResponse("index.html", {"request": request, "message1": message, "message2": body})


@app.get("/data")
async def get_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Populations")
        data = cursor.fetchall()

        # 커서를 닫기 전에 description 가져오기
        columns = [column[0] for column in cursor.description]

        cursor.close()
        conn.close()

        # 데이터를 JSON 형식으로 변환
        result = [dict(zip(columns, row)) for row in data]

        return JSONResponse(content={"data": result})

    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/data/{index}")
async def get_data_by_index(index: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Populations")
        data = cursor.fetchall()

        # 커서를 닫기 전에 description 가져오기
        columns = [column[0] for column in cursor.description]

        cursor.close()
        conn.close()

        # 인덱스 범위 확인
        if index < 0 or index >= len(data):
            raise HTTPException(status_code=404, detail="Index out of range")

        # 특정 인덱스의 데이터를 JSON 형식으로 변환
        result = dict(zip(columns, data[index]))

        return JSONResponse(content={"data": result})

    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
