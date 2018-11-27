import xml.etree.ElementTree as ET, os
from unidecode import unidecode
from os import walk


def getFiles():
  dataDir = '.\\data'         # set the dir to walk
  for files in walk(dataDir): # loop through the files in dataDir
    return files

def parseXML(file):
  tree = ET.parse(file)   # parse XML data.
  root = tree.getroot()   # get root of the data
  return tree, root       # return both for future use

def handler():
  files = getFiles()
  for file in files:
    tree, root = parseXML(file)                       # call func and put the returned values in vars
    for child in root.iter('group'):                  # iterate the tree root and find "group"
      child.text = str(unidecode(child.text))         # turn the string into a normalized string, explicitly cast as str so there wont be errors.

    tree.write(file, encoding="UTF-8", method="xml")  # write the changed tree to a new file

if __name__ == '__main__':
  handler()