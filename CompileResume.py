from Cheetah.Template import Template
import xml.etree.ElementTree as ET

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

class Item(object):
	def __init__(self):
		self.title = ""
		self.text = ""

if __name__ == '__main__':
	searchList = {}
	
	tree = ET.parse("Resume.xml")
	
	root = tree.getroot()
	
	searchList['name'] = root.find("Name").text

	info = root.find("ContactInfo")
	cinfo = ContactInfo()
	cinfo.misc = info.find("Misc").text
	cinfo.email = info.find("Email").text
	searchList['contactInfo'] = cinfo

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
				newItem = Item()

				if (item.find("Title") <> None):
					newItem.title = item.find("Title").text

				newItem.text = item.find("Text").text
				newCat.items.append(item)

		categories.append(newCat)

	searchList["categories"] = categories
	