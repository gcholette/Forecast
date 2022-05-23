
import arrow
from constants import hrdps_matching_type_str

class HrdpsEntry:
  @staticmethod
  def parse(entry: dict, run_hour: str) -> dict:
    return {
     'time': HrdpsEntry.parse_hrdps_time(entry, run_hour),
     'value': HrdpsEntry.parse_hrdps_value(entry),
     'type': HrdpsEntry.parse_hrdps_type(entry)
    }

  @staticmethod
  def parse_hrdps_time(entry: dict, run_hour: str) -> str:
    return arrow.get(entry['time']).to('America/New_York').shift(hours=int(run_hour)).format()

  @staticmethod
  def parse_hrdps_type(entry: dict) -> str:
    for (var_name, matching_str) in hrdps_matching_type_str:
      if (matching_str in entry['type']):
        return var_name

  @staticmethod
  def parse_hrdps_value(entry: dict) -> float | str:
    entry_type = HrdpsEntry.parse_hrdps_type(entry)
    entry_value = entry['value']
    match entry_type:
      case 'temperature':
        return round(entry_value - 273.15, 2)
      case 'wind':
        return round(entry_value * 3.6, 2)
      case 'humidity':
        return round(entry_value * 10000, 2)
      case 'precipitation':
        return round(entry_value, 2)
      case 'default':
        return entry_value