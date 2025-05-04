# Storage manager for handling data storage and retrieval
# Define functions for saving and loading data here.

import sqlite3
from config import load_config
from typing import Any, List, Tuple

class SQLiteBackend:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._create_table()

    def _create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            timestamp TEXT NOT NULL,
            description TEXT,
            calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fat INTEGER,
            caffeine INTEGER
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_entry(self, entry: dict):
        query = """
        INSERT INTO entries (timestamp, description, calories, protein, carbs, fat, caffeine)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.conn.execute(query, (
            entry["timestamp"],
            entry["description"],
            entry["calories"],
            entry["protein"],
            entry["carbs"],
            entry["fat"],
            entry["caffeine"]
        ))
        self.conn.commit()

    def get_entries(self, start: str, end: str) -> List[Tuple]:
        query = """
        SELECT * FROM entries
        WHERE date(timestamp) BETWEEN date(?) AND date(?)
        """
        cursor = self.conn.execute(query, (start, end))
        return cursor.fetchall()

    def delete_entries(self, date: str):
        query = """
        DELETE FROM entries
        WHERE date(timestamp) = date(?)
        """
        self.conn.execute(query, (date,))
        self.conn.commit()

    def flush_entries(self):
        query = "DELETE FROM entries"
        self.conn.execute(query)
        self.conn.commit()

    def get_daily_summary(self, date: str) -> Tuple:
        query = """
        SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fat), SUM(caffeine)
        FROM entries
        WHERE date(timestamp) = date(?)
        """
        cursor = self.conn.execute(query, (date,))
        return cursor.fetchone()

    def get_weekly_summary(self, start: str, end: str) -> Tuple:
        query = """
        SELECT SUM(calories), SUM(protein), SUM(carbs), SUM(fat), SUM(caffeine)
        FROM entries
        WHERE date(timestamp) BETWEEN date(?) AND date(?)
        """
        cursor = self.conn.execute(query, (start, end))
        return cursor.fetchone()

class JSONBackend:
    def __init__(self, base_dir: str, mode: str):
        self.base_dir = base_dir
        self.mode = mode

    def add_entry(self, entry: Any):
        # Placeholder for adding an entry to JSON
        print(f"Adding entry to JSON in {self.base_dir} with mode {self.mode}: {entry}")

class StorageManager:
    def __init__(self, config_path: str):
        config = load_config(config_path)
        self.primary = SQLiteBackend(config.sqlite.path)
        self.secondary = JSONBackend(config.json.base_dir, config.json.mode)

    def add_entry(self, entry: Any):
        try:
            self.primary.add_entry(entry)
        except Exception as e:
            print(f"Error adding entry to primary storage: {e}")
        try:
            self.secondary.add_entry(entry)
        except Exception as e:
            print(f"Error adding entry to secondary storage: {e}")

    def get_entries(self, start: str, end: str):
        raise NotImplementedError("get_entries is not implemented yet.")

    def delete_entries(self, date: str):
        raise NotImplementedError("delete_entries is not implemented yet.")

    def flush_entries(self):
        raise NotImplementedError("flush_entries is not implemented yet.")

    def get_daily_summary(self, date: str):
        raise NotImplementedError("get_daily_summary is not implemented yet.")

    def get_weekly_summary(self, start: str, end: str):
        raise NotImplementedError("get_weekly_summary is not implemented yet.")
