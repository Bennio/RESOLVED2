"""
Parsing drugbank.xml script
"""

import xml.etree.ElementTree as ET
import re
import time
import sys
from utils import File_Reader as FR
from utils import Task_Follower as TF
from utils import File_Maker as FM
from utils import head


def get_xpath(elem, keyword = "", returntodrug = True, path = ""):
	'''
	Returns a predefined XPath string to retrive xml.etree objects.

	:param elem: predefined query
	:param keyword: target xml tag
	:param returntodrug: rerurn XPath of drug tag elemement
	:param path: return specified path
	'''
	retpath = ""

	if path:
		return(path)

	if keyword:
		keyword = "".join(["'",keyword, "'"])

	xpath_dict = {
	"all_name":"./drug/name",
	"all_pubmed-id": "./drug/general-references/articles/article/pubmed-id",
	"all_synonym": "./drug/synonyms/synonym",
	"by_name": "./drug[name="+keyword+"]",
	"by_description": "./drug[description="+keyword+"]",
	"by_pubmed-id": "./drug/general-references/articles/article[pubmed-id="+keyword+"]"
	}

	if returntodrug:
		retpath = "/".join([".." for i in range(xpath_dict[elem].count("/")-1)])

	return xpath_dict[elem]+retpath


def get_alltext_fromtag(tag):
	"""
	Returns a list of text elements from all tag with specified name. Tag must be searchable with get_xpath function
	and be in the xpath dict.
	"""
	tag = "all_"+tag
	return([elem.text for elem in root.findall(get_xpath(tag, returntodrug = False))])



def match_any(items, data, sep = ";"):
	"""
	Return a list of booleans. Is True if any string in items is matched in data.

	:param items: List of query strings. Each string can contain multiple mathcing terms and the function will return True if any match. 
	:pram data: List of queried strings.
	:param sep: sperator for strings in items if multiple matching queries for one element in items.
	"""
	res = [False for j in range(len(data))]

	for i in items:
		drugs = i
		if sep:
			drugs = i.split(sep)
		match = False
		index = -1
		for d in drugs:
			if(d in data):
				match = True
				index = data.index(d)
		if match:
			res[index] = True
	
	return(res)


def char_strip(string, pattern):
	"""
	Deletes any characters from string that corresponds to the regular expression (pattern).
	"""
	return re.sub(pattern, '', string)


def find_rec(node, level):
	for item in node:
		yield (item, level)
		for child in find_rec(item, level+1):
			yield child



if __name__ == '__main__':
	
	# Load files and data
	print("reading files")
	pmid = []
	drugs_data = []


	drug_data_file = FR("../DRUG_LISTS/full_drug_list.latest.txt", sep = ';', suppress_newlines = True, skiplines = 0,
		encoding = "utf-8")

	drugs_data = drug_data_file.readlines()

	# for line in drug_data_file.iter():
	# 	pmid.append(line[0])
	# 	a = line[1]
	# 	if a!="NA" or a!="":
	# 		drugs_data.append(a)

	# Parse xml file.
	print("parsing xml")
	tree = ET.parse('../DRUGBANK/drugbank_db.xml')
	root = tree.getroot()

	sample = ["Erlotinib","Irinotecan","Cisplatin","Pembrolizumab","Bevacizumab","(4R)-limonene","Obinutuzumab","Rituximab"]
	dico = []
	
	# for s in sample:
	# r = root.findall("./drug[name='"+s+"']")
	r = root.findall("./drug[name='Rituximab']")
	
	# for drug in r:
	# 	queue = []
	# 	for node in drug.iter():


	l = list(find_rec(r, 0))

	# for element in l:
	# 	print("\t".join([str(element[0].tag), str(element.text)]))

	for el in l:
		# print(el)
		tag = str(el[0].tag)
		text = str(el[0].text)
		tabs = el[1]*'\t'

		
		text = re.sub(r'\n',", ", text)

		text = re.sub(r'\n{2,}',"", text)

		text = re.sub(r"^, +", "", text)

		# print(text)
		print(tabs+"\t".join([tag,text]))
	

       
         


	# # a = [elem for elem in root.findall(get_xpath("by_PMID", keyword = "26242220"))]
	# a = [elem for elem in root.findall("./drug[name='Lepirudin']")]
	# head(a)
	# res = []
	# print("search")
	# # i=1
	# # for p in pmid:
	# # 	print(i)
	# # 	res.append(root.findall(get_xpath("all_pmid", keyword = p)))
	# # 	i+=1

	# # Extracts names of drugs from xml. all_name is to be formated.
	# all_name = get_alltext_fromtag("name")
	# real_names = get_alltext_fromtag("name")


	# # Formating for searching
	# print("stripping")



	# head(drugs_data)

	# head(all_name)


	# save_file = FM("../DRUGBANK/db_drugsNalias_v2", extension = ".txt", olddata_dir = "../OLD_DATA/DRUGBANK/")

	# with save_file.get_filepointer() as fp:
	# 	fp.write("DB_NAME\tDB_SYNONYMS\tDB_PRODUCTS\tDB_ID\tCAS_NUMBER\tUNII\n")
	# 	for name in all_name:
	# 		xpath_syn = "./drug[name=\""+name+"\"]/synonyms/synonym"
	# 		xpath_products = "./drug[name=\""+name+"\"]/products/product/name"
	# 		xpath_dbid = "./drug[name=\""+name+"\"]/drugbank-id"
	# 		xpath_cas_number = "./drug[name=\""+name+"\"]/cas-number"
	# 		xpath_unii = "./drug[name=\""+name+"\"]/unii"


	# 		syn = [elem.text for elem in root.findall(xpath_syn)]
	# 		products = [elem.text for elem in root.findall(xpath_products)]
	# 		dbid = [elem.text for elem in root.findall(xpath_dbid)]
	# 		cas_number = [elem.text for elem in root.findall(xpath_cas_number)]
	# 		unii = [elem.text for elem in root.findall(xpath_unii)]

	# 		write_list = [name,";".join(list(set(syn))),";".join(list(set(products))), "", "", ""]
			
	# 		if dbid[0] is not None:
	# 			write_list[3] = ";".join(dbid)
	# 		if cas_number[0] is not None:
	# 			write_list[4] = ";".join(cas_number)
	# 		if unii[0] is not None:
	# 			write_list[5] = ";".join(unii)

	# 		fp.write("\t".join(write_list)+'\n')


	# syn = get_alltext_fromtag("synonym")



	# for i in range(len(all_name)):
	# 	all_name[i] = char_strip(all_name[i], "[-]").lower()

	# for i in range(len(drugs_data)):
	# 	drugs_data[i] = char_strip(drugs_data[i], "[-]").lower()


	# print("lookup")

	# # find correspondance between our database and xml database.
	# res = match_any(drugs_data, all_name)



	# print(len(res))

	# print(res.count(True))


	# print("relookup")

	# # elems = [root.findall(get_xpath("by_name", keyword = name)) for name,found in zip(all_name, res) if found]

	# elems = []

	# # extract all xml objects by name for further task.
	# start = time.time()
	# for name,found in zip(real_names, res):
		
	# 	if found:
	# 		elems.append(root.find(get_xpath("by_name", keyword = name)))
	# 		# elems.append(name)


	# duree = time.time() - start

	# print("La recherche prend %.2f" % duree)
	# print(len(elems))