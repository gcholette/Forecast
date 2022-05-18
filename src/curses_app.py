from signal import signal, SIGWINCH
import curses
from curses.textpad import rectangle
import time

def int_half(x):
  return int((x / 2) - 1)

#class Box:

class CursesApp:
  def display(self, stdscr):
    (init_y, init_x) = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLUE)
    pad = curses.newpad(init_y-1, init_x-1)
    stdscr.refresh()

    while 1:
      time.sleep(0.2)
      (max_y, max_x) = stdscr.getmaxyx()

      max_box_y = max_y - 3
      max_box_x = max_x - 3

      max_pad_y = max_y
      max_pad_x = max_x

      pad.resize(max_pad_y, max_pad_x)
      rectangle(stdscr, 0, 0, max_box_y, max_box_x)
      stdscr.refresh()

      for i in range(3):
        for j in range(26):
          char = chr(67 + j)
          pad.addstr(char, curses.color_pair(1))

      pad.refresh(0, 0, 1, 1, max_box_y-3, max_box_x- 3)


      key_or_event = stdscr.getch()
      if key_or_event == curses.KEY_RESIZE:
        stdscr.clear()
        pad.clear()
        stdscr.refresh()
      if key_or_event == curses.KEY_DOWN:
        exit(0)
      