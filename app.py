import traceback
import dbcreds
import mariadb
import dbconnect

# set values to none/false
conn = None
cursor = None
logged_in = False

# Try to connect to the database, show the proper exceptions.
# Call the functions from the imported dbconnect file
try:
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
except mariadb.OperationalError: 
    print("there seems to be a connection issue")
except:
    print("there is an unexpected error")
    

# Try to logim

try:
    # Enter the username and then the password. 
    # An sql statement and a conditonal block will check If there is a user with the same name, and the password is entered correctly, 
    # the  is logged in value will be true, otherwise, the corresponding error message will appear
    username = input("Please enter your username: ")

    password = input("Please enter your password: ")

    cursor.execute("SELECT * FROM hackers WHERE alias=?", [username, ])
    current_hacker = cursor.fetchone()
    if(current_hacker[2] == password):
        print("")
        print("you are now logged in!")
        logged_in = True
    else:
        print("")
        print("Wrong password")
except mariadb.IntegrityError:
    print("There was an integrity error, the post was not posted")
except mariadb.DataError:
    print("There was a data error")
    traceback.print_exc()
except mariadb.InternalError:
    print("there was an internal error ")
    traceback.print_exc()
except mariadb.DatabaseError:
    print("there was a database error ")
    traceback.print_exc()
except mariadb.OperationalError:
    print("There was an operational error")
    traceback.print_exc()
except:
    print("There is no account with that username")
    

# this function will add a post into the database

def insert_exploit():
    try:
        exploit_content = input("Enter your post: ")
        cursor.execute(f"INSERT INTO exploits(user_id, content) VALUES('{current_hacker[0]}', '{exploit_content}')")
        conn.commit()
    except mariadb.IntegrityError:
        print("There was an integrity error, the post was not posted")
    except mariadb.DataError:
        print("There was a data error")
        traceback.print_exc()
    except mariadb.InternalError:
        print("there was an internal error ")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("there was a database error ")
        traceback.print_exc()
    except mariadb.OperationalError:
        print("There was an operational error")
        traceback.print_exc()
    except: 
        print("there was an unexpected error")


# this function will show the logged in users posts by calling an sql that is based on the current users ID
def view_user_exploits():
    try:
        cursor.execute("SELECT * FROM exploits WHERE user_id=?", [current_hacker[0], ])
        return cursor.fetchall()
    except mariadb.IntegrityError:
        print("There was an integrity error")
        traceback.print_exc()
    except mariadb.InternalError:
        print("there was an internal error ")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("there was a database error ")
        traceback.print_exc()
    except mariadb.OperationalError:
        print("There was an operational error")
        traceback.print_exc()
    except: 
        print("there was an unexpected error")


# this function will call an inner join sql to fetch the username and the content of the posts of everyone 
# except the current hacker
def view_exploits():
    try:
        cursor.execute("SELECT alias, content FROM exploits e INNER JOIN hackers h ON e.user_id = h.id WHERE NOT user_id = ?;", [current_hacker[0], ])
        return cursor.fetchall()
    except mariadb.IntegrityError:
        print("There was an integrity error")
        traceback.print_exc()
    except mariadb.InternalError:
        print("there was an internal error ")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("there was a database error ")
        traceback.print_exc()
    except mariadb.OperationalError:
        print("There was an operational error")
        traceback.print_exc()
    except: 
        print("there was an unexpected error")


# the user will input an option, and the corresponding messages and funcitons will run
while(logged_in == True):
    # loop through this while logged in
    print("")
    print("Make a selection")
    print("    1. Make a new exploit")
    print("    2. See your own exploits")
    print("    3. See others exploits")
    print("    4. Exit the application")

    user_choice = input("Enter: ");

    if(user_choice == "1"):
        print("")
        insert_exploit()
        print("")
    elif(user_choice == "2"):
        print("")
        print(f"{current_hacker[1]}'s posts: ")
        print("")
        posts = view_user_exploits()
        # loop through posts so that it looks nice
        for post in posts:
            print(f"    {post[1]}")
            print(f"      -{current_hacker[1]}")
            print("")
    elif(user_choice == "3"):
        print("")
        print("Exploits: ")
        print("")
        posts = view_exploits()
        # loop through posts so that it looks nice
        for post in posts:
            print(f"    {post[1]}")
            print(f"      -{post[0]}")
            print("")
    elif(user_choice == "4"):
        print("")
        print("Exiting application....")
        print("")
        # break the while loop to exit
        break
    else:
        print("")
        print("Please choose a correct key")
    

dbconnect.close_db_cursor
dbconnect.close_db_connection


