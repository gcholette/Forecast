import copy
import curses
from curses.textpad import rectangle
import time
from constants import version
from enum import Enum
from content_manager import ContentManager
from util import int_half, filter_future_only, temperature_color_code
from file_manager import FileManager
import arrow
from cmc import CMC
from constants import rdps_variables
from threading import Thread

TOO_SMALL_BOUNDARY_X = 57
SMALL_BOUNDARY_X = 75 
MEDIUM_BOUNDARY_X = 100 
LARGE_BOUNDARY_X = 150 
X_LARGE_BOUNDARY_X = 250 

empty_hrdps_data = {
  'temperature': [],
  'humidity': [],
  'wind': [],
  'precipitation': []
}

timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374
hrdps_data = copy.deepcopy(empty_hrdps_data)
loading_msg: str = 'Up to date'
updated_data = False

def extract_value(x):
  return (int(x['value']))

def extract_timestamp(x):
  return (arrow.get(x['time']).format('HH'))

class Breakpoints(Enum):
  TOO_SMALL = 1
  SMALL = 2
  MEDIUM = 3
  LARGE = 4
  X_LARGE = 5

spinner_frames_1 = ['_', '/','|', '\\']
spinner_frames_2 = ['_', '_','_', '_', '-','-','-','-']

class CursesSpinner:
  frames: list[str] = []
  curr_symbol: str = ''
  index: int = 0

  def __init__(self, frames) -> None:
    self.frames = frames
    self.curr_symbol = frames[0]
  
  def render(self) -> str:
    return self.curr_symbol
  
  def animate(self) -> None:
    self.index += 1
    if self.index >= len(self.frames):
      self.index = 0

    self.curr_symbol = self.frames[self.index]

  def set_frames(self, frames):
    self.frames = frames

