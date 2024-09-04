from mysql.connector import (Error, errorcode)
import mysql.connector
from todo.utils import dev_config

connection_config = dev_config.connection_config
cnx = None

def connect():
    global cnx
    try:
        print("Connecting to SQL")
        cnx = mysql.connector.connect(
            user=connection_config['user'],
            password=connection_config['password'],
            host=connection_config['host'],
            database=connection_config['database']
            )
        
        print("Connection successful!")
        return cnx
    
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


  
def create_table():
    cnx.connect()
    cursor_ = cnx.cursor()
    create_user_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL
    )
    """
    create_todo_table_query = """
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        description VARCHAR(50) NOT NULL,
        complete BOOLEAN NOT NULL,
        incomplete BOOLEAN NOT NULL,
        time_completed DATETIME,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    cursor_.execute(create_user_table_query)
    cursor_.execute(create_todo_table_query)
    cnx.commit()
    
    print("Table(s) created successfully")
 
def populate_user_table(first_name, last_name):
    cnx.connect()
    cursor_ = cnx.cursor()
    new_user_query = """
       INSERT INTO users
        (first_name, last_name) VALUES
        (%s, %s);
       """
       
    values = first_name, last_name
    
    cursor_.execute(new_user_query, values)
    cnx.commit()
    print("Data successfully added..")

def populate_todo_table(description, complete, incomplete, time_completed, user_id):
    cnx.connect()
    cursor_ = cnx.cursor()
    new_user_query = """
       INSERT INTO todos
        (description, complete, incomplete, time_completed, user_id) VALUES
        (%s, %s, %s, %s, %s);
       """
       
    values = description, complete, incomplete, time_completed, user_id
    
    cursor_.execute(new_user_query, values)
    cnx.commit()
    print("Data successfully added..")

def update_todo_table(id, description, complete, incomplete, time_completed, user_id):
    cnx.connect()
    cursor_ = cnx.cursor()
    updated_todo_query = """
       UPDATE todos 
       SET 
            description = CASE WHEN %s IS NOT NULL THEN %s ELSE description END, 
            complete = CASE WHEN %s IS NOT NULL THEN %s ELSE complete END, 
            incomplete = CASE WHEN %s IS NOT NULL THEN %s ELSE incomplete END, 
            time_completed = CASE WHEN %s IS NOT NULL THEN %s ELSE time_completed END, 
            user_id = CASE WHEN %s IS NOT NULL THEN %s ELSE user_id END
            
       WHERE id = %s
       """

    values = (
            description, description, 
            complete, complete, 
            incomplete, incomplete, 
            time_completed, time_completed, 
            user_id, user_id,
            id
    )
    
    cursor_.execute(updated_todo_query, values)
    cnx.commit()
    print("Data successfully updated..")
    
    
def delete_todo_table(id):
    cnx.connect()
    cursor_ = cnx.cursor()
    updated_todo_query = """
       DELETE FROM todos
       WHERE id = %s
       """
    
    cursor_.execute(updated_todo_query, (id, ))
    cnx.commit()
    print("Data successfully deleted..")
    
def check_user_exist(first_name, last_name):
    try:
        print("check")
        cnx.connect()
        cursor_ = cnx.cursor()

        find_user_query = """
            SELECT users.first_name, users.last_name, users.id
            FROM users WHERE first_name = %s
            AND last_name = %s
        """
        values = first_name, last_name
        
        cursor_.execute(find_user_query, values)
        result = cursor_.fetchone()
        
        cnx.commit()
        if result:
            print(f'User successfully found: {result}')
            return {'status': 'success', 'result': result}
        else:
            print('No user found with the given name.')
            return result
        
    except Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
            
    
def get_all_todos(userId):
    try:
        print(userId)
        cnx.connect()
        cursor_ = cnx.cursor()

        get_all_user_todos = """
            SELECT * FROM todos WHERE user_id = %s
        """
        
        cursor_.execute(get_all_user_todos, (userId,))
        result = cursor_.fetchall()
        
        cnx.commit()
        if result:
            print(f'User todos successfully found: {result}')
            return {'status': 'success', 'result': result}
        else:
            print('No user todos found with the given name.')
            return result
        
    except Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        
def get_one_todo(id, userId):
    try:
        print(userId)
        cnx.connect()
        cursor_ = cnx.cursor()

        get_all_user_todos = """
            SELECT * FROM todos WHERE user_id = %s AND id = %s
        """
        
        values = id, userId
        
        cursor_.execute(get_all_user_todos, values)
        result = cursor_.fetchone()
        
        todoId = result[5]
        todoUserId = result[0]
        
        cnx.commit()
        if result:
            print(f'Todo: {userId}, {todoUserId}')
            print(f'User todo successfully found: {result}')
            return {'status': 'success', 'result': {
                'todoUserId': {todoUserId},
                'todoId': {todoId}
                }}
        else:
            print('No user todo found with the given name.')
            return result
        
    except Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    
def main():
    connect()

if __name__ == "__main__":
    main()