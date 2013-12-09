import json
import matplotlib.pyplot as pyplot

a = [ '[{"code":72,"down":0,"up":144},{"code":69,"down":152,"up":256},{"code":76,"down":320,"up":424},{"code":76,"down":496,"up":616},{"code":79,"down":696,"up":848}]',
'[{"code":72,"down":0,"up":144},{"code":69,"down":176,"up":280},{"code":76,"down":320,"up":424},{"code":76,"down":496,"up":608},{"code":79,"down":696,"up":824}]',
'[{"code":72,"down":0,"up":144},{"code":69,"down":176,"up":272},{"code":76,"down":320,"up":432},{"code":76,"down":504,"up":600},{"code":79,"down":696,"up":824}]',
'[{"code":72,"down":0,"up":136},{"code":69,"down":160,"up":256},{"code":76,"down":320,"up":424},{"code":76,"down":504,"up":608},{"code":79,"down":696,"up":840}]',
'[{"code":72,"down":0,"up":120},{"code":69,"down":144,"up":272},{"code":76,"down":296,"up":408},{"code":76,"down":472,"up":584},{"code":79,"down":952,"up":1056}]',
'[{"code":72,"down":0,"up":136},{"code":69,"down":156,"up":284},{"code":76,"down":312,"up":412},{"code":76,"down":488,"up":600},{"code":79,"down":684,"up":820}]',
'[{"code":72,"down":0,"up":144},{"code":69,"down":148,"up":288},{"code":76,"down":312,"up":424},{"code":76,"down":488,"up":600},{"code":79,"down":688,"up":824}]',

]





counter = 0
colors = {}
for b in a:
  b = json.loads(b)
  temp_sum = 0
  for i in range(len(b)):
    temp_sum += b[i]["code"]
  if not (temp_sum in colors):
    colors[temp_sum] = counter
    counter += 1
  print temp_sum
print colors

for b in a:
  pyplot.plot([x.get(u'down',0) for x in json.loads(b)])
pyplot.savefig('down.png')
pyplot.clf()

for b in a:
  pyplot.plot([x.get(u'up',0) for x in json.loads(b)])
pyplot.savefig('up.png')
pyplot.clf()

for b in a:
  pyplot.plot([x.get(u'up',0) - x.get(u'down',0) for x in json.loads(b)])
pyplot.savefig('dwell.png')
pyplot.clf()

for b in a:
  b=json.loads(b)
  x = []
  temp_sum = 0
  for i in range(len(b)-1):
    x.append(b[i+1][u'down']-b[i][u'down'])
    temp_sum += b[i]["code"]
  temp_sum += b[-1]["code"]
  pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
pyplot.savefig('down_down.png')
pyplot.clf()

for b in a:
  b=json.loads(b)
  x = []
  for i in range(len(b)-1):
    x.append(b[i+1].get(u'up',0)-b[i].get(u'up',0))
  pyplot.plot(x)
pyplot.savefig('up_up.png')
