import curses

import arrow
from curses_ui.widget import Widget
from util import temperature_color_code, int_half
from constants import timezone

class CurrentWidget(Widget):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    super().__init__(curses_screen_instance, pos_y, pos_x, height, width)

  def draw(self):
    (max_y, max_x) = self.screen.getmaxyx()
    self.instance.mvwin(0, 0)
    self.instance.resize(7, 28)

    self.instance.attron(curses.color_pair(3))
    self.instance.border()
    self.instance.attroff(curses.color_pair(3))

    self.instance.addstr(1, 2, f'Current   {arrow.utcnow().to(timezone).format("MM-DD HH:mm:ss")}')
    self.instance.addstr(2, 2, 'T °C')
    self.instance.addstr(3, 2, 'W km/h')
    self.instance.addstr(4, 2, 'H g/kg')
    self.instance.addstr(5, 2, 'P kg/kg')

    def draw_value(var_name, y, x, color_code_fn = None):
      val = self.data[var_name]
      variation = self.data[var_name + '_variation']
      pos = (y, x)

      if not(val == ''):
        color = curses.color_pair(color_code_fn(float(val))) if not(color_code_fn == None) else curses.color_pair(1)
        variation_symbol = '↑' if variation > 0 else '↓'
        self.instance.addstr(pos[0], pos[1], f'{str(val).center(9)} {variation_symbol} ', color)
      else:
        color = curses.color_pair(1)
        self.instance.addstr(pos[0], pos[1], ' - ', color)

    value_x = 12
    draw_value('temperature', 2, value_x, temperature_color_code)
    draw_value('humidity', 4, value_x, None)
    draw_value('wind', 3, value_x, None)
    draw_value('precipitation', 5, value_x, None)

    self.instance.refresh()