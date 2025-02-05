import tkinter
from browser.browser import Browser
from browser.url import URL


if __name__ == "__main__":
    import sys

    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
