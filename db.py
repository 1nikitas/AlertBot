import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def addUser(self, tg_id, table_number):
        with self.connection:
            return self.cursor.execute("INSERT INTO data(tg_id, table_number) VALUES (?, ?)", (tg_id, table_number,))

    def userExists(self, tg_id):
        with self.connection:
            return bool(len(self.cursor.execute("SELECT * FROM data WHERE tg_id = ?", (tg_id,)).fetchall()))

    def tgIdSelector(self, table_number):
        with self.connection:
            return self.cursor.execute(
                "SELECT tg_id from data where table_number=?;", (table_number,)).fetchall()

if __name__ == '__main__':
    db = Database('db.db')
    print(*db.tgIdSelector("123213")[0])