from sty import fg, bg

def cprint(col, txt, end = ''):
  print(col + txt + fg.rs, end)

def reorderData(xs, N, M):
  n = int(M / N)
  indexes = []
  for I in list(range(0, n)):
    for i in list(range(0, N)):
      indexes.append(int((i * n) + I))

  reordered = list(range(0, M))
  for j, i in zip(indexes, range(0, len(indexes))):
    reordered[i] = xs[j]
  return reordered