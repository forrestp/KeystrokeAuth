import json
import matplotlib.pyplot as pyplot

def filter_data(input_data):
  counter = 0
  phidelt = []
  fbgoogl = []
  biedenh = []
  for b in input_data:
    b = json.loads(b)
    temp_sum = 0
    for i in range(len(b)):
      temp_sum += b[i]["code"]
    if temp_sum == 961:
      phidelt.append(b)
    elif temp_sum == 1015:
      fbgoogl.append(b)
    elif temp_sum == 720:
      biedenh.append(b)
  return [phidelt, fbgoogl, biedenh]

def graph_data(input_data, prefix):
  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'down', 0))
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_down.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'up', 0))
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_up.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1][u'down']-b[i][u'down'])
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_down-down.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1].get(u'up', 0)-b[i].get(u'up', 0))
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_up-up.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'up',0) - b[i].get(u'down',0))
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_dwell.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1].get(u'down',0) - b[i].get(u'up',0))
      pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_flight.png')
  pyplot.clf()

##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

# This is a selection of people that had to type three phrases 5-10 times.
# The phrases are:
#   phideltatheta
#   facebookgoogle
#   biedenharn
# The phrases were chosen because one is common for a small group of people to
# type, one is common for many people to type, and one is common for only a few
# people to type.

from more_data import *
people = [cavin,justin,evan,peter,joe,luis,matt,tuan, carlo]
filtered_people = zip(*map(filter_data, people))
graph_data(filtered_people[0], "phideltatheta")
graph_data(filtered_people[1], "facebookgoogle")
graph_data(filtered_people[2], "biedenharn")

##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

