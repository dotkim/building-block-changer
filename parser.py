import xml.etree.ElementTree as ET

xmlFile = '.\\data\\start_chrome.xml'

def parseXML(file):
  tree = ET.parse(file)   # parse XML data.
  root = tree.getroot()   # get root of the data
  return tree, root       # return both for future use


def handler():
  tree, root = parseXML(xmlFile)    # call func and put the returned values in vars
  for child in root[1][1][5][1]:    # loop over the root element, 1 1 5 1 is the index for Access Control -> Groups
    print(child.text, child.attrib) # display values

if __name__ == '__main__':
  handler()