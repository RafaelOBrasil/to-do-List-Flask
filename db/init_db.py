import sqlite3

con = sqlite3.connect("./db/to_do_list.db")

cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS USER (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        senha TEXT NOT NULL
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS TAREFAS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data TEXT,
        status TEXT,
        id_usuario INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES USER(id)
    )
""")

con.commit()
con.close()