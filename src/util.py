from sty import fg, bg

def cprint(col, txt, end = ''):
  print(col + txt + fg.rs, end)

