
import pymysql

# Update these if your MySQL connection uses different settings
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "94123"

try:
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )

    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS orgbot_saas")
        print("Database 'orgbot_saas' created successfully!")

    connection.close()

except Exception as error:
    print("Database creation failed:", error)