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

import numpy as np
def getMedianTiming(timings):
	elements = len(timings)
	n = len(timings[0])
	out = np.zeros(n)
	for data in timings:
		out += np.array(data)
	out /= elements
	return out.tolist()

def graph_data(input_data, prefix, boxplots=True, lineplots=True, meanplot=True):
  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'down', 0))
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_down.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'up', 0))
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_up.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1][u'down']-b[i][u'down'])
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_down-down.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1].get(u'up', 0)-b[i].get(u'up', 0))
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_up-up.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)):
        x.append(b[i].get(u'up',0) - b[i].get(u'down',0))
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    counter += 1
  pyplot.savefig(prefix + '_dwell.png')
  pyplot.clf()

  counter = 0
  for person in input_data:
    attempts = []
    for b in person:
      x = []
      for i in range(len(b)-1):
        x.append(b[i+1].get(u'down',0) - b[i].get(u'up',0))
      if (lineplots):
        pyplot.plot(x, ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
      attempts.append(x[:])
    if (meanplot):
      pyplot.plot(getMedianTiming(attempts), ['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
    if (boxplots):
      errors = zip(*attempts)
      r = pyplot.boxplot(errors[1:])
      pyplot.setp(r['boxes'], color=['b','g','r','c','m','y','k','DarkOrange','CornflowerBlue','Crimson','DarkMagenta', 'DarkOliveGreen'][counter])
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
people = [cavin,evan,peter,joe,luis,matt,tuan, carlo, juan, jordan]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta")
#graph_data(filtered_people[1], "facebookgoogle")
#graph_data(filtered_people[2], "biedenharn")

people = [carlo, cavin]
filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_cavin2")
#graph_data(filtered_people[1], "facebookgoogle_cavin2")
graph_data(filtered_people[2], "biedenharn_cavin", True, False)

#people = [carlo, evan]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_evan")
#graph_data(filtered_people[1], "facebookgoogle_evan")
#graph_data(filtered_people[2], "biedenharn_evan")
#
#people = [carlo, peter]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_peter")
#graph_data(filtered_people[1], "facebookgoogle_peter")
#graph_data(filtered_people[2], "biedenharn_peter")
#
#people = [carlo, joe]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_joe")
#graph_data(filtered_people[1], "facebookgoogle_joe")
#graph_data(filtered_people[2], "biedenharn_joe")
#
#people = [carlo, luis]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_luis")
#graph_data(filtered_people[1], "facebookgoogle_luis")
#graph_data(filtered_people[2], "biedenharn_luis")
#
#people = [carlo, matt]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_matt")
#graph_data(filtered_people[1], "facebookgoogle_matt")
#graph_data(filtered_people[2], "biedenharn_matt")
#
#people = [carlo, tuan]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_tuan")
#graph_data(filtered_people[1], "facebookgoogle_tuan")
#graph_data(filtered_people[2], "biedenharn_tuan")
#
#people = [carlo, juan]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_juan")
#graph_data(filtered_people[1], "facebookgoogle_juan")
#graph_data(filtered_people[2], "biedenharn_juan")
#
#people = [carlo, jordan]
#filtered_people = zip(*map(filter_data, people))
#graph_data(filtered_people[0], "phideltatheta_jordan")
#graph_data(filtered_people[1], "facebookgoogle_jordan")
#graph_data(filtered_people[2], "biedenharn_jordan")
##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####

