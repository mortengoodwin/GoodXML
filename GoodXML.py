import sys
from xml.dom import minidom

#      Copyright 2008-2012 Mortn Goodwin
#      This program is distributed under the terms of the GNU General
#      Public License.
#
#  This file is part of the GoodXML
#
#  GoodXML is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  GoodXML is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with GoodXML; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
#  MA 02110-1301 USA


def isFloat(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

class GoodParser:
   """ Simple XML DOM Parser transforming XML into a pythonic class structure """
   def __init__(self,filename='',content='',element=None):
      self.haschild = False
      if filename:
          self.xmldoc = minidom.parse(filename)
      elif content:
          self.xmldoc = minidom.parseString(content)
      else:
          self.xmldoc = element
      self.content = ''
      if self.xmldoc.hasChildNodes():
          try:
              self.content = self.xmldoc.firstChild.wholeText
          except AttributeError:
              self.content = ''
          if isFloat(self.content):
              self.content = float(self.content)

          for nodeName in set([i.nodeName for i in self.xmldoc.childNodes if not i.nodeName=='#text']):
              if nodeName=='#comment':
                  continue
              if len([i for i in self.xmldoc.childNodes if i.nodeName==nodeName])>1:
                  tempList = [GoodParser(element=i) for i in self.xmldoc.childNodes if i.nodeName==nodeName]
                  exec('self.'+nodeName+' = tempList')
                  self.haschild = True
              else:
                  tempList = [GoodParser(element=i) for i in self.xmldoc.childNodes if i.nodeName==nodeName]
                  if (type(tempList[0].content)==type(0.0) or tempList[0].content) and not tempList[0].haschild:
                      exec('self.'+nodeName+' = tempList[0].content')
                  else:
                      exec('self.'+nodeName+' = tempList[0]')
                  self.haschild = True

if __name__ == '__main__':
    kommuner = GoodParser(content=open('kommuner.xml').read())
    #print kommuner.Kommuner.kommune[0].kommunenavn
    vendors = [i.portal for i in kommuner.Kommuner.kommune]
    for vendor in set(vendors):
        print vendor,vendors.count(vendor)
