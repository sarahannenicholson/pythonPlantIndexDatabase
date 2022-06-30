import pymysql

con = pymysql.connect(host='plant-index-database.cyaimo2g0lsu.us-east-2.rds.amazonaws.com', user='admin',
                     password='admin123', charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

try:

    with con.cursor() as cur:
        # selects specific database
        cur.execute('use plant_database')
        # selects database specific table
        cur.execute('SELECT * FROM plant_information')
        # fetches
        rows = cur.fetchall()

        # prints
        for row in rows:
            print(row['plant_id'], row['plant_name'])

# closes connection to db
finally:
    con.close()