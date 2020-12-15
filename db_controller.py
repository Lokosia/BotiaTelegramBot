import sqlite3

conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

option = 2

# Создание таблицы
if option == 0:
    sql = """CREATE TABLE users
                  (user_id int, nickname text, state text, location text)
               """

# Удаление юзера из таблицы
if option == 1:
    sql = "DELETE FROM users WHERE user_id = 460092246"

# Показать таблицу
if option == 2:
    sql = "SELECT * FROM users"
    
# Exevute sql command
cursor.execute(sql)

# Save result of command execution
conn.commit()

# Print what have we done
print(cursor.fetchall())
