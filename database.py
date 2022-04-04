import sqlite3 as sql



def change_subscription(id, blog=None, contests=None):
    # create a local database file or just connect if exists
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    
    
    # create table if not exists
    cursor.execute("""CREATE TABLE IF NOT EXISTS subs (id BIGINT PRIMARY KEY, blog INT, contests INT);""")
    blog_text = ('', '', '')
    contests_text = ('', '', '')
    if blog is not None:
        blog_text = (', blog', f', {int(blog)}', f'blog = {int(blog)}')
    if contests is not None:
        contests_text = (', contests', f', {int(contests)}', f'contests = {int(contests)}')
    query = f"""INSERT INTO subs (id{blog_text[0]}{contests_text[0]}) VALUES ({id}{blog_text[1]}{contests_text[1]}) ON CONFLICT(id) DO UPDATE SET {blog_text[2]}{contests_text[2]};"""
    cursor.execute(query)
    connection.commit()
    connection.close()
    


def change_post(id):
    # create a local database file or just connect if exists
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    
    # create table if not exists
    cursor.execute("""CREATE TABLE IF NOT EXISTS post (id INT, post TINYINT);""")
    cursor.execute(f"""REPLACE INTO post (id, post) VALUES ({id}, 1);""")
    connection.commit()
    connection.close()


def get_last_rus_post():
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS post (id INT, post TINYINT);""")
    connection.commit()
    cursor.execute("SELECT * FROM post;")
    ans = cursor.fetchone()
    if not ans:
        ans = [(101079, 1)]
    connection.close()
    return ans[0][0]


def get_subs(id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS subs (id BIGINT PRIMARY KEY, blog INT, contests INT);""")
    connection.commit()
    cursor.execute(f"SELECT * FROM subs WHERE id = {id};")
    ans = cursor.fetchone()
    if not ans:
        ans = {'blog': False,
               'contests': False}
    else:
        ans = ans[1:]
        ans = {'blog': ans[0],
               'contests': ans[1]}
    connection.close()
    return ans