

import curses
from curses.textpad import rectangle


class App:
  def display(self, stdscr):
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLUE)

    (max_lines, max_cols) = (curses.LINES - 1, curses.COLS - 1)

    window1 = curses.newwin(10, 40, 5, 5)

    stdscr.clear()
    window1.clear()
    window1.addstr(2, 2, 'Forecasts', curses.color_pair(1))
    window1.refresh()
    rectangle(window1, 0, 0, 10-1, 40-2)
    window1.refresh()

    #pad = curses.newpad(100, 100)
    #for i in range(100):
    #  for j in range(26):
    #    char = chr(67 + j)
    #    pad.addstr(char, curses.color_pair(1))

    #stdscr.refresh()
    #for i in range(50):
    #  time.sleep(0.2)
    #  stdscr.clear()
    #  stdscr.refresh()
    #  pad.refresh(0, i, 5, i, 10, 25 + i)

    window1.getch()