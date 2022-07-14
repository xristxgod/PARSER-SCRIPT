import time

from art import tprint

from app import run


def main():
    tprint("PARSER SCRIPT", font="bulbhead")
    while True:
        run()
        time.sleep(150)


if __name__ == '__main__':
    main()
