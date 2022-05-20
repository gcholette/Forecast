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
