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
from dust_api import get_dust_forecast
from pydantic import BaseModel


db_pw = os.getenv('DB_Project_PW')
app = FastAPI()

# 절대 경로를 직접 지정합니다.
static_dir = "C:\\Users\\kakao\\Desktop\\Ajou_DatabaseManagement\\static"

app.mount("/static", StaticFiles(directory=static_dir), name="static")

def get_db_connection():
    server = r'localhost\SQLEXPRESS'  # 예: 'localhost\SQLEXPRESS'
    database = 'projectDB'
    username = 'Login'
    password = db_pw
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
    )
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
            "GWD": "강원%",
            "GGD": "경기도",
            "GSD": "경상남도",
            "GSB": "경상북도",
            "GJW": "광주광역시",
            "TGU": "대구광역시",
            "DJN": "대전광역시",
            "PUS": "부산광역시",
            "SEL": "서울특별시",
            "SJS": "세종%",
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
                SELECT [시도별], [2024] 
                FROM Populations 
                WHERE [시도별] LIKE ? AND [인구종류별(1)] LIKE '고령인구(천명): 65세+'
            """
            params = (f"%{region}%",)  # 지역을 포함하는 패턴
        elif table_name == "Careservices":
            execute_query = """
                SELECT [시도], [시군구], [기관명], [주소], [시설유형구분], [추천]
                FROM Care_Services
                WHERE [시도] LIKE ? OR [시군구] LIKE ?
            """
            params = (f"%{region}%", f"%{region}%")
        elif table_name == "Senior_Employment":
            execute_query = """
                SELECT [사업유형], [사업명], [관할시군구], [목표일자리수], [사업번호]
                FROM Senior_Employment
                WHERE [관할시도명] LIKE ? AND [계속사업여부] LIKE 'Y'
            """
            params = (f"%{region}%",)  # 지역을 포함하는 패턴
        elif table_name == "Regional_Health_Institutions_Status":
            execute_query = """
                SELECT [보건기관명], [대표 전화번호], [기관유형], [주소], [운영시간]
                FROM Regional_Health_Institutions_Status
                WHERE [시도] LIKE ?
            """
            params = (f"%{region}%",)  # 지역을 포함하는 패턴
        else:
            raise HTTPException(status_code=400, detail="Invalid table name")

        cursor.execute(execute_query, params)
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

@app.get("/api/dust_forecast", response_class=JSONResponse)
async def api_dust_forecast():
    data = get_dust_forecast()
    return JSONResponse(content=data)

# New route for updating operation time
class OperationTimeUpdate(BaseModel):
    address: str
    operation_time: str

@app.post("/update_operation_time", response_class=JSONResponse)
async def update_operation_time(update: OperationTimeUpdate):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Regional_Health_Institutions_Status
            SET 운영시간 = ?
            WHERE 주소 = ?
            """,
            (update.operation_time, update.address)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Address not found")
        return JSONResponse(content={"message": "Operation time updated successfully"})
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Update failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        conn.close()


class Recommendation(BaseModel):
    institution_name: str

@app.post("/recommend", response_class=JSONResponse)
async def recommend_service(recommendation: Recommendation):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE Care_Services
            SET 추천 = ISNULL(추천, 0) + 1
            WHERE 기관명 = ?
            """,
            (recommendation.institution_name,)
        )
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Institution not found")
        return JSONResponse(content={"message": "Recommendation added successfully"})
    except pyodbc.Error as e:
        print(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Recommendation failed: {str(e)}")
    except Exception as e:
        print(f"General error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        conn.close()
# class User(BaseModel):
#     user_name: str
#     region: str
#     feature: str

# @app.post("/register_user", response_class=JSONResponse)
# async def register_user(user: User):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = """
#             INSERT INTO UsersTable (User, Region, Function)
#             VALUES (?, ?, ?)
#             """
#         params = (user.user_name, user.region, user.feature)
#         print("Executing query:", query)
#         print("With parameters:", params)
        
#         cursor.execute(query, params)
#         conn.commit()

#         return JSONResponse(content={"message": "User registered successfully"})
#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#     finally:
#         conn.close()

# @app.get("/users", response_class=JSONResponse)
# async def get_users():
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT User FROM UsersTable")
#         users = cursor.fetchall()
#         user_names = [user[0] for user in users]
#         return JSONResponse(content=user_names)
#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# @app.get("/users/{user_name}", response_class=JSONResponse)
# async def get_user(user_name: str):
#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute(
#             "SELECT Region, Function FROM UsersTable WHERE User = ?", (user_name,)
#         )
#         user = cursor.fetchone()
#         if user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return JSONResponse(content={"region": user[0], "feature": user[1]})
#     except pyodbc.Error as e:
#         raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
#     finally:
#         conn.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
