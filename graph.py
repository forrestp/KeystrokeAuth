import json
import matplotlib.pyplot as pyplot

carlo = [
'[{"code":172,"down":0,"up":61},{"code":69,"down":70,"up":182},{"code":76,"down":191,"up":263},{"code":76,"down":336,"up":407},{"code":79,"down":480,"up":566},{"code":32,"down":688,"up":807},{"code":87,"down":863,"up":959},{"code":79,"down":975,"up":1063},{"code":82,"down":1071,"up":1142},{"code":76,"down":1183,"up":1287},{"code":68,"down":1256,"up":1350},{"code":16,"down":1446,"up":1686},{"code":49,"down":1543,"up":1662}]',
'[{"code":172,"down":0,"up":39},{"code":69,"down":96,"up":206},{"code":76,"down":200,"up":255},{"code":76,"down":344,"up":430},{"code":79,"down":496,"up":551},{"code":32,"down":680,"up":791},{"code":87,"down":864,"up":966},{"code":79,"down":960,"up":1039},{"code":82,"down":1048,"up":1143},{"code":76,"down":1160,"up":1258},{"code":68,"down":1232,"up":1335},{"code":16,"down":1391,"up":1638},{"code":49,"down":1496,"up":1623}]',
'[{"code":172,"down":0,"up":63},{"code":69,"down":88,"up":191},{"code":76,"down":208,"up":286},{"code":76,"down":367,"up":414},{"code":79,"down":487,"up":582},{"code":32,"down":703,"up":814},{"code":87,"down":895,"up":998},{"code":79,"down":992,"up":1063},{"code":82,"down":1104,"up":1174},{"code":76,"down":1224,"up":1310},{"code":68,"down":1296,"up":1407},{"code":16,"down":1471,"up":1695},{"code":49,"down":1552,"up":1679}]',
'[{"code":172,"down":0,"up":71},{"code":69,"down":112,"up":207},{"code":76,"down":224,"up":279},{"code":76,"down":368,"up":446},{"code":79,"down":503,"up":591},{"code":32,"down":704,"up":815},{"code":87,"down":912,"up":1007},{"code":79,"down":1032,"up":1111},{"code":82,"down":1136,"up":1214},{"code":76,"down":1240,"up":1334},{"code":68,"down":1320,"up":1414},{"code":16,"down":1487,"up":1703},{"code":49,"down":1568,"up":1710}]',
'[{"code":172,"down":0,"up":79},{"code":69,"down":104,"up":230},{"code":76,"down":224,"up":287},{"code":76,"down":352,"up":447},{"code":79,"down":520,"up":607},{"code":32,"down":680,"up":791},{"code":87,"down":824,"up":919},{"code":79,"down":935,"up":1022},{"code":82,"down":1016,"up":1119},{"code":76,"down":1152,"up":1254},{"code":68,"down":1248,"up":1350},{"code":16,"down":1415,"up":1655},{"code":49,"down":1528,"up":1639}]',
'[{"code":172,"down":0,"up":71},{"code":69,"down":96,"up":207},{"code":76,"down":232,"up":287},{"code":76,"down":368,"up":439},{"code":79,"down":520,"up":598},{"code":32,"down":696,"up":799},{"code":87,"down":848,"up":943},{"code":79,"down":951,"up":1038},{"code":82,"down":1032,"up":1127},{"code":76,"down":1168,"up":1270},{"code":68,"down":1247,"up":1351},{"code":16,"down":1439,"up":1630},{"code":49,"down":1512,"up":1623}]',
]

