import pyodbc
import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

db_pw = os.getenv('DB_Project_PW')
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db_connection():
    server = 'localhost\SQLEXPRESS'  # 예: 'localhost\SQLEXPRESS'
    database = 'projectDB'
    username = 'jaeseokk'
    password = db_pw
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          f'SERVER={server};'
                          f'DATABASE={database};'
                          f'UID={username};'
                          f'PWD={password};')
    return cnxn

@app.get("/")
async def root(request: Request):    
    message = "Nice 2 meet U"
    message = db_pw
    body = "Ajou Univ Engineering Database Management"
    return templates.TemplateResponse("index.html", {"request": request, "message1": message, "message2": body})


@app.get("/data")
async def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM YourTableName")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"data": data}