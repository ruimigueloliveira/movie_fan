import csv
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="mypass",
        host="10.139.0.2",   #maybe change this ip
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
#print(myresult)
cur.close()

file = open('movies.csv')

csvreader = csv.reader(file)
header = next(csvreader)
#print(header)
rows = []
count=0

cur = conn.cursor()
statement ="select count(*) from show_info;"
cur.execute(statement)
myresult = cur.fetchall()
cur.close()
if(int(myresult[0][0]))==0:  #only inserts if the table is empty
    #Para a tabela show_info
    for row in csvreader:
        rows.append(row)
        count+=1
        try:
            if(len(row)>=12):
                cur = conn.cursor()
                cur.execute("INSERT INTO show_info (id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description) VALUES (?, ?,?, ?,?, ?,?, ?,?, ?,?, ?)", (count, row[1],row[2], row[3],row[4], row[5],row[6], int(row[7]),row[8], row[9],row[10], row[11]))
                
            if(len(row)>=12):
                cur = conn.cursor()
                cur.execute("INSERT INTO show_rank (id, nranks, sumranks) VALUES (?, ?, ?)", (count,0,0))
                
        except mariadb.Error as e:
            print(f"Error: {e}")
            count-=1
    conn.commit()