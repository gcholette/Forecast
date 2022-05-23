import sys
import old_script
from content_manager import ContentManager
from util import  str_in_list
from curses import wrapper
from curses_ui.curses_app import CursesApp

def fullscreen_app():
  app = CursesApp()
  wrapper(app.init)

def main():
  if str_in_list('--old-script', sys.argv):
    # keeping this for reference
    old_script.run_prediction()
  elif str_in_list('--test-stuff', sys.argv):
    print(ContentManager().current())
  else:
    fullscreen_app()

if __name__ == "__main__":
  main()
