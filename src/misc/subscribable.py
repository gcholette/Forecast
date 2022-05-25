
class Subscribable:
  def __init__(self):
    self.subscribers = []

  def subscribe(self, sub):
      self.subscribers.append(sub)

  def notify_subs(self, *args):
      for sub in self.subscribers:
          sub.notify(*args)

  def unsubscribe(self, sub):
      self.subscribers.remove(sub)