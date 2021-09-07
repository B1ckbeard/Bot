import sqlite3

#database = r"C:\Users\Дмитрий\Documents\Python\Bot\ComService.db"
database = r'ComService.db'
conn = sqlite3.connect(database, check_same_thread=False)
cursor = conn.cursor()

def db_table_add(ligth: float, c_water: float, h_water: float):
	cursor.execute('INSERT INTO flat25 (light, c_water, h_water) VALUES (?, ?, ?)', (ligth, c_water, h_water))
	conn.commit()

def select():
    sel = 'SELECT light AS Свет, c_water AS х_вода, h_water AS г_вода FROM flat25 WHERE id=(SELECT MAX(id) FROM flat25)';
    cursor.execute(sel)
    rows = cursor.fetchall()
    s = (f'свет: {rows[0][0]}, х_вода: {rows[0][1]}, г_вода: {rows[0][2]}')
    return s

def priceSum():
    el_price = 5.93
    c_water_price = 24.98
    h_water_price = 169.6
    id = 'SELECT id FROM flat25'
    cursor.execute(id)
    id_rows = cursor.fetchall()
    second_last_id = str(id_rows[-2]).replace(',', '').replace('(','').replace(')','')
    sel = f'SELECT light AS Свет, c_water, h_water FROM flat25 WHERE id={second_last_id}';
    cursor.execute(sel)
    rows = cursor.fetchall()
    s = (f'свет: {rows[0][0]}, х_вода: {rows[0][1]}, г_вода: {rows[0][2]}')
    last = 'SELECT light AS Свет, c_water, h_water FROM flat25 WHERE id=(SELECT MAX(id) FROM flat25)';
    cursor.execute(last)
    rows1 = cursor.fetchall()
    s1 = (f'свет: {rows1[0][0]}, х_вода: {rows1[0][1]}, г_вода: {rows1[0][2]}')
    price = ((rows1[0][0]-rows[0][0])*el_price)+((rows1[0][1]-rows[0][1])*c_water_price)+((rows1[0][2]-rows[0][2])*h_water_price)
    price = (f'{round(price,2)} руб.')
    return price

def delete_last_record():
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        print('Подключен к БД')

        req = 'DELETE FROM flat25 WHERE id=(SELECT MAX(id) FROM flat25)';
        cursor.execute(req)
        conn.commit()
        print('Последняя запись удалена')
        cursor.close()
    except sqlite3.Error as error:
        print('Ошибка при работе с SQLite', error)
    finally:
        if conn:
            conn.close()
            print('Соединение с SQLite закрыто')
