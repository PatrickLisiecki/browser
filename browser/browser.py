import tkinter

from utils.text import lex
from utils.render import layout

WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 13, 18
SCROLL_STEP = 100


class Browser:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.bind("<Down>", self.scrolldown)
        self.canvas = tkinter.Canvas(self.window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        self.display_list = []
        self.scroll = 0

    def load(self, url):
        body = url.make_request()
        text = lex(body)
        self.display_list = layout(text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, char in self.display_list:
            if y > self.scroll + HEIGHT: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=char)

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()
