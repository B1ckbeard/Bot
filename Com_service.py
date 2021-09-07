import sqlite3

#database = r"C:\Users\Дмитрий\Documents\Python\Bot\ComService.db"
database = r"ComService.db"
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
    sel = 'SELECT light AS Свет, c_water, h_water FROM flat25 WHERE id=(SELECT MAX(id-1) FROM flat25)';
    cursor.execute(sel)
    rows = cursor.fetchall()
    #s = (f'свет: {rows[0][0]}, х_вода: {rows[0][1]}, г_вода: {rows[0][2]}')
    last = 'SELECT light AS Свет, c_water, h_water FROM flat25 WHERE id=(SELECT MAX(id) FROM flat25)';
    cursor.execute(last)
    rows1 = cursor.fetchall()
    #s1 = (f'свет: {rows1[0][0]}, х_вода: {rows1[0][1]}, г_вода: {rows1[0][2]}')
    price = ((rows1[0][0]-rows[0][0])*el_price)+((rows1[0][1]-rows[0][1])*c_water_price)+((rows1[0][2]-rows[0][2])*h_water_price)
    price1 = (f'{round(price,2)} руб.')
    return price1

def delLast():
    req = 'DELETE FROM flat25 WHERE id=(SELECT MAX(id) FROM flat25)';
    cursor.execute(req)
    conn.commit()
    print('Последняя запись удалена')