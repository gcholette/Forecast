
import curses
from curses_ui.widget import Widget
from util import temperature_color_code, extract_value, extract_timestamp
from constants import active_variable_names

class HourlyWidget(Widget):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    super().__init__(curses_screen_instance, pos_y, pos_x, height, width)

  def draw(self):
    (max_y, max_x) = self.screen.getmaxyx()
    self.instance.mvwin(max_y - 11, 0)
    self.instance.resize(8, max_x)

    self.instance.attron(curses.color_pair(3))
    self.instance.border()
    self.instance.attroff(curses.color_pair(3))

    for (var_name, index_height) in zip(active_variable_names, range(0, len(active_variable_names))):
      no_data = len(self.data[var_name]) < 1
      data_values = list(map(extract_value,self.data[var_name]))
      data_times = list(map(extract_timestamp,self.data[var_name]))

      if no_data:
        for i in range(0, 48):
          data_times.append('-')
          data_values.append(' - ')
      else:
        for (d, i) in zip(data_values, range(0, len(data_values)-1)):
          data_values[i] = str(d).rjust(2,"0").center(4, " ")

      #self.instance.addstr(2, 2, 'T °C ')
      self.instance.addstr(index_height+2, 2, var_name[0:3])
      #self.instance.addstr(2, 8 + 8, '~~', curses.color_pair(10))

      for val, time, i in zip(data_values, data_times, list(range(0, len(data_values)))):
        chosen_x = 8 + (i*6)
        chosen_color =  curses.color_pair(1) if (no_data or (var_name != 'temperature')) else curses.color_pair(temperature_color_code(float(val)))
        if (chosen_x + 4 < max_x):
          self.instance.addstr(1, 8 + (i*6), f' {str(time)} ')
          self.instance.addstr(index_height + 2, 8 + (i*6), f'{val}', chosen_color)

    self.instance.refresh()