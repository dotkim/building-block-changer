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
      printer = app.find('printer')
      comment = app.find('comment')
      location = app.find('location')

      if (printer.text):
        output += printer.text + ";"
      else:
        output += "No printername;"

      if (comment.text):
        output += comment.text + ";"
      else:
        output += "No comment;"

      if (location.text):
        output += location.text + "\n"
      else:
        output += "No location\n"

  outputFile = openFile("./output_" + file + ".csv")
  outputFile.write("printer;comment;location\n")
  outputFile.write(output)
  outputFile.close()

if __name__ == '__main__':
  handler()