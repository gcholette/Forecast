
class Subscribable:
  def __init__(self):
    self.subsribers = []

  def subscribe(self, sub):
      self.subsribers.append(sub)

  def notify_subs(self, *args):
      for sub in self.subsribers:
          sub.notify(*args)

  def unsubscribe(self, sub):
      self.subsribers.remove(sub)