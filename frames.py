import tkinter
import tkinter.messagebox
import tkinter.simpledialog

from lib.mines import Minefield
import utils


class Tile(tkinter.Button):
    def __init__(self, parent: tkinter.Frame, x: int, y: int, image: tkinter.PhotoImage):
        super().__init__(parent, image=image)
        self.parent = parent
        self.x = x
        self.y = y


class GameFrame(tkinter.Frame):
    def __init__(self, game, *args, **kwargs):
        super().__init__(game.root, *args, **kwargs)

        self._game = game


class PlayFrame(GameFrame):
    def __init__(self, game, width: int, height: int, mines_n: int, theme: str):
        super().__init__(game)

        self.theme = theme
        self.tiles = utils.ImageManager.load(self.theme)

        self.minefield = Minefield(width, height, mines_n)

        for x, y in self.minefield:
            tile = Tile(self, x, y, image=self.tiles["close"])
            tile.bind("<Button-1>", lambda event, current=tile: self.click(event, current))
            tile.bind("<Button-3>", lambda event, current=tile: self.click(event, current))
            tile.bind("<ButtonRelease-1>", self.change_status)
            tile.grid(row=tile.y + 1, column=tile.x)

        self.status = tkinter.Button(
            self,
            image=self.tiles["status_idle"],
            command=lambda: self._game.switch(
                PlayFrame, self.minefield.width, self.minefield.height, self.minefield.mines_n, self.theme)
        )
        self.status.grid(row=0, column=0, columnspan=self.minefield.width)

        self.timer = utils.Timer(self)
        self.timer.start()

    def change_status(self, event: tkinter.Event):
        self.status.configure(image=self.tiles["status_idle"])

    def click(self, event: tkinter.Event, tile: Tile):
        match event.num:
            case 1:
                self.status.configure(image=self.tiles["status_scary"])
                self.minefield.open(tile.x, tile.y)
            case 3:
                self.minefield.flag(tile.x, tile.y)

        win = self.minefield.is_win()
        loose = self.minefield.exploded

        for child in self.children.values():
            if isinstance(child, Tile):
                if win or loose:
                    child.unbind("<Button-1>")
                    child.unbind("<Button-3>")
                    child.unbind("<ButtonRelease-1>")
                    self.timer.stop()

                child.configure(image=self.get_img_by_tile(child))
                child.update()

        if win:
            self.status.configure(image=self.tiles["status_cool"])
            self.on_win()
        if loose:
            self.status.configure(image=self.tiles["status_damn"])

    def get_img_by_tile(self, tile: Tile):
        cell = self.minefield.at(tile.x, tile.y)
        img = None

        if self.minefield.exploded:
            if cell.opened:
                img = self.tiles["bomb"] if cell.mined else self.tiles["n"][cell.mines_around]
            elif cell.flagged:
                img = self.tiles["flag"] if cell.mined else self.tiles["miss"]
            else:
                img = self.tiles["explode"] if cell.mined else self.tiles["close"]

        else:
            if cell.opened:
                img = self.tiles["n"][cell.mines_around]
            elif cell.flagged:
                img = self.tiles["flag"]
            else:
                img = self.tiles["close"]

        return img

    def on_win(self):
        elapsed = self.timer.elapsed_time
        name = tkinter.simpledialog.askstring("YOU WIN!", f"record: {elapsed}")
        if name:
            self._game.record_manager.add(name, elapsed)


class MenuFrame(GameFrame):
    def __init__(self, game):
        super().__init__(game)

        tkinter.Button(
            self, text="10x10x10",
            command=lambda: self._game.switch(PlayFrame, 10, 10, 10, "themes/native")
        ).pack()

        tkinter.Button(
            self, text="20x20x20",
            command=lambda: self._game.switch(PlayFrame, 20, 20, 20, "themes/native"),
        ).pack()

        tkinter.Button(
            self, text="30x30x30",
            command=lambda: self._game.switch(PlayFrame, 30, 30, 30, "themes/native")
        ).pack()
