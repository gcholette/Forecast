import copy
import curses
import time
from constants import TOO_SMALL_BOUNDARY_X
from enum import Enum
from content_manager import ContentManager
from util import int_half, filter_future_only
from threading import Thread
from models.current_forecast import CurrentForecast
from curses_ui.hourly_widget import HourlyWidget
from curses_ui.footer_widget import FooterWidget
from curses_ui.current_widget import CurrentWidget
from curses_ui.splash_widget import SplashWidget

empty_hrdps_data = {
  'temperature': [],
  'humidity': [],
  'wind': [],
  'precipitation': []
}

hrdps_data = copy.deepcopy(empty_hrdps_data)
current_data = CurrentForecast.get_empty()
loading_msg: str = 'Up to date'
updated_data = False

class Breakpoints(Enum):
  TOO_SMALL = 1
  SMALL = 2
  MEDIUM = 3
  LARGE = 4
  X_LARGE = 5


class CursesApp():
  def __init__(self):
    self.counter: int = 0
    self.content_manager = ContentManager()
    self.hourly_data_scrolled = copy.deepcopy(empty_hrdps_data)
    self.data_times = copy.deepcopy(empty_hrdps_data)
    self.data_values = copy.deepcopy(empty_hrdps_data)
    self.hourly_data_scroll = 0

  def init(self, stdscr):
    self.screen = stdscr
    curses.initscr()
    curses.curs_set(False)
    self.active_breakpoints = (Breakpoints.MEDIUM, Breakpoints.MEDIUM)

    (init_y, init_x) = self.screen.getmaxyx()
    self.max_y = init_y
    self.max_x = init_x

    self.refresh_data()
    self.footer = FooterWidget(self.screen, init_y-2, 0, 0, init_x)
    self.hourly_widget = HourlyWidget(self.screen, 13, 0, 4, init_x)
    self.current_widget = CurrentWidget(self.screen, 0, 0, 7, int_half(init_x))
    self.splash = SplashWidget(self.screen, 0, 0, init_y-4, init_x)

    self.init_colors()

    self.boot_sequence()

    self.render_loop()

  def render_loop(self):
    while 1:
      (max_y, max_x) = self.screen.getmaxyx()
      self.max_y = max_y
      self.max_x = max_x

      self.setBreakpoints(max_y, max_x)

      if (len(self.hourly_data_scrolled['temperature']) == 0 or updated_data):
        self.scroll_hourly_data()
        self.current_widget.set_data(current_data)

      self.draw_screen()
      self.counter += 1
      if (self.counter == 800):
        self.refresh_data()
        self.counter = 0

      if not(self.is_window_too_small()):
        self.footer.draw()
        self.footer.set_message(loading_msg)
        self.hourly_widget.draw()
        self.current_widget.draw()

      self.screen.timeout(100)
      self.screen.move(0, 0)

      key_or_event = self.screen.getch()
      if key_or_event == curses.KEY_RIGHT:
        self.set_hourly_data_scroll(self.hourly_data_scroll + 1)
      if key_or_event == curses.KEY_LEFT and self.hourly_data_scroll > 0:
        self.set_hourly_data_scroll(self.hourly_data_scroll - 1)
      if key_or_event == curses.KEY_RESIZE:
        self.refresh_all_windows()
      if key_or_event == ord('q'):
        exit(0)
      else:
        curses.echo()

  def set_hourly_data_scroll(self, val):
    self.hourly_data_scroll = val
    self.scroll_hourly_data()
    self.hourly_widget.refresh()
  
  def scroll_hourly_data(self):
    global updated_data

    hourly_data_scrolled = {}
    hourly_data_scrolled['temperature'] = []
    for d, i in zip(hrdps_data['temperature'], list(range(0, len(hrdps_data['temperature'])))):
      if i > self.hourly_data_scroll:
        hourly_data_scrolled['temperature'].append(d)

    self.hourly_widget.set_data(hourly_data_scrolled)
    updated_data = False

  def draw_screen(self):
    if self.is_window_too_small():
      self.screen.addstr(0, 0, f'Terminal is too small.')
      self.screen.addstr(1, 0, f'Please use a wider interface.')

  def boot_sequence(self):
    self.splash.draw()
    self.footer.set_message('Starting up')
    self.footer.draw()
    for i in range(0, 20):
      time.sleep(0.1)
      self.footer.draw()
    self.splash.clear()
    self.splash.refresh()
    self.screen.clear()
    self.screen.refresh()

  def setBreakpoints(self, max_y, max_x):
    if (max_x <= TOO_SMALL_BOUNDARY_X):
      self.active_breakpoints = (self.active_breakpoints[0], Breakpoints.TOO_SMALL)
    if (max_x > TOO_SMALL_BOUNDARY_X):
      self.active_breakpoints = (self.active_breakpoints[0], Breakpoints.SMALL)
    if (max_y <= 8):
      self.active_breakpoints = (Breakpoints.TOO_SMALL, self.active_breakpoints[1])
    if (max_y > 8):
      self.active_breakpoints = (Breakpoints.SMALL, self.active_breakpoints[1])

  def is_window_too_small(self):
    (bk_y, bk_x) = self.active_breakpoints
    return bk_x == Breakpoints.TOO_SMALL or bk_y == Breakpoints.TOO_SMALL

  def init_colors(self):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(9, 160, curses.COLOR_BLACK)
    curses.init_pair(10, 39, curses.COLOR_BLACK)
    curses.init_pair(11, 166, curses.COLOR_BLACK)
    for i in (list(range(25, 194))):
      curses.init_pair(i, curses.COLOR_BLACK, i)


  def refresh_all_windows(self):
    self.screen.clear()
    self.footer.clear()
    self.hourly_widget.clear()
    self.current_widget.clear()
    self.screen.refresh()
    self.footer.refresh()
    self.hourly_widget.refresh()
    self.current_widget.refresh()

  def refresh_data(self):
    t = Thread(target=self.use_content_manager)
    t.start()

  # Threaded fn
  def use_content_manager(self):
    global hrdps_data
    global loading_msg
    global updated_data 
    global current_data 
    loading_msg = 'Loading HRDPS data'

    data = {}
    for (d, lm) in self.content_manager.cmc_hrdps_hourly_load():
      loading_msg = lm
      data = d

    hrdps_data['temperature'] = list(filter(filter_future_only, data['temperature']))
    hrdps_data['humidity'] = list(filter(filter_future_only, data['humidity']))
    hrdps_data['wind'] = list(filter(filter_future_only, data['wind']))
    hrdps_data['precipitation'] = list(filter(filter_future_only, data['precipitation']))

    for (d, lm) in self.content_manager.current():
      loading_msg = lm
      current_data = d

    loading_msg = 'Up to date'
    updated_data = True
