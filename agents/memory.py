import sqlite3, json, os
class Memory:
    def __init__(self, path="memory.sqlite"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS seen(hash TEXT PRIMARY KEY, url TEXT)")
        self.db.commit()
    def seen(self, h: str) -> bool:
        cur = self.db.execute("SELECT 1 FROM seen WHERE hash=?", (h,))
        return cur.fetchone() is not None
    def remember(self, docs):
        self.db.executemany("INSERT OR IGNORE INTO seen(hash, url) VALUES(?,?)",
                            [(d["hash"], d["url"]) for d in docs])
        self.db.commit()
