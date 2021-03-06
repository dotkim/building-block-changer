# This script is used to copy specific application from a build-block
# currently it is totally useless for anything other than what it was created for
# When ran, this script creates an output of everything it does in a readerfriendly format
# run it with out-file for an easy log

import xml.etree.ElementTree as ET
from unidecode import unidecode
from os import walk
import re
import copy

def getFiles():
  dataDir = '.\\data\\'                       # set the dir to walk
  for rootDir, dirs, files in walk(dataDir):  # loop through the files in dataDir
    return rootDir, files                     # only return the root dir and the files in it, we only want the files in the data dir

def parseXML(file):
  enc = ET.XMLParser(encoding='utf-8')  # create a new parser to set encoding
  tree = ET.parse(file, parser=enc)     # parse XML data using the encoder
  root = tree.getroot()                 # get root of the data
  return tree, root                     # return both for future use

def getTemplate():
  # this function parses the template file if it is present
  # this is if we are adding any elements to the xml
  file = '.\\template.xml'
  return parseXML(file)

def handler():
  # get the files we are working on
  # just return if there are no files
  rootDir, files = getFiles()
  if len(files) == 0:
    print('there are no files in data')
    return

  # start working on file(s) here
  # first we loop over the files to independently work on each file.
  print(files)
  for file in files:
    print(file)
    tree, root = parseXML(rootDir+file) # call the parsexml function and give it the file and rootdir
    tempTree, tempRoot = getTemplate()  # also get the template so we can use it later on

    # find every element with the tag "application"
    # then loop over each one to find the applications we are looking for
    for app in root.findall('./buildingblock/application'):
      # create variables for settings under the application
      config = app.find('configuration')
      citrix = app.find('citrix')
      wControl = app.find('workspacecontrol')
      zone = '{33F35656-6637-49F9-AD5F-C76511552A77}' # intern-o365, this is the workspace container we are looking for
      isZone = False  # this is a check for if we find the container

      # check if the application we are on are the root application, there is no config for this one
      # the script fails if these applications gets past this point
      if app[1].text == '{E72C877D-6A29-4807-B81C-BE404DD2FBB7}' or app[1].text == '{5F9939BD-727A-4C2C-BA6C-163A678A2377}':
        print('root app, stopping')
        continue

      header = 'Application: ' + config[1].text # create header for the application
      print('Application: ' + config[1].text)   # print the header
      print('-' * len(header))

      ######## APPLICATION CONTROL ########
      # We need to check a few things before we can work on the application
      enabled = citrix.find('enabled')  # find the setting "enabled" under citrix in the app
      if enabled.text == 'no':          # check if the app is not enabled, if so jump to the next app
        print('app is disabled\n')
        continue

      # since we are looking for applications with "_" at the end of the name
      # we just use regex for finding it
      # skip to next if it doesnt find the underscore
      name = re.search('(_$)', config[1].text)
      if name is None:
        print('Application name is missing "_"', end='\n\n')
        continue

      # check if the app has workspaces
      if wControl is None:
        print('app has no workspaces', end='\n\n')
        continue

      # check if workspaces length is 0, skip if so
      workspace = wControl.findall('workspace')
      if len(workspace) == 0:
        continue

      # loop over workspaces, there can be more than one
      for ws in workspace:
        print('checking:', ws.text)
        if ws.text == zone:  # check if the workspace is the one we want
          isZone = True
      
      # this only passes if isZone is true
      if isZone == False:
        print('app is in the wrong workspace', end='\n\n')
        continue


      ######## CONFIGURATION ########
      # Here the script is going to copy and configure the application we are in.
      # By checking if the values in a template is the same as the values in the main file.
      print('__ready to configure__')
      template = tempRoot.find('./buildingblock/application')
      tempCon = template.find('configuration')
      tempCtx = template.find('citrix')
      tempCtrl = template.find('workspacecontrol')
      tempSrvGroups = template.find('citrix/servergroups')

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

      newCon = newApp.find('configuration')
      newCtx = newApp.find('citrix')
      newCtrl = newApp.find('workspacecontrol')
      newSrvGroup = newApp.find('citrix/servergroups')

      if tempCon is not None:
        print('* checking:', str(tempCon.tag))
        for elem in tempCon.iter():
          if elem.tag != 'configuration':
            if newCon.find(elem.tag) is None:
              print('creating subelement:', str(elem.tag))
              newElem = ET.SubElement(newCon, elem.tag)
              if elem.text:
                newElem.text = elem.text
            else:
              print('configuring subelement:', str(elem.tag))
              newCon.find(elem.tag).text = elem.text

#      if tempCtx is not None:
#        print('* checking:', str(tempCtx.tag))
#        for elem in tempCtx.iter():
#          if elem.tag != 'citrix' or elem.tag != 'servergroups':
#            if newCtx.find(elem.tag) is None:
#              print('creating subelement:', str(elem.tag))
#              newElem = ET.SubElement(newCtx, elem.tag)
#              if elem.text:
#                newElem.text = elem.text
#            else:
#              print('configuring subelement:', str(elem.tag))
#              newCtx.find(elem.tag).text = elem.text

      if tempSrvGroups is not None:
        print('* reconfiguring:', tempSrvGroups.tag)
        newSrvGroup.clear()
        for elem in tempSrvGroups.findall('servergroup'):
          print('creating subelement:', str(elem.tag), elem.text)
          newElem = ET.SubElement(newSrvGroup, elem.tag, attrib=elem.attrib)
          if elem.text:
            newElem.text = elem.text
      
      if tempCtrl is not None:
        print('* reconfiguring:', tempCtrl.tag)
        newCtrl.clear()
        for elem in tempCtrl.findall('workspace'):
          print('creating subelement:', str(elem.tag), elem.text)
          newElem = ET.SubElement(newCtrl, elem.tag)
          if elem.text:
            newElem.text = elem.text
      print('__Application is configured__')
      print('-' * len('__Application is configured__'), end='\n\n')

    print('creating file:', str(file))
    tree.write('./output/configured_' + file, encoding="UTF-8", method="xml")
    print('file created, check output folder')

if __name__ == '__main__':
  handler()