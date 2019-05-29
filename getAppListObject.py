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
    obj = {}

    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      access = app.find('accesscontrol')
      cmd = config[3].text

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
            grp = "none"
            if not grp in obj:
              obj[grp] = {
                "ivanti": []
              }
            
            newApp = {
              config[1].text: {
                "folder": config[0].text,
                "enabled": citrix.find('enabled').text,
                "cmd": "",
                "appv": False
              }
            }

            if cmd:
              appv = cmd
              regex = re.search('App-V', appv, flags = re.I)
              regex2 = re.search('appv', appv, flags = re.I)
              print(regex)
            if not cmd:
              newApp[config[1].text]["cmd"] = ""
            else:
              newApp[config[1].text]["cmd"] = cmd
            if regex or regex2:
              newApp[config[1].text]["appv"] = True
            else:
              newApp[config[1].text]["appv"] = False
            obj[grp]["ivanti"].append(newApp)
            continue

          if attr == "group":
            grp = group.text.split('\\').pop()
            if not grp in obj:
              obj[grp] = {
                "ivanti": []
              }
            
            newApp = {
              config[1].text: {
                "folder": config[0].text,
                "enabled": citrix.find('enabled').text,
                "cmd": "",
                "appv": False
              }
            }

            if cmd:
              appv = cmd
              regex = re.search('App-V', appv)
              print(regex)
            if not cmd:
              newApp[config[1].text]["cmd"] = ""
            else:
              newApp[config[1].text]["cmd"] = cmd
            if regex:
              newApp[config[1].text]["appv"] = True
            else:
              newApp[config[1].text]["appv"] = False
            obj[grp]["ivanti"].append(newApp)

    objArr = []
    for key in obj:
      finalObj = {
        key: obj[key]
      }
      objArr.append(finalObj)

    aList.write(json.dumps(objArr, ensure_ascii=False))
    aList.close()

if __name__ == '__main__':
  handler()