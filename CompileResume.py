from Cheetah.Template import Template
from optparse import OptionParser
import xml.etree.ElementTree as ET
import MyFilters
import os

class ContactInfo(object):
	def __init__(self):
		self.misc = ""
		self.email = ""

class Category(object):
	def __init__(self):
		self.name = ""
		self.type = ""
		self.items = []
		self.content = ""

class CatItem(object):
	def __init__(self):
		self.title = ""
		self.text = ""

if __name__ == '__main__':
	parser = OptionParser(usage = "%prog [private] <fileTypes> <resumeFile>", 
		description = "Takes the colon-separated list <fileTypes> and for each type, fills in the Cheetah template ResTemp<Type>.tmpl according to the data in ResumeFile")
	parser.add_option("-p", "--addprivateacontactdata", action="store_true", dest="addprivate", default = False)
	options, manArgs = parser.parse_args()

	if (len(manArgs) < 2):
		parser.print_help()
		exit()


	allOutputTypes = manArgs[0]
	outputList = allOutputTypes.split(":")

	inputFile = manArgs[1]

	searchList = {}
	
	tree = ET.parse(inputFile)
	
	root = tree.getroot()
	
	searchList['name'] = root.find("Name").text
	cInfo = root.find("ContactInfo")
	outputStr = cInfo.find("PublicInfo").text
	if (options.addprivate):
		outputStr = outputStr + "{cr}" + cInfo.find("PrivateInfo").text

	searchList['contactInfo'] = outputStr
	categories = []
	for category in root.iter("Category"):
		newCat = Category()
		newCat.name = category.find("Name").text

		if (category.find("Items") == None):
			newCat.type = "single"
			newCat.content = category.find("Text").text
		else:
			newCat.type = "multiple"
			newCat.items = []
			for item in category.iter("Item"):
				newItem = CatItem()

				if (item.find("Title") <> None):
					newItem.title = item.find("Title").text

				newItem.text = item.find("Text").text
				
				newCat.items.append(newItem)

		categories.append(newCat)

	searchList["categories"] = categories

	for outputType in outputList:
		templatePath = "restemp%s.tmpl" % outputType
		if (os.path.exists (templatePath)):
			print "Writing using template %s" % templatePath
			template = Template(file = templatePath, searchList = searchList, filtersLib = MyFilters)
			currFile = open("Resume.%s" % outputType, 'w')
			currFile.write(str(template))
			currFile.close()
			print "Written to Resume.%s" % outputType
		else:
			print "%s could not be found" % templatePath




