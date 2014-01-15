# -*- coding: utf-8 -*-  
from lxml import etree

root = etree.Element("root")
#  xml  use tag to get
print root.tag 
#element is the cell of the xml tree
root.append(etree.Element("child1"))
#use sub element 
child2 = etree.SubElement(root, "child2")

#use tostring() method to see the XML
print etree.tostring(root, pretty_print=True)

# element is a list
child = root[0]
print child.tag


