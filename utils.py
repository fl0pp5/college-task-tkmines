import os
import sqlite3
import tkinter
import datetime


class Timer:
    def __init__(self, frame: tkinter.Frame):
        self._elapsed_time = 0
        self._frame = frame
        self._job_id = None

    @property
    def elapsed_time(self):
        return str(datetime.timedelta(seconds=self._elapsed_time))

    def start(self):
        self._update_time()

    def stop(self):
        if self._job_id:
            self._frame.after_cancel(self._job_id)

    def _update_time(self):
        self._frame.winfo_toplevel().title(self.elapsed_time)
        self._elapsed_time += 1
        self._job_id = self._frame.after(1000, self._update_time)


class RecordManager:
    def __init__(self):
        self.connection = sqlite3.connect("records.db")
        self.init()

    def __del__(self):
        self.connection.close()

    def init(self) -> None:
        query = """
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            record TEXT
        );"""

        with self.connection:
            self.connection.execute(query)

    def add(self, name: str, record: str) -> None:
        query = "INSERT INTO records (name, record) VALUES (?, ?)"

        with self.connection:
            try:
                self.connection.execute(query, (name, record))
            except sqlite3.IntegrityError:
                pass

    def all(self) -> list[tuple[str, str]]:
        query = "SELECT name, record FROM records ORDER BY datetime(record)"

        with self.connection:
            return self.connection.execute(query).fetchall()


class ImageManager:
    IMAGE_NAMES = {
        "n": [f"tile_{i}.png" for i in range(9)],
        "bomb": "tile_bomb.png",
        "close": "tile_close.png",
        "explode": "tile_explode.png",
        "flag": "tile_flag.png",
        "miss": "tile_miss.png",
        "status_idle": "status_idle.png",
        "status_scary": "status_scary.png",
        "status_cool": "status_cool.png",
        "status_damn": "status_damn.png",
    }

    @staticmethod
    def load(image_root: str):
        file_list = os.listdir(image_root)
        img_list = {}

        for key, value in ImageManager.IMAGE_NAMES.items():
            if key == "n":
                img_list[key] = list()
                for name in value:
                    if name not in file_list:
                        raise FileNotFoundError(f"{name} not found")
                    img_list[key].append(tkinter.PhotoImage(file=os.path.join(image_root, name)))
                continue

            if value not in file_list:
                raise FileNotFoundError(f"{value} not found")

            img_list[key] = tkinter.PhotoImage(file=os.path.join(image_root, value))

        return img_list
