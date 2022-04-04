import csv
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        port=3306,
        database="movies"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
cur.execute("select * from show_info;")
myresult = cur.fetchall()
print(myresult)
cur.close()

file = open('movies.csv')

csvreader = csv.reader(file)
header = next(csvreader)
print(header)
rows = []
count=0

for row in csvreader:
    rows.append(row)
    count+=1
    try:
        if(len(row)>=12):
            cur = conn.cursor()
            #print("aqui" + row[6] + "acaba")
            cur.execute("INSERT INTO show_info (id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)", (int(row[0]), row[1],row[2], row[3],row[4], row[5],row[6], int(row[7]),row[8], row[9],row[10], row[11]))
    except mariadb.Error as e:
        print(f"Error: {e}")

conn.commit()