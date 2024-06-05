# import pyodbc
# import os
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import JSONResponse
# from urllib.parse import unquote

# db_pw = os.getenv('DB_Project_PW')
# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# def get_db_connection():
#     server = 'localhost\SQLEXPRESS'  # 예: 'localhost\SQLEXPRESS'
#     database = 'projectDB'
#     username = 'Login'
#     password = db_pw
#     cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
#                           f'SERVER={server};'
#                           f'DATABASE={database};'
#                           f'UID={username};'
#                           f'PWD={password};')
#     return cnxn

# @app.get("/")
# async def root(request: Request):    
#     message = "Nice 2 meet U"
#     message = db_pw
#     body = "Ajou Univ Engineering Database Management"
#     return templates.TemplateResponse("index.html", {"request": request, "message1": message, "message2": body})

# # 테이블 목록을 가져오는 엔드포인트 추가
# @app.get("/tables")
# async def get_tables():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
#         tables = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         table_names = [table[0] for table in tables]

#         return JSONResponse(content={"tables": table_names})

#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# # 인구 table 가져오기
# @app.get("/data/Populations")
# async def get_data():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         execute_query = "SELECT * FROM Populations"
#         # cursor.execute("SELECT * FROM Populations")
#         cursor.execute(execute_query)
#         data = cursor.fetchall()

#         # 커서를 닫기 전에 description 가져오기
#         columns = [column[0] for column in cursor.description]

#         cursor.close()
#         conn.close()

#         # 데이터를 JSON 형식으로 변환
#         result = [dict(zip(columns, row)) for row in data]

#         return JSONResponse(content={"data": result})

#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# # region
# regions_dict = {
#     "GWD": "강원도",
#     "GGD": "경기도",
#     "GSD": "경상남도",
#     "GSB": "경상북도",
#     "GJW": "광주광역시",
#     "TGU": "대구광역시",
#     "DJN": "대전광역시",
#     "PUS": "부산광역시",
#     "SEL": "서울특별시",
#     "SJS": "세종특별자치시",
#     "USN": "울산광역시",
#     "ICN": "인천광역시",
#     "KOR": "전국",
#     "JND": "전라남도",
#     "JBD": "전라북도",
#     "JJU": "제주특별자치도",
#     "CND": "충청남도",
#     "CBD": "충청북도"
# }


# @app.get("/data/Populations/{region_code}")
# async def get_data_by_region(region_code: str):
#     try:
#         # region_code가 regions_dict에 있는지 확인
#         if region_code not in regions_dict:
#             raise HTTPException(status_code=404, detail="Invalid region code")

#         region = regions_dict[region_code]  # 지역명 가져오기
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         execute_query = """
#             SELECT [시도별(1)], [2024] 
#             FROM Populations 
#             WHERE [시도별(1)] = ? AND [인구종류별(1)] LIKE '고령인구(천명): 65세+'
#         """
#         cursor.execute(execute_query, (region,))
#         data = cursor.fetchall()

#         # 커서를 닫기 전에 description 가져오기
#         columns = [column[0] for column in cursor.description]

#         cursor.close()
#         conn.close()

#         if not data:
#             raise HTTPException(status_code=404, detail="Region not found")

#         # 데이터를 JSON 형식으로 변환
#         result = [dict(zip(columns, row)) for row in data]

#         return JSONResponse(content={"data": result})

#     except pyodbc.ProgrammingError as pe:
#         # 추가적인 에러 정보를 로깅
#         raise HTTPException(status_code=500, detail=f"Programming error: {str(pe)}")
#     except pyodbc.Error as e:
#         # SQL 에러 디테일을 로깅
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e.args[1])}")
#     except Exception as e:
#         # 일반적인 예외 처리
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
# @app.get("/data/Careservices/{region_code}")
# async def get_data(region_code:str):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         region = regions_dict[region_code]  # 지역명 가져오기
#         execute_query = "SELECT * FROM Care_Services"
#         cursor.execute(execute_query)
#         data = cursor.fetchall()

#         # 커서를 닫기 전에 description 가져오기
#         columns = [column[0] for column in cursor.description]

#         cursor.close()
#         conn.close()

#         # 데이터를 JSON 형식으로 변환
#         result = [dict(zip(columns, row)) for row in data]

#         return JSONResponse(content={"data": result})

#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

import pyodbc
import os
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

db_pw = os.getenv('DB_Project_PW')
app = FastAPI()

static_dir = "../static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

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

@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join(static_dir, "index.html"), encoding='utf-8') as file:
        content = file.read()
    return HTMLResponse(content=content)

@app.post("/data", response_class=JSONResponse)
async def get_selected_data(table_name: str = Form(...), region_code: str = Form(...)):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        regions_dict = {
            "GWD": "강원도",
            "GGD": "경기도",
            "GSD": "경상남도",
            "GSB": "경상북도",
            "GJW": "광주광역시",
            "TGU": "대구광역시",
            "DJN": "대전광역시",
            "PUS": "부산광역시",
            "SEL": "서울특별시",
            "SJS": "세종특별자치시",
            "USN": "울산광역시",
            "ICN": "인천광역시",
            "KOR": "전국",
            "JND": "전라남도",
            "JBD": "전라북도",
            "JJU": "제주특별자치도",
            "CND": "충청남도",
            "CBD": "충청북도"
        }

        if region_code not in regions_dict:
            raise HTTPException(status_code=404, detail="Invalid region code")

        region = regions_dict[region_code]

        if table_name == "Populations":
            execute_query = """
                SELECT [시도별(1)], [2024] 
                FROM Populations 
                WHERE [시도별(1)] = ? AND [인구종류별(1)] LIKE '고령인구(천명): 65세+'
            """
        elif table_name == "Careservices":
            execute_query = """
                SELECT [시도], [시군구], [기관명], [주소], [시설유형구분]
                FROM Care_Services
                WHERE [시도] = ?
            """
        else:
            raise HTTPException(status_code=400, detail="Invalid table name")

        cursor.execute(execute_query, (region,))
        data = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        cursor.close()
        conn.close()

        result = [dict(zip(columns, row)) for row in data]

        return JSONResponse(content={"columns": columns, "data": result})

    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