class CursesApp():
  def __init__(self):
    self.spinner = CursesSpinner(spinner_frames_1)
    self.counter: int = 0
    self.content_manager = ContentManager()
    self.pre_t_data = copy.deepcopy(empty_hrdps_data)
    self.data_times = copy.deepcopy(empty_hrdps_data)
    self.data_values = copy.deepcopy(empty_hrdps_data)
    self.widget_hourly_1_scroll = 0

  def init(self, stdscr):
    self.screen = stdscr
    curses.initscr()
    curses.curs_set(False)
    self.active_breakpoints = (Breakpoints.MEDIUM, Breakpoints.MEDIUM)

    (init_y, init_x) = self.screen.getmaxyx()
    self.max_y = init_y
    self.max_x = init_x

    self.refresh_data()
    self.footer = curses.newwin(0, init_x, init_y-2, 0)
    self.widget_hourly_1 = curses.newwin(7, init_x, 0, 0)

    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_CYAN)
    curses.init_pair(9, 160, curses.COLOR_BLACK)
    curses.init_pair(10, 39, curses.COLOR_BLACK)
    curses.init_pair(11, 166, curses.COLOR_BLACK)

    for i in (list(range(25, 194))):
      curses.init_pair(i, curses.COLOR_BLACK, i)

    self.render_loop()

  # Threaded fn
  def use_content_manager(self):
    global hrdps_data
    global loading_msg
    global updated_data 
    loading_msg = 'Loading HRDPS data'

    data = {}
    for (d, lm) in self.content_manager.cmc_hrdps_multi_load():
      loading_msg = lm
      data = d

    hrdps_data['temperature'] = list(filter(filter_future_only, data['temperature']))
    hrdps_data['humidity'] = list(filter(filter_future_only, data['humidity']))
    hrdps_data['wind'] = list(filter(filter_future_only, data['wind']))
    hrdps_data['precipitation'] = list(filter(filter_future_only, data['precipitation']))

    loading_msg = 'Up to date'
    updated_data = True


  def refresh_data(self):
    t = Thread(target=self.use_content_manager)
    t.start()

  def render_loop(self):
    while 1:
      #time.sleep(0.1)

      (max_y, max_x) = self.screen.getmaxyx()
      self.max_y = max_y
      self.max_x = max_x

      self.setBreakpoints()

      if (len(self.pre_t_data['temperature']) == 0 or updated_data):
        self.scroll_pre_t_data()

      if (loading_msg == 'Up to date'):
        self.spinner.set_frames(spinner_frames_2)

      self.spinner.animate()
      self.draw_screen()
      self.counter += 1
      if (self.counter == 800):
        self.refresh_data()
        self.counter = 0

      if not(self.is_window_too_small()):
        self.draw_footer()
        self.draw_widget_hourly_1()

      self.screen.timeout(100)
      self.screen.move(0, 0)

      key_or_event = self.screen.getch()
      if key_or_event == curses.KEY_RIGHT:
        self.widget_hourly_1_scroll += 1
        self.scroll_pre_t_data()

        self.widget_hourly_1.clear()
        self.widget_hourly_1.refresh()
      if key_or_event == curses.KEY_LEFT and self.widget_hourly_1_scroll > 0:
        self.widget_hourly_1_scroll -= 1
        self.scroll_pre_t_data()

        self.widget_hourly_1.clear()
        self.widget_hourly_1.refresh()
      if key_or_event == curses.KEY_RESIZE:
        self.screen.clear()
        self.screen.refresh()
        self.footer.clear()
        self.widget_hourly_1.clear()
      if key_or_event == ord('q'):
        exit(0)
      else:
        curses.echo()
  
  def scroll_pre_t_data(self):
    global updated_data
    self.pre_t_data['temperature'] = []
    for d, i in zip(hrdps_data['temperature'], list(range(0, len(hrdps_data['temperature'])))):
      if i > self.widget_hourly_1_scroll:
        self.pre_t_data['temperature'].append(d)

    self.data_values['temperature'] = list(map(extract_value,self.pre_t_data['temperature']))
    self.data_times['temperature'] = list(map(extract_timestamp,self.pre_t_data['temperature']))
    updated_data = False

  def draw_screen(self):
    if self.is_window_too_small():
      self.screen.addstr(0, 0, f'Terminal is too small.')
      self.screen.addstr(1, 0, f'Please use a wider interface.')

  def draw_widget_hourly_1(self):

    self.widget_hourly_1.attron(curses.color_pair(3))
    self.widget_hourly_1.border()
    self.widget_hourly_1.attroff(curses.color_pair(3))

    if (len(hrdps_data['temperature']) < 1):
      return

    self.widget_hourly_1.addstr(3, 2, 'T°C ', curses.color_pair(11))
    #self.widget_hourly_1.addstr(2, 8 + 8, '~~', curses.color_pair(10))

    for val, time, i in zip(self.data_values['temperature'], self.data_times['temperature'], list(range(0, len(self.data_values['temperature'])))):
      chosen_x = 8 + (i*7)
      chosen_color = curses.color_pair(temperature_color_code(float(val)))
      if (chosen_x + 4 < self.max_x):
        self.widget_hourly_1.addstr(3, 8 + (i*7), f'{str(val).rjust(2,"0").center(4, " ")}', chosen_color)
        self.widget_hourly_1.addstr(1, 8 + (i*7), f' {str(time)} ')

    self.widget_hourly_1.refresh()

  def draw_footer_loop(self):
    while 1:
      time.sleep(0.1)
      self.draw_footer()

  def draw_footer(self):

    if not(self.is_window_too_small()):
      self.footer.mvwin(self.max_y - 3, 0)
      self.footer.resize(3, self.max_x)

      self.footer.attron(curses.color_pair(3))
      self.footer.border()
      self.footer.attroff(curses.color_pair(3))

      self.footer.addstr(1, 2, ' ', curses.color_pair(2))
      self.footer.addstr(1, 4, f'Forecasts v{version}')

      self.footer.addstr(1, self.max_x-3, self.spinner.render())

      half_loading_msg_length = int(len(loading_msg) / 2)
      half_footer_width = int(self.max_x / 2)
      self.footer.addstr(1, half_footer_width - half_loading_msg_length - 5, f'        {loading_msg}         ')
      self.footer.refresh()

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

