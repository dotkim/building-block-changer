import xml.etree.ElementTree as ET
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

def getTemplate():
  file = '.\\template\\Template.xml'
  return parseXML(file)

def handler():
  rootDir, files = getFiles()
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file)
    tempTree, tempRoot = getTemplate()
    
    for app in root.findall('./buildingblock/application'):
      config = app.find('configuration')
      citrix = app.find('citrix')
      wControl = app.find('workspacecontrol')
      zone = '{E225DEE3-520D-4BBF-A6C6-1D7E2AFBB3A2}'
      isZone = False

      header = 'Application: ' + config[1].text
      print('Application: ' + config[1].text)
      print('-' * len(header))

      ######## APPLICATION CONTROL ########
      # We need to check a few things before we can work on the application.
      # - Check if the application is enabled.
      # - Check if the application has the correct workspace, and only that workspace.
      enabled = citrix.find('enabled')  # find the setting "enabled" under citrix in the app.
      if enabled.text == 'no':          # check if the app is not enabled, if so jump to the next app.
        print('app is disabled\n')
        continue

      if wControl is None:
        print('app has no workspaces\n')
        continue

      workspace = wControl.findall('workspace')
      print(workspace)
      if len(workspace) == 0:
        continue
      if len(workspace) > 1:
        print('Too many workspaces\n')
        continue
      for ws in workspace:
        print('checking: ' + ws.text)
        if ws.text != zone:  # check if the workspace is the one we want.
          print('app is in the wrong workspace\n')
        else:
          isZone = True
      if isZone == False:
        continue

      ######## CONFIGURATION ########
      # Here the script is going to configure the application we are in.
      # By checking if the values in a template is the same as the values in the main file.
      print('__ready to configure__')
      template = tempRoot.find('./buildingblock/application')
      tempCon = template.find('configuration')
      tempCtx = template.find('citrix')
      tempCtrl = template.find('workspacecontrol')

      if tempCon is not None:
        print('* checking:', str(tempCon.tag))
        for elem in tempCon.iter():
          if elem.tag != 'configuration':
            if config.find(elem.tag) is None:
              print('creating subelement:', str(elem.tag), elem.text)
              new = ET.SubElement(config, elem.tag)
              if elem.text:
                new.text = elem.text
            else:
              print('configuring subelement:', str(elem.tag), elem.text)
              config.find(elem.tag).text = elem.text

      if tempCtx is not None:
        print('* checking:', str(tempCtx.tag))
        for elem in tempCtx.iter():
          if elem.tag != 'citrix':
            if citrix.find(elem.tag) is None:
              print('creating subelement:', str(elem.tag), elem.text)
              new = ET.SubElement(citrix, elem.tag)
              if elem.text:
                new.text = elem.text
            else:
              print('configuring subelement:', str(elem.tag), elem.text)
              citrix.find(elem.tag).text = elem.text
      
      if tempCtrl is not None:
        print('* reconfiguring:', tempCtrl.tag)
        wControl.clear()
        for elem in tempCtrl.findall('workspace'):
          print('creating subelement:', str(elem.tag), elem.text)
          new = ET.SubElement(wControl, elem.tag)
          if elem.text:
            new.text = elem.text
      print('__Application is configured__')
      print('-' * len('__Application is configured__'), end='\n\n')

    print('creating file:', str(file))
    tree.write('./output/' + file, encoding="UTF-8", method="xml")
    print('file created, check output folder')

if __name__ == '__main__':
  handler()