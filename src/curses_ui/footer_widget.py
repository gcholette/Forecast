import curses
from curses_ui.widget import Widget
from constants import version, spinner_frames_1, spinner_frames_2
from curses_ui.spinner import Spinner

class FooterWidget(Widget):
  def __init__(self, curses_screen_instance, pos_y, pos_x, height, width):
    super().__init__(curses_screen_instance, pos_y, pos_x, height, width)
    self.message = ''
    self.spinner = Spinner(spinner_frames_1)

  def draw(self):
    (max_y, max_x) = self.screen.getmaxyx()
    self.instance.mvwin(max_y - 3, 0)
    self.instance.resize(3, max_x)

    self.instance.attron(curses.color_pair(3))
    self.instance.border()
    self.instance.attroff(curses.color_pair(3))

    self.instance.addstr(1, 2, ' ', curses.color_pair(2))
    self.instance.addstr(1, 4, f'Forecasts v{version}')

    self.instance.addstr(1, max_x-3, self.spinner.render())

    half_loading_msg_length = int(len(self.message) / 2)
    half_footer_width = int(max_x / 2)
    self.instance.addstr(1, half_footer_width - half_loading_msg_length - 10, f'           {self.message}           ')
    self.spinner.animate()
    self.instance.refresh()
  
  def set_message(self, msg):
    self.message = msg
    if (msg == 'Up to date'):
      self.spinner.set_frames(spinner_frames_2)