import mysql.connector
from mysql.connector import Error
from ScrambleRubixcube import xInitial, make_move
import numpy as np

class St:
    cube = None
    cost = 0

def get_corner_string(cube):
    string = ''
    for i in range(18):
        if i % 3 == 0 or i % 3 == 2:
            string = string + cube[i, 0] + cube[i, 2]
    return string

# Database dictionary setup
db = dict()
front = list()
goal = St()
goal.cube = np.array(xInitial)
front.append(goal)
db[get_corner_string(goal.cube)] = 0

while len(front) != 0:
    curr = front.pop(0)
    if curr.cost < 5:
        child_cost = curr.cost + 1
        for i in range(12):
            new = St()
            new.cube = np.array(curr.cube)
            new.cost = child_cost
            make_move(new.cube, i + 1, 0)
            string = get_corner_string(new.cube)
            if string not in db.keys():
                db[string] = new.cost
                front.append(new)

# Connect to MySQL and insert data
try:
    # Replace 'your_host', 'your_database', 'your_username', 'your_password' with actual values
    conn = mysql.connector.connect(
        host='localhost',
        database='rubikscubedb',
        user='root',
        password='Shreya@802'
    )

    if conn.is_connected():
        cursor = conn.cursor()
        
        # Create table if it doesn't already exist
        cursor.execute('CREATE TABLE IF NOT EXISTS CornerValue (Corners VARCHAR(50), Value INT)')
        
        # Insert data into the table
        cursor.executemany('INSERT INTO CornerValue (Corners, Value) VALUES (%s, %s)', db.items())
        
        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")

except Error as e:
    print("Error connecting to MySQL:", e)
finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
