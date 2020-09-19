#!/usr/bin/python
def gettemp(id):
  try:
    mytemp = ''
    if not id.startswith('/sys'): id = '/sys/bus/w1/devices/'+id+'/w1_slave'
    f = open(id, 'r')
    line = f.readline().split() # read 1st line
    if line[-1]=='YES':
      line = f.readline().strip().split('=') # read 2nd line
      mytemp = int(line[-1])
    else:
      mytemp = 99999
    f.close()
    return mytemp
  except:
      return 99999

def getctemp(id):
    return float(gettemp(id)/1000)

def getftemp(id):
    return float("{:.1f}".format(((gettemp(id)/1000) * 9/5) + 32))

if __name__ == '__main__':
    # Script has been called directly
    import glob as g
    for x in g.glob('/sys/bus/w1/devices/10-*/w1_slave'):
        w1dev = x.split('/')[5]
        print(w1dev," Raw Temp: ",gettemp(x),sep='')
        print(w1dev," Temp: ",getctemp(x),"°C",sep='')
        print(w1dev," Temp: ",getftemp(x),"°F",sep='')
