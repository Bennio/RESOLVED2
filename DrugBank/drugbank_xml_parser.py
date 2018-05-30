import xml.etree.ElementTree as ET
import re
import time
import sys
from utils import File_Handler as FH
from utils import Task_Follower as TF


def get_xpath(elem, keyword = "", returntodrug = True, path = ""):

	retpath = ""

	if path:
		return(path)

	if keyword:
		keyword = "".join(["'",keyword, "'"])

	xpath_dict = {
	"all_name":"./drug/name",
	"all_pubmed-id": "./drug/general-references/articles/article/pubmed-id",
	"by_name": "./drug[name="+keyword+"]",
	"by_description": "./drug[description="+keyword+"]",
	"by_pubmed-id": "./drug/general-references/articles/article[pubmed-id="+keyword+"]"
	 }

	if returntodrug:
		retpath = "/".join([".." for i in range(xpath_dict[elem].count("/")-1)])

	return xpath_dict[elem]+retpath


def get_alltext_fromtag(tag):
	
	tag = "all_"+tag
	return([elem.text for elem in root.findall(get_xpath(tag, returntodrug = False))])



def match_any(items, data, sep = ";"):
	
	res = [False for j in range(len(data))]

	for i in items:
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
	return re.sub(pattern, '', string)




print("reading files")
pmid = []
drugs_data = []


file = FH("../PUBMED_DATA/pubmedNdrugs.txt", sep = '\t', no_newline = True, skiplines = 1)

for line in file.iter():
	pmid.append(char_strip(line[1],"^\"\"$"))
	a = char_strip(line[2],"\"")
	if a!="NA":
		drugs_data.append(a)


print("parsing xml")
tree = ET.parse('drugbank_db.xml')
root = tree.getroot()





# a = [elem for elem in root.findall(get_xpath("by_PMID", keyword = "26242220"))]
# a = [elem for elem in root.findall("./drug[name='Lepirudin']")]

res = []
print("search")
# i=1
# for p in pmid:
# 	print(i)
# 	res.append(root.findall(get_xpath("all_pmid", keyword = p)))
# 	i+=1

all_name = get_alltext_fromtag("name")
real_names = get_alltext_fromtag("name")

print(len(all_name))

print("stripping")

for i in range(len(all_name)):
	all_name[i] = char_strip(all_name[i], "[-]").lower()

for i in range(len(drugs_data)):
	drugs_data[i] = char_strip(drugs_data[i], "[-]").lower()


print("lookup")

res = match_any(drugs_data, all_name)



print(len(res))

print(res.count(True))


print("relookup")

# elem for elem in 
# elems = [root.findall(get_xpath("by_name", keyword = name)) for name,found in zip(all_name, res) if found]

elems = []

tf = TF(len(res))

start = time.time()
for name,found in zip(real_names, res):
	
	tf.next()
	if found:
		elems.append(root.find(get_xpath("by_name", keyword = name)))
		# elems.append(name)


duree = time.time() - start

print("La recherche prend %.2f" % duree)

print(elems[0:10])
print(len(elems))


# out = []
# for i in [elem.tag for elem in elems[0].iter()]:
# 	if i not in out:
# 		out.append(i)
# 		print(i)
# elems = []
# tot = len(res)
# i = 0

# tf = TF(len(res))

# start = time.time()
# for name,found in zip(real_names, res):
# 	i+=1
# 	percent = 100*i/tot
# 	sys.stdout.write('%.2f \r' % (percent))
# 	sys.stdout.flush()
# 	if found:
# 		elems.append(root.find(get_xpath("by_name", keyword = name)))
# 		# elems.append(name)
