import os.path
import tkinter
import tkinter.messagebox
import typing

from frames import GameFrame, MenuFrame
import utils


class Game:
    def __init__(self, root: tkinter.Tk):
        self._frame: GameFrame | None = None
        self._root = root

        self._init_ui()

        self.record_manager = utils.RecordManager()

    def _init_ui(self):
        self._root.iconbitmap(True, os.path.join("res", "icon", "milk.ico"))
        self._root.title("TkMines")
        self._root.resizable(False, False)
        self._root.minsize(230, 230)

        main_menu = tkinter.Menu(self._root)
        self._root.configure(menu=main_menu)

        game_menu = tkinter.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New", command=lambda: self.switch(MenuFrame))
        game_menu.add_command(label="Records", command=self.records)
        game_menu.add_command(label="Quit", command=self._root.quit)

        help_menu = tkinter.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.about)
        help_menu.add_command(label="How to play?", command=self.how2play)

        self.switch(MenuFrame)

    @property
    def root(self) -> tkinter.Tk:
        return self._root

    def records(self):
        top_10 = self.record_manager.all()[:10]
        tkinter.messagebox.showinfo("TOP-10", "\n".join([" :: ".join(i) for i in top_10]))

    def about(self):
        tkinter.messagebox.showinfo("About", "TkMines :: version 0.1")

    def how2play(self):
        tkinter.messagebox.showinfo("How to play?", "https://en.wikipedia.org/wiki/Minesweeper_(video_game)")

    def switch(self, frame: typing.Type[GameFrame], *args, **kwargs):
        if self._frame:
            self._frame.destroy()

        self._frame = frame(self, *args, **kwargs)
        self._frame.pack()

    def run(self):
        self._root.mainloop()

