from pymysql import connections
from pymysql.cursors import DictCursor
import yaml
import requests
import pymysql
from congif import host, user, password, db_name

# response = requests.get('http://example.com/toys')

with open('toys.yaml') as file:
    toys_data = yaml.load(file, Loader=yaml.FullLoader)

toys, toys_games, toys_repair = [], [], []
for i in toys_data['toys']:
    toys.append((i['id'], i['name'], i['status'], i['status_updated']))
    for x in i['games']:
        toys_games.append((x['id'], i['id'], x['note']))
        toys_repair.append((i['id'], x['note']))


with open('games.yaml') as file:
    games_data = yaml.load(file, Loader=yaml.FullLoader)

games = []
for i in games_data['games']:
    games.append((i['id'], i['name'], i['date']))


try:
    connection = pymysql.connect(
        host = host,
        port = 3306,
        user = user,
        password = password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor    
    )
    print('Сonnect successfully')


    try:
        # TASK#1 and TASK#2
        with connection.cursor() as cursor:
            create_toys_table_query = """CREATE TABLE IF NOT EXISTS `toys`( 
                                    id INT NOT NULL AUTO_INCREMENT, 
                                    toy_id INT, 
                                    name VARCHAR(30), 
                                    status VARCHAR(30),
                                    status_updated DATE,
                                    PRIMARY KEY (id))"""
            cursor.execute(create_toys_table_query)

            create_games_table_query = """CREATE TABLE IF NOT EXISTS `games`( 
                                    id INT NOT NULL AUTO_INCREMENT, 
                                    game_id INT,
                                    name VARCHAR(30),
                                    date DATE,
                                    PRIMARY KEY (id))"""
            cursor.execute(create_games_table_query)

            create_toys_games_table_query = """CREATE TABLE IF NOT EXISTS `toys_games`( 
                                    id INT NOT NULL AUTO_INCREMENT, 
                                    game_id INT,
                                    toy_id INT, 
                                    note VARCHAR(255), 
                                    PRIMARY KEY (id))"""
            cursor.execute(create_toys_games_table_query)

            create_toys_repair_table_query = """CREATE TABLE IF NOT EXISTS `toys_repair`( 
                                    id INT NOT NULL AUTO_INCREMENT, 
                                    toy_id INT, 
                                    issue_description VARCHAR(255), 
                                    PRIMARY KEY (id))"""
            cursor.execute(create_toys_repair_table_query)
            
        print('Tables create')

        with connection.cursor() as cursor:
            insert_toys_query = """INSERT INTO toys(toy_id, name, status, status_updated)
                                    VALUES (%s, %s, %s, %s)"""
            cursor.executemany(insert_toys_query, toys)
            connection.commit()

            insert_games_query = """INSERT INTO games(game_id, name, date)
                                    VALUES (%s, %s, %s)"""
            cursor.executemany(insert_games_query, games)
            connection.commit()
            
            insert_toys_games_query = """INSERT INTO toys_games(game_id, toy_id, note)
                                    VALUES (%s, %s, %s)"""
            cursor.executemany(insert_toys_games_query, toys_games)
            connection.commit()

            insert_toys_repair_query = """INSERT INTO toys_repair(toy_id, issue_description)
                                    VALUES (%s, %s)"""
            cursor.executemany(insert_toys_repair_query, toys_repair)
            connection.commit()
       
        print('Insert data')

        # TASK#3.a
        games_select = []
        with connection.cursor() as cursor:
            select = """SELECT * FROM games WHERE date BETWEEN (NOW() - INTERVAL 7 DAY) AND NOW();"""
            cursor.execute(select)
            rows = cursor.fetchall()
             
            for row in rows:
                games_select.append(row)

       
        with open ('a.yaml', 'a') as yaml_file:
            new_data = yaml.dump(games_select)
            yaml_file.write(new_data)

        # TASK#3.b
        toys_select = []
        with connection.cursor() as cursor:
            select = """SELECT * FROM toys WHERE status_updated BETWEEN (NOW() - INTERVAL 7 DAY) AND NOW();"""
            cursor.execute(select)
            rows = cursor.fetchall()
             
            for row in rows:
                toys_select.append(row)

       
        with open ('b.yaml', 'a') as yaml_file:
            new_data = yaml.dump(toys_select)
            yaml_file.write(new_data)

        # TASK#3.c
        note_select = []
        with connection.cursor() as cursor:
            select = """SELECT * FROM toys_repair
                        WHERE issue_description LIKE '%repair%' OR issue_description LIKE '%break%' OR issue_description LIKE '%broken%'"""
            cursor.execute(select)
            rows = cursor.fetchall()
             
            for row in rows:
                note_select.append(row)

       
        with open ('c.yaml', 'a') as yaml_file:
            new_data = yaml.dump(note_select)
            yaml_file.write(new_data)


        # TASK#4
        with connection.cursor() as cursor:
            select = """SELECT toys.toy_id,
	                    toys.name,
                        toys.status,
                        toys.status_updated,
                        games.name,
                        games.date,
                        toys_games.note
                        FROM toys INNER JOIN toys_games 
                        ON toys.toy_id = toys_games.toy_id INNER JOIN games ON toys_games.game_id = games.game_id
                        WHERE games.date BETWEEN (NOW() - INTERVAL 1 YEAR) AND NOW();"""
            cursor.execute(select)
            rows = cursor.fetchall()
             
            for row in rows:
                print(row)


        # TASK#5
        with connection.cursor() as cursor:
            select = """SELECT toys.toy_id, toys.name, toys_repair.issue_description FROM toys INNER JOIN toys_repair 
                        ON toys.toy_id = toys_repair.toy_id
                        WHERE LOWER(toys_repair.issue_description) NOT LIKE '%repair%';"""
            cursor.execute(select)
            rows = cursor.fetchall()
             
            for row in rows:
                print(row)

    finally:
        connection.close()
except Exception as ex:
    print('Сonnect failed')
    

