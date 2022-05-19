from signal import signal, SIGWINCH
import curses
from curses.textpad import rectangle
import time
from constants import version
from enum import Enum

TOO_SMALL_BOUNDARY_X = 57
SMALL_BOUNDARY_X = 75 
MEDIUM_BOUNDARY_X = 100 
LARGE_BOUNDARY_X = 150 
X_LARGE_BOUNDARY_X = 250 

class Breakpoints(Enum):
  TOO_SMALL = 1
  SMALL = 2
  MEDIUM = 3
  LARGE = 4
  X_LARGE = 5


def int_half(x):
  return int((x / 2) - 1)

class CursesApp:
  def init(self, stdscr):
    self.screen = stdscr
    self.active_breakpoints = (Breakpoints.MEDIUM, Breakpoints.MEDIUM)

    (init_y, init_x) = self.screen.getmaxyx()
    self.max_y = init_y
    self.max_x = init_x

    self.pad1 = curses.newpad(self.max_y-1, self.max_x)
    self.footer = curses.newwin(0, init_x, init_y-2, 0)

    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)

    self.render_loop()

  def render_loop(self):
    while 1:
      time.sleep(0.2)
      self.loading_msg = "Up to date"

      (max_y, max_x) = self.screen.getmaxyx()
      self.max_y = max_y
      self.max_x = max_x

      self.setBreakpoints()

      self.draw_screen()
      self.draw_footer()

      key_or_event = self.screen.getch()
      if key_or_event == curses.KEY_RESIZE:
        self.screen.clear()
        self.pad1.clear()
        self.screen.refresh()
      if key_or_event == ord('q'):
        exit(0)

  def draw_screen(self):
      if self.is_window_too_small():
        self.screen.addstr(0, 0, f'Terminal is too small.')
        self.screen.addstr(1, 0, f'Please use a wider interface.')
      else:
        max_box_y = self.max_y - 15 
        max_box_x = self.max_x - 1
        max_pad_y = self.max_y
        max_pad_x = self.max_x

        self.pad1.resize(max_pad_y, max_pad_x)
        rectangle(self.screen, 0, 0, max_box_y, max_box_x)
        self.screen.refresh()

        for i in range(3):
          for j in range(26):
            char = chr(67 + j)
            self.pad1.addstr(char, curses.color_pair(1))

        self.pad1.refresh(0, 0, 1, 1, max_box_y-3, max_box_x- 3)

  def draw_footer(self):
      self.footer.clear()

      if not(self.is_window_too_small()):
        self.footer.mvwin(self.max_y - 3, 0)
        self.footer.resize(3, self.max_x+1)
        (max_y, max_x) = self.footer.getmaxyx()
        rectangle(self.footer, 0, 0, 2, max_x-2)
        self.footer.addstr(1, 2, ' ', curses.color_pair(2))
        self.footer.addstr(1, 4, f'Forecasts v{version}')

        half_loading_msg_length = int(len(self.loading_msg) / 2)
        half_footer_width = int(self.max_x / 2)
        self.footer.addstr(1, half_footer_width - half_loading_msg_length, self.loading_msg)

      self.screen.refresh()
      self.footer.refresh()

  def setBreakpoints(self):
      if (self.max_x <= TOO_SMALL_BOUNDARY_X):
        self.active_breakpoints = (self.active_breakpoints[0], Breakpoints.TOO_SMALL)
      if (self.max_x > TOO_SMALL_BOUNDARY_X):
        self.active_breakpoints = (self.active_breakpoints[0], Breakpoints.SMALL)

      if (self.max_y <= 8):
        self.active_breakpoints = (Breakpoints.TOO_SMALL, self.active_breakpoints[1])
      if (self.max_y > 8):
        self.active_breakpoints = (Breakpoints.SMALL, self.active_breakpoints[1])

  def is_window_too_small(self):
      (bk_y, bk_x) = self.active_breakpoints
      return bk_x == Breakpoints.TOO_SMALL or bk_y == Breakpoints.TOO_SMALL
