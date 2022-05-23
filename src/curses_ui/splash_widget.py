
import curses
from curses_ui.widget import Widget
from constants import splash_strs, short_splash_strs
from curses_ui.spinner import Spinner
from util import int_half
import time

class SplashWidget(Widget):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    super().__init__(curses_screen_instance, pos_y, pos_x, height, width)

  def draw(self):
    (max_y, max_x) = self.screen.getmaxyx()
    longest = 0
    chosen_splash_str = splash_strs
    for string in splash_strs:
      length = len(string)
      if length > longest:
        longest = length

    if longest >= max_x:
      chosen_splash_str = short_splash_strs
      longest = len(short_splash_strs[0])

    start_x = int_half(max_x) - int_half(longest)
    start_y = int_half(max_y) - int_half(len(chosen_splash_str)) - 3

    self.instance.clear()
    self.instance.attron(curses.color_pair(4))
    for (string, i) in zip(chosen_splash_str, range(0, len(chosen_splash_str)-1)):
      self.instance.addstr(start_y + i, start_x, string)
    self.instance.attroff(curses.color_pair(4))

    self.instance.refresh()