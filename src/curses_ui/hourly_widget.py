
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

    no_data = len(self.data['temperature']) < 1
    data_values = list(map(extract_value,self.data['temperature']))
    data_times = list(map(extract_timestamp,self.data['temperature']))

    if no_data:
      for i in range(0, 48):
        data_times.append('-')
        data_values.append(' - ')
    else:
      for (d, i) in zip(data_values, range(0, len(data_values)-1)):
        data_values[i] = str(d).rjust(2,"0").center(4, " ")

    self.instance.addstr(2, 2, 'T °C ')
    #self.instance.addstr(2, 8 + 8, '~~', curses.color_pair(10))

    for val, time, i in zip(data_values, data_times, list(range(0, len(data_values)))):
      chosen_x = 8 + (i*6)
      chosen_color = curses.color_pair(temperature_color_code(float(val))) if not(no_data) else curses.color_pair(1)
      if (chosen_x + 4 < max_x):
        self.instance.addstr(1, 8 + (i*6), f' {str(time)} ')
        self.instance.addstr(2, 8 + (i*6), f'{val}', chosen_color)

    self.instance.refresh()