from signal import signal, SIGWINCH
import curses
from curses.textpad import rectangle
import time
from constants import version
from enum import Enum
from util import int_half
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

timezone = 'America/New_York'
lat = 45.536325
lon = -73.491374
global_data = []
loading_msg: str = 'Up to date'

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
    self.data_times: list[str] = []
    self.data_values: list[str] = []

  def refresh_data(self):
    t = Thread(target=self.get_hrdps, args=(lat, lon, rdps_variables["temperature"]))
    t.start()

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
    self.widget_hourly_1 = curses.newwin(14, init_x, 0, 0)
    self.widget_hourly_1_pad = curses.newpad(12, 150)

    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, 160)
    curses.init_pair(5, curses.COLOR_BLACK, 161)
    curses.init_pair(6, curses.COLOR_BLACK, 162)
    curses.init_pair(7, curses.COLOR_BLACK, 163)
    curses.init_pair(8, curses.COLOR_BLACK, 164)
    curses.init_pair(9, 160, curses.COLOR_BLACK)

    self.render_loop()

  def render_loop(self):
    while 1:
      #time.sleep(0.1)

      (max_y, max_x) = self.screen.getmaxyx()
      self.max_y = max_y
      self.max_x = max_x

      self.setBreakpoints()

      self.data_values = list(map(extract_value,global_data))
      self.data_times = list(map(extract_timestamp,global_data))

      if (loading_msg == 'Up to date'):
        self.spinner.set_frames(spinner_frames_2)

      self.spinner.animate()
      self.draw_screen()
      self.counter += 1
      if (self.counter == 1000):
        self.refresh_data()
        self.counter = 0

      if not(self.is_window_too_small()):
        self.draw_footer()
        self.draw_widget_hourly_1()

      self.screen.timeout(100)
      self.screen.move(0, 0)

      key_or_event = self.screen.getch()
      if key_or_event == curses.KEY_RESIZE:
        self.screen.clear()
        self.screen.refresh()
        self.footer.clear()
        self.widget_hourly_1.clear()
      if key_or_event == ord('q'):
        exit(0)
      else:
        curses.echo()

  def draw_screen(self):
    if self.is_window_too_small():
      self.screen.addstr(0, 0, f'Terminal is too small.')
      self.screen.addstr(1, 0, f'Please use a wider interface.')

  def draw_widget_hourly_1(self):

    self.widget_hourly_1.attron(curses.color_pair(3))
    self.widget_hourly_1.border()
    self.widget_hourly_1.attroff(curses.color_pair(3))

    mock_values = ['15', '16', '17', '18','19','20','21','22','23']
    time_values = ['08', '09', '10', '11','12','13','14','15','16']

    self.widget_hourly_1.addstr(3, 2, 'T°C ', curses.color_pair(9))

    for val, time, i in zip(self.data_values, self.data_times, list(range(0, len(self.data_values)))):
      chosen_x = 8 + (i*7)
      chosen_color = curses.color_pair(5) if int(val) < 17 else ( curses.color_pair(7) if (int(val) < 20) else curses.color_pair(8))
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


  def get_hrdps(self, lat, lon, variables):
    global loading_msg
    global global_data
    loading_msg = 'Initiating HRDPS analysis'

    cmc_type = 'hrdps'
    hours = 48
    resolution = 'ps2.5km'
    domain = 'east'
    now = arrow.utcnow().to('-04:00').format('YYYYMMDD')
    run_hour = CMC.calculate_run_start(cmc_type)
    json_filename = ('hrdps_local_%s_%s_%s_%s_%s' % (now, variables[0],lat,lon, run_hour))
    hrdps_cmc = CMC(cmc_type, domain, resolution, variables, run_hour, hours)
    data = []

    if (not FileManager.json_file_exists(cmc_type, json_filename)):
      filenames = hrdps_cmc.generate_filename_list()
      loading_msg = "Fetching HRDPS files"
      urls = hrdps_cmc.generate_url_list()
      loading_msg = "Loading HRDPS data"
      hrdps_cmc.fetch_files(urls, filenames)
      data = hrdps_cmc.load_grib_from_files(lat, lon, filenames)
      FileManager.save_json('hrdps', json_filename, data)
    else:
      data = FileManager.open_json_file(cmc_type, json_filename)
    

    loading_msg = 'Up to date'
    global_data = list(filter(post_filtering, data))


def post_filtering(entry):
  time = arrow.utcnow().to('America/New_York')
  time2 = arrow.get(entry['time']).to('America/New_York')
  diff = time < time2
  return diff
