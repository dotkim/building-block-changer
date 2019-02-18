import xml.etree.ElementTree as ET
from unidecode import unidecode
from os import walk
import re
import copy

def getFiles():
  dataDir = '.\\data\\'                       # set the dir to walk.
  for rootDir, dirs, files in walk(dataDir):  # loop through the files in dataDir.
    return rootDir, files

def parseXML(file):
  enc = ET.XMLParser(encoding='utf-8')
  tree = ET.parse(file, parser=enc)   # parse XML data.
  root = tree.getroot()               # get root of the data.
  return tree, root                   # return both for future use.

def getTemplate():
  file = '.\\template.xml'
  return parseXML(file)

def handler():
  rootDir, files = getFiles()
  if len(files) == 0:
    print('there are no files in data')
    return

  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)
    tempTree, tempRoot = getTemplate()
    
    appList = []
    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      name = re.search('(-$)', config[1].text)
      if name is not None:
        appList.append(config[1].text)
        continue


    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      wControl = app.find('workspacecontrol')
      zone = '{33F35656-6637-49F9-AD5F-C76511552A77}' # intern-o365
      isZone = False

      header = 'Application: ' + config[1].text
      print('Application: ' + config[1].text)
      print('-' * len(header))

      ######## APPLICATION CONTROL ########
      # We need to check a few things before we can work on the application.
      enabled = citrix.find('enabled')  # find the setting "enabled" under citrix in the app.
      if enabled.text == 'no':          # check if the app is not enabled, if so jump to the next app.
        print('app is disabled\n')
        continue

      name = re.search('(_$)', config[1].text)
      if name is None:
        print('Application name is missing "_"', end='\n\n')
        continue

      if wControl is None:
        print('app has no workspaces', end='\n\n')
        continue

      workspace = wControl.findall('workspace')
      if len(workspace) == 0:
        continue

      for ws in workspace:
        print('checking:', ws.text)
        if ws.text == zone:  # check if the workspace is the one we want.
          isZone = True
          
      if isZone == False:
        print('app is in the wrong workspace', end='\n\n')
        continue

      ######## CONFIGURATION ########
      # Here the script is going to configure the application we are in.
      # By checking if the values in a template is the same as the values in the main file.
      print('__ready to configure__')
      template = tempRoot.find('./buildingblock/application')
      tempCon = template.find('configuration')
      tempCtx = template.find('citrix')
      tempCtrl = template.find('workspacecontrol')

      print('copying application...')
      newApp = copy.deepcopy(app)
      root.find('./buildingblock').append(newApp)
      print('changing app name')
      newConfig = newApp.find('configuration')
      newName = re.search('(.*)_$', newConfig[1].text)
      newConfig[1].text = newName.group(1) + '-'
      print('name is changed')
      print('removing appid and guid')
      newApp.remove(newApp.find('appid'))
      newApp.remove(newApp.find('guid'))
      print('removed appid and guid')

      if tempCon is not None:
        print('* checking:', str(tempCon.tag))
        for elem in tempCon.iter():
          if elem.tag != 'configuration':
            if config.find(elem.tag) is None:
              print('creating subelement:', str(elem.tag))
              newElem = ET.SubElement(config, elem.tag)
              if elem.text:
                newElem.text = elem.text
            else:
              print('configuring subelement:', str(elem.tag))
              config.find(elem.tag).text = elem.text

      if tempCtx is not None:
        print('* checking:', str(tempCtx.tag))
        for elem in tempCtx.iter():
          if elem.tag != 'citrix':
            if citrix.find(elem.tag) is None:
              print('creating subelement:', str(elem.tag))
              newElem = ET.SubElement(citrix, elem.tag)
              if elem.text:
                newElem.text = elem.text
            else:
              print('configuring subelement:', str(elem.tag))
              citrix.find(elem.tag).text = elem.text
      
      if tempCtrl is not None:
        print('* reconfiguring:', tempCtrl.tag)
        wControl.clear()
        for elem in tempCtrl.findall('workspace'):
          print('creating subelement:', str(elem.tag), elem.text)
          newElem = ET.SubElement(wControl, elem.tag)
          if elem.text:
            newElem.text = elem.text
      print('__Application is configured__')
      print('-' * len('__Application is configured__'), end='\n\n')

    print('creating file:', str(file))
    tree.write('./output/' + file, encoding="UTF-8", method="xml")
    print('file created, check output folder')

if __name__ == '__main__':
  handler()