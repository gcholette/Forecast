
import arrow
from constants import active_variable_names
from util import in_between_data, minute_diff_percent

format = 'YYYY-MM-DD HH:00:00ZZ'

class CurrentForecast:
  def __init__(self, hourly_data = []):
    self.hourly_data = hourly_data
    self.now = arrow.utcnow().to('-04:00').format('YYYY-MM-DD HH:00:00ZZ')
    self.now_with_mins = arrow.utcnow().to('-04:00').format('YYYY-MM-DD HH:mm:ssZZ')
    self.next_hour = arrow.get(arrow.utcnow().shift(hours=+1).to('-04:00').format('YYYY-MM-DD HH:00:00ZZ')).format(format)
    self.progression_percent = minute_diff_percent(arrow.get(self.now_with_mins), arrow.get(self.next_hour))

  @staticmethod
  def get_empty():
    current_data = {
      'time': ''
    }
    for var_name in active_variable_names:
      current_data[var_name] = ''
      current_data[var_name + '_variation'] = ''
    return current_data

  def set_hourly_data(self, data):
    self.hourly_data = data

  def get(self):
    (now_data, next_hour_data) = self.join_now_next_hour_raw()

    current_data = self.get_empty()
    current_data['time'] = self.now_with_mins

    for var_name in active_variable_names:
      x = in_between_data(next_hour_data[var_name]['value'], now_data[var_name]['value'], self.progression_percent)
      diff = next_hour_data[var_name]['value'] - now_data[var_name]['value']
      current_data[var_name] = round(x, 2)
      current_data[f'{var_name}_variation'] = round(diff, 2)

    return (current_data, 'Up to date')

  def join_now_next_hour_raw(self):
    data = self.hourly_data
    first_list = data[active_variable_names[0]]
    (now_data, next_hour_data) = ({}, {})
    for (x, i) in zip(first_list, range(0, len(first_list)-1)):
      if (x['time'] == self.now):
        for var_name in active_variable_names:
          now_data[var_name] = data[var_name][i]
      elif (x['time'] == self.next_hour):
        for var_name in active_variable_names:
          next_hour_data[var_name] = data[var_name][i]
    
    return (now_data, next_hour_data)