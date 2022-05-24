from abc import ABC, abstractmethod
import arrow
from sty import fg, bg

def cprint(col, txt, end = ''):
  print(col + txt + fg.rs, end)

def reorder_data(xs, N, M):
  n = int(M / N)
  indexes = []
  for I in list(range(0, n)):
    for i in list(range(0, N)):
      indexes.append(int((i * n) + I))

  reordered = list(range(0, M))
  for j, i in zip(indexes, range(0, len(indexes))):
    reordered[i] = xs[j]
  return reordered

def str_in_list(x: str, xs: list[str]) -> bool:
  for i in xs:
    if x == i:
      return True
  return False

def int_half(x):
  return int((x / 2) - 1)

def in_between_data(x, y, percent):
  return x + ((y - x) * percent)

def minute_diff_percent(x, y):
    diff = y - x
    _,remainder = divmod(diff.seconds, 3600)
    minutes,_ = divmod(remainder, 60)
    return minutes / 60

def filter_future_only(entry):
  time = arrow.utcnow().to('America/New_York').shift(hours=-2)
  time2 = arrow.get(entry['time']).to('America/New_York')
  diff = time < time2
  return diff

def temperature_color_code(temperature: float) -> int:
  if temperature <= 15:
    return 51
  if temperature <= 18:
    return 49
  if temperature <= 20:
    return 46
  if temperature <= 22:
    return 82
  if temperature <= 24:
    return 118
  if temperature <= 26:
    return 154
  if temperature <= 28:
    return 190
  if temperature <= 30:
    return 178
  if temperature <= 32:
    return 166
  else:
    return 167

def extract_value(x):
  return (int(x['value']))

def extract_timestamp(x):
  return (arrow.get(x['time']).format('HH'))
