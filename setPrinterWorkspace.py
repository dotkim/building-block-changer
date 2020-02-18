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
  file = open(fileName, 'w+', encoding="UTF-8")
  return file

def handler():

  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    output = ""
    tree, root = parseXML(rootDir+file)

    for app in root.findall('./buildingblock/powerlaunch/printermapping'):
      workspacecontrol = app.find('workspacecontrol')
      workspacecontrol.clear()

      ET.SubElement(workspacecontrol, 'workspace').text = '{868B2F5E-8CE4-44F4-BA04-330B0E96BB72}'
      ET.SubElement(workspacecontrol, 'workspace').text = '{0BAB7235-7F30-445C-A445-1C73A251134E}'

    print('creating file:', str(file))
    tree.write('./output/configured_' + file, encoding="UTF-8", method="xml")
    print('file created, check output folder')


if __name__ == '__main__':
  handler()