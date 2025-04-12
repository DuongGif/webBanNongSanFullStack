import urllib

params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=MSI\SQLEXPRESS;"           # Thay bằng tên server của bạn nếu cần
    "DATABASE=QLNongSan_Api;"      # Cơ sở dữ liệu đã tạo sẵn
    "Trusted_Connection=yes;"
)

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={params}"

class Config:
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key_here'
