from browser.url import URL


def show(body):
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            print(c, end="")


def load(url):
    body = url.make_request()
    show(body)


if __name__ == "__main__":
    import sys

    load(URL(sys.argv[1]))
