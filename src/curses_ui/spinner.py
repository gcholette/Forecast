
class Spinner:
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