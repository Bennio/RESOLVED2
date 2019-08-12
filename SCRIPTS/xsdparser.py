import xml.etree.ElementTree as ET
from utils import File_Maker as FM

# Parse xml file.
print("parsing xml")
tree = ET.parse('../DRUGBANK/drugbank_db_schema.xml')
root = tree.getroot()

res = []

def tree_builder(node,depth):
	for child in node:
		print(child.tag)
		res.append(depth * '\t' + child.tag)
		tree_builder(child, depth+1)

tree_builder(root, 0)

tree_tagging = FM("../DRUGBANK/tree_tagging", extension = ".txt")

with tree_tagging.get_filepointer() as fp:
	for t in res:
		fp.write(t+'\n')
	fp.close()

# def tree_builder(node):
# 	children = []
# 	for elem in node:
# 		children.append(elem.tag)
# 		next_elem = tree_builder(elem)
# 		if next_elem:
# 			children.append(next_elem)

# 	return children


# depth = 0
# processed = []
# rep = []
# def flat(elements, depth):
# 	local = []
# 	for i in elements:
# 		if type(i) is list and i not in processed:
# 			processed.append(i)
# 			flat(i, depth+1)
			
# 		elif type(i) is str and i not in local:
# 			local.append(i)
# 			rep.append(depth*'\t'+i)
	

# flat(tags, 0)

