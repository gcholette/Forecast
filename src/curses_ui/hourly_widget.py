
import curses
from curses_ui.widget import Widget
from util import temperature_color_code, extract_value, extract_timestamp

class HourlyWidget(Widget):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    super().__init__(curses_screen_instance, pos_y, pos_x, height, width)

  def draw(self):
    (max_y, max_x) = self.screen.getmaxyx()
    self.instance.attron(curses.color_pair(3))
    self.instance.border()
    self.instance.attroff(curses.color_pair(3))

    if (len(self.data['temperature']) < 1):
      return

    self.instance.addstr(2, 2, 'T °C ')
    #self.instance.addstr(2, 8 + 8, '~~', curses.color_pair(10))

    data_values = list(map(extract_value,self.data['temperature']))
    data_times = list(map(extract_timestamp,self.data['temperature']))
    for val, time, i in zip(data_values, data_times, list(range(0, len(data_values)))):
      chosen_x = 8 + (i*6)
      chosen_color = curses.color_pair(temperature_color_code(float(val)))
      if (chosen_x + 4 < max_x):
        self.instance.addstr(1, 8 + (i*6), f' {str(time)} ')
        self.instance.addstr(2, 8 + (i*6), f'{str(val).rjust(2,"0").center(4, " ")}', chosen_color)

    self.instance.refresh()