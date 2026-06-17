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
            reviews TEXT,
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


    def insert_user(self, user_id: int, premium: int = 1, reviews: str = None, verification: str = "<tg-emoji emoji-id='5206607081334906820'>✅</tg-emoji>"):
        with self.connection:
            self.cursor.execute("""INSERT INTO users (id, premium, reviews, verification) VALUES (?, ?, ?, ?)""", (user_id, premium, reviews, verification))


    def insert_addresses(self, user_id: int, address: str = None, addresses: list = None, name: str = "Main"):
        with self.connection:
            if address:
                self.cursor.execute("""INSERT INTO addresses (user_id, address, name) VALUES (?, ?, ?)""", (user_id, address, name))

            for address in addresses:
                self.cursor.execute("""INSERT INTO addresses (user_id, address, name) VALUES (?, ?, ?)""", (user_id, address, name))

            self.connection.commit()


    def insert_user_and_addresses(self, user_id: int, premium: int = 1, reviews: str = None, verification: str = "<tg-emoji emoji-id='5206607081334906820'>✅</tg-emoji>", address: str = None, addresses: list = None, name: str = "Main"):
        self.insert_user(user_id=user_id, premium=premium, reviews=reviews, verification=verification)
        self.insert_addresses(user_id=user_id, address=address, addresses=addresses, name=name)













DB_PATH = os.path.join(os.path.dirname(__file__), "dates.db")
mdb = Database(DB_PATH)


if __name__ == '__main__':
    mdb.insert_user_and_addresses(user_id=5359181591, reviews="https://t.me/+5R0izSPP4bQyNGFi", addresses=['lucas.tontake.ton', 'UQAJcm9_x3USNzOBJDpnc5rsnSMdpeJfaCLyZHkouwOwSqni', 'agent-v-tone.ton'], name='Lucas')
    mdb.insert_user_and_addresses(user_id=7599554498, reviews="https://t.me/+L6Meh1ulK59iYWEy", addresses=['emil.tontake.ton', 'UQDMR0H9tXihLJmd1hOdH-K3uTlMmMZpD3ySxd7Dcst4IKaJ'], name='Emil')
    mdb.insert_user_and_addresses(user_id=1185048983, reviews="http://t.me/kasperskylaboratory_rewiews", addresses=['karim.tontake.ton', 'UQB0LxgMfVXKliqq7fHrrM5iZosutEW5pejpActnQBLEvWwX', 'kasperskylaboratory.ton'], name='Karim')
    mdb.insert_user_and_addresses(user_id=1433530, reviews="https://t.me/+Dau__pEQQ5tjYmQy", addresses=['lenety.tontake.ton', 'UQAvCaPfM7PmFS1wq27Q8acqt9zBWElNnVNGw3U0NEzF8lnt', 'lenety.ton'], name='Lenety')
    mdb.insert_user_and_addresses(user_id=163271274, reviews="https://t.me/vlad_otzyv", addresses=['vlad.tontake.ton', 'UQAWa-EmvczUDBE4wDCMtO-yzUQBFwDoRJQzC4fc9PV5QJpe'], name='Vlad')
    mdb.insert_user_and_addresses(user_id=1171669625, reviews="https://t.me/deals_ytehochek", addresses=['utya.tontake.ton', 'UQCWiBGqnM67HAT8ovgCn7M8CrKn2KpRThECg5IcjtRW1Iky', 'ytehochek-tg.ton'], name='Utya')
    mdb.insert_user_and_addresses(user_id=627894511, reviews="https://t.me/repa05", addresses=['maga.tontake.ton', 'UQDyp7DHpukpSreqtXcRBrZrxBbHnmS9-mDnQQ_TeF7NNNU9'], name='Maga')
    mdb.insert_user_and_addresses(reviews="https://t.me/info_MHE_OXOTA_TAKE", user_id=7734663828, addresses=['lilya.tontake.ton', 'UQCwBXCmdOY_McrjC-QkKCY2F3TrQgDbcsRMg6c3USTkZeR7'], name='Lilya')
    mdb.insert_user_and_addresses(reviews="https://t.me/JesusReview", user_id=912135415, addresses=['jesus.tontake.ton', 'UQC_6PkGJ136GJT4Wx789eS1SFAl5sUTw3Ql_lLwdcxGTA2Y'], name='Jesus')
    mdb.insert_user_and_addresses(reviews="https://t.me/+h20a4PhsUVw0MTg0", user_id=13100592, addresses=['froxwart.tontake.ton', 'UQAL-3sQ9odEGzDQamU6zHh7Zvy_wozPIVwplZ8hbh4-LIDW'], name='Froxwart')
    mdb.insert_user_and_addresses(reviews="https://t.me/otzivi_ceonista", user_id=1006151645, addresses=['ceonist.tontake.ton', 'UQA2khIiFQmhDuKKDxeZLyLTpj-TOFaVzSFkTXVbDzRy8gS0'], name='Ceonist')
    mdb.insert_user_and_addresses(reviews="https://t.me/suncher1_review", user_id=6910022647, addresses=['suncher.tontake.ton', 'UQD8dT52yFd5wQqJEsAKuNrIdeFrizRZzsJhq5UFyE_d1JKo'], name='Suncher')
    mdb.insert_user_and_addresses(reviews="https://t.me/ludomamontTake", user_id=4256745, addresses=['ludomamont.tontake.ton', 'UQCOGyF--fRzJJBfFm54wy1xExwokIlN5sBZEQfOiCNsBwH5'], name='Ludomamont')