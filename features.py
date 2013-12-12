''' The various four features/metrics we use for comparison.'''
def down(data):
  if (isinstance(data[0], list)):
    return map(down, data)
  else:
    return [d.get('down',0) for d in data]

def dwell(data):
  if (isinstance(data[0], list)):
    return map(dwell, data)
  else:
    return [d.get('up',0) - d.get('down',0) for d in data]

def flight(data):
  if (isinstance(data[0], list)):
    return map(flight, data)
  else:
    return [data[i+1].get('down',0) - data[i].get('up',0) for i in range(len(data)-1)]

def down_down(data):
  if (isinstance(data[0], list)):
    return map(down_down, data)
  else:
    return [data[i+1].get('down',0) - data[i].get('down',0) for i in range(len(data)-1)]