forrest = [
'[{"code":72,"down":0,"up":103},{"code":69,"down":159,"up":247},{"code":76,"down":344,"up":415},{"code":76,"down":496,"up":575},{"code":79,"down":672,"up":783},{"code":32,"down":856,"up":983},{"code":87,"down":1095,"up":1191},{"code":79,"down":1207,"up":1295},{"code":82,"down":1336,"up":1415},{"code":76,"down":1480,"up":1575},{"code":68,"down":1583,"up":1679},{"code":16,"down":1759,"up":2046},{"code":49,"down":1935,"up":2031}]',
'[{"code":72,"down":0,"up":94},{"code":69,"down":144,"up":223},{"code":76,"down":279,"up":351},{"code":76,"down":439,"up":510},{"code":79,"down":615,"up":694},{"code":32,"down":888,"up":990},{"code":87,"down":1135,"up":1214},{"code":79,"down":1264,"up":1358},{"code":82,"down":1384,"up":1470},{"code":76,"down":1511,"up":1621},{"code":68,"down":1607,"up":1710},{"code":16,"down":1783,"up":2061},{"code":49,"down":1951,"up":2054}]',
'[{"code":72,"down":0,"up":103},{"code":69,"down":152,"up":247},{"code":76,"down":336,"up":407},{"code":76,"down":496,"up":575},{"code":79,"down":688,"up":807},{"code":32,"down":1127,"up":1231},{"code":87,"down":1304,"up":1423},{"code":79,"down":1448,"up":1535},{"code":82,"down":1608,"up":1703},{"code":76,"down":1745,"up":1847},{"code":68,"down":1920,"up":2031},{"code":16,"down":2167,"up":2495},{"code":49,"down":2360,"up":2471}]',
'[{"code":72,"down":0,"up":86},{"code":69,"down":119,"up":231},{"code":76,"down":272,"up":367},{"code":76,"down":440,"up":535},{"code":79,"down":624,"up":727},{"code":32,"down":816,"up":927},{"code":87,"down":1200,"up":1303},{"code":79,"down":1352,"up":1447},{"code":82,"down":1488,"up":1575},{"code":76,"down":1624,"up":1742},{"code":68,"down":1736,"up":1831},{"code":16,"down":1903,"up":2182},{"code":49,"down":2056,"up":2174}]',
'[{"code":72,"down":0,"up":87},{"code":69,"down":144,"up":255},{"code":76,"down":304,"up":367},{"code":76,"down":464,"up":535},{"code":79,"down":631,"up":719},{"code":32,"down":823,"up":927},{"code":87,"down":1111,"up":1199},{"code":79,"down":1238,"up":1335},{"code":82,"down":1367,"up":1447},{"code":76,"down":1519,"up":1623},{"code":68,"down":1655,"up":1759},{"code":16,"down":1822,"up":2190},{"code":49,"down":2056,"up":2127}]',
'[{"code":72,"down":0,"up":95},{"code":69,"down":136,"up":231},{"code":76,"down":280,"up":343},{"code":76,"down":432,"up":527},{"code":79,"down":664,"up":759},{"code":32,"down":1183,"up":1287},{"code":87,"down":1376,"up":1471},{"code":79,"down":1520,"up":1615},{"code":82,"down":1632,"up":1727},{"code":76,"down":1800,"up":1898},{"code":68,"down":1896,"up":1999},{"code":16,"down":2054,"up":2319},{"code":49,"down":2216,"up":2303}]',
'[{"code":72,"down":0,"up":88},{"code":69,"down":137,"up":232},{"code":76,"down":297,"up":376},{"code":76,"down":473,"up":553},{"code":79,"down":648,"up":752},{"code":32,"down":1313,"up":1423},{"code":87,"down":1513,"up":1624},{"code":79,"down":1640,"up":1728},{"code":82,"down":1760,"up":1840},{"code":76,"down":1920,"up":2022},{"code":68,"down":2015,"up":2112},{"code":16,"down":2183,"up":2431},{"code":49,"down":2336,"up":2423}]',
'[{"code":72,"down":0,"up":86},{"code":69,"down":103,"up":214},{"code":76,"down":255,"up":335},{"code":76,"down":431,"up":526},{"code":79,"down":615,"up":718},{"code":32,"down":951,"up":1063},{"code":87,"down":1206,"up":1294},{"code":79,"down":1343,"up":1421},{"code":82,"down":1438,"up":1527},{"code":76,"down":1584,"up":1693},{"code":68,"down":1688,"up":1766},{"code":16,"down":1837,"up":2085},{"code":49,"down":1990,"up":2078}]',
]

def graph_passwords(a, filename):
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
    b=json.loads(b)
    x = []
    temp_sum = 0
    for i in range(len(b)):
      x.append(b[i].get(u'down', 0))
      temp_sum += b[i]["code"]
    pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
  pyplot.savefig('down' + str(filename) + '.png')
  pyplot.clf()

  for b in a:
    b=json.loads(b)
    x = []
    temp_sum = 0
    for i in range(len(b)):
      x.append(b[i].get(u'up', 0))
      temp_sum += b[i]["code"]
    pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
  pyplot.savefig('up' + str(filename) + '.png')
  pyplot.clf()

  for b in a:
    b=json.loads(b)
    x = []
    temp_sum = 0
    for i in range(len(b)):
      x.append(b[i].get(u'up',0) - b[i].get(u'down',0))
      temp_sum += b[i]["code"]
    pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
  pyplot.savefig('dwell' + str(filename) + '.png')
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
  pyplot.savefig('down_down' + str(filename) + '.png')
  pyplot.clf()

  for b in a:
    b=json.loads(b)
    x = []
    temp_sum = 0
    for i in range(len(b)-1):
      x.append(b[i+1].get(u'up',0)-b[i].get(u'up',0))
      temp_sum += b[i]["code"]
    temp_sum += b[-1]["code"]
    pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
  pyplot.savefig('up_up' + str(filename) + '.png')

  for b in a:
    b=sorted(json.loads(b), key=lambda k: k[u'up'])
    x = []
    temp_sum = 0
    for i in range(len(b)-1):
      x.append(b[i+1].get(u'down',0)-b[i].get(u'up',0))
      temp_sum += b[i]["code"]
    temp_sum += b[-1]["code"]
    pyplot.plot(x, ['b','g','r','c','m','y','k','b','g','r','c','m','y','k'][colors[temp_sum]])
  pyplot.savefig('flight' + str(filename) + '.png')

graph_passwords(forrest + carlo, "forrest_carlo_hw")
