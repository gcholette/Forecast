import sys
from threading import Thread
import old_script
from util import  str_in_list
from curses import wrapper
from curses_ui.curses_app import CursesApp
from services.file_manager import FileManager
from services.aggregator import Aggregator
from constants import lat, lon

aggregator = Aggregator(lat, lon)

def run_aggregator():
  t = Thread(target=aggregator.execution_loop, daemon=True)
  t.start()

def fullscreen_app():
  app = CursesApp(aggregator)
  run_aggregator()

  wrapper(app.init)

def main():
  if str_in_list('--old-script', sys.argv):
    # keeping this for reference
    old_script.run_prediction()
  elif str_in_list('--test-stuff', sys.argv):
    pass
  else:
    fullscreen_app()

if __name__ == "__main__":
  main()
