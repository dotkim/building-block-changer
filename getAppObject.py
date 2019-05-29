import xml.etree.ElementTree as ET
import re
import json
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
  file = open(fileName, 'w+', encoding='UTF-8')
  return file

def handler():
  aList = openFile('appObj.json')
  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)
    objArr = []

    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      access = app.find('accesscontrol')
      cmd = config[3].text
      groups = []

      print('Application: ' + config[1].text)
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
            grp = group.text.split('\\').pop()
            groups.append(grp)

      obj = {
        "name": config[1].text,
        "src": "Ivanti",
        "data": {
          "folder": config[0].text,
          "enabled": citrix.find('enabled').text,
          "cmd": "",
          "appv": False,
          "groups": groups
        }
      }
      
      if cmd:
        appv = cmd
        regex = re.search('App-V', appv)
        print(regex)
      if not cmd:
        obj["data"]["cmd"] = ""
      else:
        obj["data"]["cmd"] = cmd
      if regex:
        obj["data"]["appv"] = True
      objArr.append(obj)

    aList.write(json.dumps(objArr, ensure_ascii=False))
    aList.close()

if __name__ == '__main__':
  handler()