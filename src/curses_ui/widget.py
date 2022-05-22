
from abc import ABC, abstractmethod
import curses

class Widget(ABC):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    self.screen = curses_screen_instance
    self.pos_x = pos_x
    self.pos_y = pos_y
    self.height = height
    self.width = width
    self.instance = curses.newwin(height, width, pos_y, pos_x)
    self.data = {}

  @abstractmethod
  def draw(self):
    pass

  def refresh(self):
    self.instance.refresh()

  def clear(self):
    self.instance.clear()

  def get_position(self):
    return (self.pos_y, self.pos_x)

  def move(self, y, x):
    self.pos_x = x
    self.pos_y = y
    self.instance.refresh()

  def get_dimensions(self):
    return (self.height, self.width)

  def resize(self, height, width):
    self.width = width
    self.height = height

  def set_data(self, data):
    self.data = data
