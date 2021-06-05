import traceback
import dbcreds
import mariadb
import dbconnect

# def view_exploits():
#     conn = dbconnect.get_db_connection()
#     cursor = dbconnect.get_db_cursor(conn)
#     if(conn == None or cursor == None):
#         print("Error in databse connection")
#         return
#     try:
#         cursor.execute("SELECT alias FROM hackers")
#         print(cursor.fetchall())
#     except:
#         print("Something went wrong with view the exploits")
#         traceback.print_exc()
#     dbconnect.close_db_connection(cursor)
#     dbconnect.close_db_connection(conn)

# view_exploits()

conn = dbconnect.get_db_connection()
cursor = dbconnect.get_db_cursor(conn)

def login():
    username = input("Please enter your username: ")

    password = input("Please enter your password: ")

    cursor.execute("SELECT * FROM hackers WHERE alias=?", [username, ])
    current_hacker = cursor.fetchone()

    if(current_hacker[2] == password):
        print("you are now logged in!")
        is_logged_in = True
        return is_logged_in
    else:
        print("Wrong password")

dbconnect.close_db_connection
dbconnect.close_db_cursor