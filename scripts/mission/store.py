"""Transactional, content-addressed local mission custody."""
import hashlib
import json
from pathlib import Path
import sqlite3


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


class Store:
    def __init__(self, root):
        self.root = Path(root).resolve()
        if any(p.casefold() == "oxyballs-industrial" for p in self.root.parts):
            raise ValueError("SOURCE_STATE_WRITE_FORBIDDEN")
        self.root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.root / "missions.sqlite3", timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS missions(
                id TEXT PRIMARY KEY, request TEXT NOT NULL, stage TEXT NOT NULL,
                outputs TEXT NOT NULL, error TEXT);
            CREATE TABLE IF NOT EXISTS artifacts(
                digest TEXT PRIMARY KEY, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events(
                seq INTEGER PRIMARY KEY AUTOINCREMENT, mission TEXT NOT NULL,
                kind TEXT NOT NULL, body TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS edges(
                mission TEXT NOT NULL, source TEXT NOT NULL, relation TEXT NOT NULL,
                target TEXT NOT NULL, UNIQUE(mission, source, relation, target));
        """)
        self.db.commit()

    def close(self):
        self.db.close()

    def put(self, value):
        key = digest(value)
        body = canonical(value)
        prior = self.db.execute("SELECT body FROM artifacts WHERE digest=?", (key,)).fetchone()
        if prior and prior["body"] != body:
            raise ValueError("ARTIFACT_COLLISION_OR_CORRUPTION")
        self.db.execute("INSERT OR IGNORE INTO artifacts VALUES(?,?)", (key, body))
        return key

    def get(self, key):
        row = self.db.execute("SELECT body FROM artifacts WHERE digest=?", (key,)).fetchone()
        if not row:
            raise ValueError("ARTIFACT_MISSING")
        value = json.loads(row["body"])
        if digest(value) != key:
            raise ValueError("ARTIFACT_HASH_MISMATCH")
        return value

    def event(self, mission, kind, value):
        self.db.execute("INSERT INTO events(mission,kind,body) VALUES(?,?,?)",
                        (mission, kind, canonical(value)))

    def edge(self, mission, source, relation, target):
        self.db.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?,?)",
                        (mission, source, relation, target))

    def status(self, mission):
        row = self.db.execute("SELECT * FROM missions WHERE id=?", (mission,)).fetchone()
        if not row:
            raise ValueError("UNKNOWN_MISSION")
        return {"mission_id": mission, "stage": row["stage"], "error": row["error"],
                "request": json.loads(row["request"]), "outputs": json.loads(row["outputs"]),
                "authority": "NONE", "independent_qualification": "NOT_ESTABLISHED"}

    def history(self, mission):
        self.status(mission)
        return [{"seq": r["seq"], "kind": r["kind"], "body": json.loads(r["body"])}
                for r in self.db.execute("SELECT * FROM events WHERE mission=? ORDER BY seq",
                                         (mission,))]

    def graph(self, mission):
        self.status(mission)
        return [dict(r) for r in self.db.execute(
            "SELECT source,relation,target FROM edges WHERE mission=? ORDER BY source,relation,target",
            (mission,))]
