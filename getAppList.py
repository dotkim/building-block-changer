import xml.etree.ElementTree as ET
import re
from os import walk

def getFiles():
  dataDir = '.\\data\\'                       # set the dir to walk.
  for rootDir, dirs, files in walk(dataDir):  # loop through the files in dataDir.
    return rootDir, files

def parseXML(file):
  enc = ET.XMLParser(encoding='utf-8')  # create a new parser to set encoding
  tree = ET.parse(file, parser=enc)     # parse XML data using the encoder
  root = tree.getroot()   # get root of the data.
  return tree, root       # return both for future use.

def openFile(fileName):
  file = open(fileName, 'w+', encoding="UTF-8")
  return file

def handler():
  aList = openFile('appList.csv')
  aList.write('folder;application;enabled;cmd;parameters;appv;group\n')

  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)

    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      access = app.find('accesscontrol')
      cmd = config[3].text
      parameters = config[5].text

      groupArr = []
      if access.find("grouplist") is None:
        continue
      else:
        for group in access.find("grouplist"):
          try:
            attr = group.attrib["type"]
          except:
            continue
          if attr is None:
            continue
          if attr == "group":
            groupArr.append(group.text)
      groupStr = ', '.join(groupArr)

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
      if not parameters:
        aList.write('None')
      else:
        aList.write(parameters)
      aList.write(";")
      if regex:
        aList.write('yes')
      else:
        aList.write('no')
      aList.write(";")
      aList.write(groupStr)
      aList.write("\n")
  aList.close()

if __name__ == '__main__':
  handler()