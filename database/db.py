import sqlite3
import os
from typing import Any


class Database:
    def __init__(self, filepath: str):
        self.connection = sqlite3.connect(filepath)
        self.cursor = self.connection.cursor()


    def create_tables(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER NOT NULL,
            premium INTEGER NOT NULL DEFAULT 0,
            reviews TEXT DEFAULT 'https://telegram.org',
            verification TEXT NOT NULL DEFAULT '<tg-emoji emoji-id="5206607081334906820">✅</tg-emoji>'
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS addresses (
            user_id INTEGER NOT NULL,
            address TEXT NOT NULL,
            name TEXT NOT NULL
            )""")
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS dates (
            invoice_id TEXT NOT NULL,
            amount INTEGER NOT NULL,
            last_time TEXT NOT NULL,
            address TEXT NOT NULL,
            username TEXT
            )""")
            self.connection.commit()
            return



    def user_has_address(self, user_id: int) -> bool:
        with self.connection:
            self.cursor.execute("""SELECT 1 FROM addresses WHERE user_id = ?""", (user_id,))
            raw = self.cursor.fetchone()
            if raw: return True
            else: return False


    def get_user_verification(self, user_id: int) -> str:
        with self.connection:
            self.cursor.execute("""SELECT verification FROM users WHERE id = ?""", (user_id,))
            raw = self.cursor.fetchone()
            if raw: return raw[0] # <tg-emoji emoji-id="5206607081334906820">✅</tg-emoji>
            else: return '<tg-emoji emoji-id="5206607081334906820">✅</tg-emoji>' # '<tg-emoji emoji-id="5210952531676504517">❌</tg-emoji>'



    def _normalize_address_list(self, raw: list[tuple]) -> list[Any]:
        return [x[0] for x in raw]




    def get_user_addresses(self, user_id: int) -> list:
        with self.connection:
            self.cursor.execute("""SELECT address FROM addresses WHERE user_id = ?""", (user_id,))
            raw = self.cursor.fetchall()
            return self._normalize_address_list(raw=raw)



    def add_user_addresses(self, user_id: int, addresses: list):
        with self.connection:
            for address in addresses:
                self.cursor.execute("""INSERT INTO addresses (user_id, address) VALUES (?, ?)""", (user_id, address))

            self.connection.commit()


    def get_invoice_dates(self, invoice_uid: str):
        with self.connection:
            self.cursor.execute("""SELECT * FROM dates WHERE invoice_id = ?""", (invoice_uid,))
            raw = self.cursor.fetchone()
            if raw:
                return raw
            else:
                return None


    def write_invoice(self, invoice_uid: str, amount: float, last_time: str, address: str, username: str):
        amount = int(amount*1_000_000_000)
        with self.connection:
            self.cursor.execute("""INSERT INTO dates (invoice_id, amount, last_time, address, username) VALUES (?, ?, ?, ?, ?)""", (invoice_uid, amount, last_time, address, username))
            self.connection.commit()


    def get_user_addresses_all(self, user_id: int):
        with self.connection:
            self.cursor.execute("""SELECT * FROM addresses WHERE user_id = ?""", (user_id,))
            raw = self.cursor.fetchall()
            if raw: return raw
            else: return False


    def get_user_reviews(self, user_id: int):
        with self.connection:
            self.cursor.execute("""SELECT reviews FROM users WHERE id = ?""", (user_id,))
            raw = self.cursor.fetchone()
            if raw: return raw[0]
            else: return None













DB_PATH = os.path.join(os.path.dirname(__file__), "dates.db")
mdb = Database(DB_PATH)


if __name__ == '__main__':
    #mdb.add_user_addresses(5359181591, ['lucas.tontake.ton', 'UQAJcm9_x3USNzOBJDpnc5rsnSMdpeJfaCLyZHkouwOwSqni', 'agent-v-tone.ton'])
    print(8686)