import psycopg2

class DB():
    def __init__(self):
        conn = psycopg2.connect(dbname='database', user='admin', password='mps', host='localhost')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE CALLS  
             (DATE TEXT NOT NULL
             ID INT PRIMARY KEY NOT NULL,
             RESULT_STAGE2 INT NOT NULL,
             TEL_NUMBER TEXT NOT NULL,
             DURATION INT NOT NULL,
             INFORMATION TEXT NOT NULL);''')

    def insert(cursor, date, id, result2, tel_number, duration, information):
        cursor.execute("INSERT INTO CALLS (DATE,ID,RESULT_STAGE2,TEL_NUMBER,DURATION,INFORMATION) \
            VALUES (date, id, result2, tel_number, duration, information)");