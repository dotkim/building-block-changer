import xml.etree.ElementTree as ET
import re
from os import walk

def getFiles():
  dataDir = '.\\data\\'                       # set the dir to walk.
  for rootDir, dirs, files in walk(dataDir):  # loop through the files in dataDir.
    return rootDir, files

def parseXML(file):
  tree = ET.parse(file)   # parse XML data.
  root = tree.getroot()   # get root of the data.
  return tree, root       # return both for future use.

def openFile(fileName):
  file = open(fileName, 'w+')
  return file

def handler():
  aList = openFile('appList.csv')
  aList.write('folder;application;enabled;cmd;appv\n')

  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)

    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      cmd = config[3].text

      print(cmd)
      if cmd:
        appv = cmd
        regex = re.search('App-V', appv)
        print(regex)

      print('Application: ' + config[1].text)
      aList.write(config[0].text)
      aList.write(";")
      aList.write(config[1].text)
      aList.write(";")
      aList.write(citrix.find('enabled').text)
      aList.write(";")
      if not cmd:
        aList.write('None')
      else:
        aList.write(cmd)
      aList.write(";")
      if regex:
        aList.write('yes')
      else:
        aList.write('no')
      aList.write("\n")
  aList.close()

if __name__ == '__main__':
  handler()