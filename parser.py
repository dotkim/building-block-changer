import xml.etree.ElementTree as ET, os
from unidecode import unidecode
from os import walk


def getFiles():
  dataDir = '.\\data\\'                       # set the dir to walk.
  for rootDir, dirs, files in walk(dataDir):  # loop through the files in dataDir.
    return rootDir, files

def parseXML(file):
  tree = ET.parse(file)   # parse XML data.
  root = tree.getroot()   # get root of the data.
  return tree, root       # return both for future use.

def handler():
  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)
    for citrix in root.iter('citrix'):                # get the citrix element
      if citrix.find('instantpassthru') is None:      
        ET.SubElement(citrix, 'instantpassthru')
        citrix.find('instantpassthru').text = 'yes'
      else:
        citrix.find('instantpassthru').text = 'yes'
      if citrix.find('ipt_http') is None:
        ET.SubElement(citrix, 'ipt_http')
        citrix.find('ipt_http').text = 'no'
      if citrix.find('ipt_auth') is None:
        ET.SubElement(citrix, 'ipt_auth')
        citrix.find('ipt_auth').text = 'citrix'
      if citrix.find('ipt_customica') is None:
        ET.SubElement(citrix, 'ipt_customica')
        citrix.find('ipt_customica').text = 'no'
      if citrix.find('ipt_type') is None:
        ET.SubElement(citrix, 'ipt_type')
        citrix.find('ipt_type').text = 'PNA'
      if citrix.find('ipt_appset') is None:
        ET.SubElement(citrix, 'ipt_appset')
      if citrix.find('ipt_farmname') is None:
        ET.SubElement(citrix, 'ipt_farmname')
      if citrix.find('checklocalapp') is None:
        ET.SubElement(citrix, 'checklocalapp')
        citrix.find('checklocalapp').text = 'no'
      if citrix.find('passthroughanyway') is None:
        ET.SubElement(citrix, 'passthroughanyway')
        citrix.find('passthroughanyway').text = 'no'
      if citrix.find('passthroughinzones') is None:
        ET.SubElement(citrix, 'passthroughinzones')
        citrix.find('passthroughinzones').text = 'yes'
      if citrix.find('passthrough_zones') is None:
        ET.SubElement(citrix, 'passthrough_zones')

    for workspacecontrol in root.iter('workspacecontrol'):
      workspacecontrol.clear()
      workspaces = ['{E225DEE3-520D-4BBF-A6C6-1D7E2AFBB3A2}', '{6A932A4B-0B01-4B44-9D1C-86FE943AB7B5}', '{24EC5C01-9F77-4AF4-BF34-3BC9C60E28CC}']
      for wspace in workspaces:
        new = ET.SubElement(workspacecontrol, 'workspace')
        new.text = wspace

    for child in root.iter('buildingblock'):
      if child.find('workspaces') is None:
        break
      else:
        subEle = child.find('workspaces')
        child.remove(subEle)

    tree.write('./output/' + file, encoding="UTF-8", method="xml")  # write the changed tree to a new file.

if __name__ == '__main__':
  handler()