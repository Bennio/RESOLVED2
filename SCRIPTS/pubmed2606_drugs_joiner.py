"""
Rasemmblement entre pubmed et liste des drugs
"""

import utils
from utils import File_Reader as FR
from utils import File_Maker as FM
from utils import Task_Follower as TF
import random
import re
from string import punctuation

strippattern = "^\"|\"$"
pubmed_file = FR("../PUBMED_DATA/pubmed_data_2606.txt",
	sep = "\t", suppress_newlines = True, skiplines = 1, encoding = "CP1252",
	strip_chars_pattern = strippattern)

drugs_file = FR("../DRUG_LISTS/drug_list_2606_curated_cleaned.latest.txt",
	sep = ";", suppress_newlines = True, encoding = "utf-8")

pubmed = pubmed_file.readlines()
drugs = drugs_file.readlines()


match = {}

for article in pubmed:
	match[int(article[1])] = ("","",[],"")



# tf = TF(len(drugs))
for names in drugs:
	# tf.step()
	count=+1
	for article in pubmed:
		found = False
		title = article[5]
		description = article[6]
		pmid = int(article[1])
		year = article[3]
		for pat in names:

			re_pattern = r'\b\(?'+re.escape(pat)

			if re.search(re_pattern, r''+title.lower()):
				found = True
				break
			elif "(" in pat or "[" in pat:
				pat = re.escape(pat).lower()
				title2 = re.escape(title.lower())
				if pat in title2:
					found = True
					break


		if found:
			match[pmid][2].append(names)
			match[pmid] = (year, title, match[pmid][2], description)
		else:
			match[pmid] = (year, title, match[pmid][2] , description)
		
	# tf.step()


missing= 0
for k,v in match.items():
	if v==("","",[],""):
		missing+=1



pubmedNdrugs = FM("../PUBMED_DATA/pubmed2606_with_drugs",
	extension = ".txt", olddata_dir = "../OLD_DATA/PUBMED_DATA/")
with pubmedNdrugs.get_filepointer() as fp:
	for k,v in match.items():
		if v[2]:
			res = ""
			for i in range(len(v[2])):
				v[2][i] = ";".join(v[2][i])

			topop = []
			for i in v[2]:
				for j in v[2]:
					# " " not in j.replace(i, "")  and not " "+i+" " in v[1]
					if i in j and len(i) < len(j) and i not in topop  and "-" in j.replace(i, "") and not v[1].count(i)>1:
						topop.append(i)
			for to in topop:
				v[2].pop(v[2].index(to))
			
			res = "|".join(v[2])


			fp.write("\t".join([str(k),v[0], v[1],res])+"\n")
		else:
			fp.write("\t".join([str(k),v[0], v[1],""])+"\n")
	fp.close()


pubmed_file = FR("../PUBMED_DATA/pubmed2606_with_drugs.latest.txt",
	sep = "\t", suppress_newlines = True, skiplines = 0, encoding = "utf-8")


pub = pubmed_file.readlines()
c= 0
for line in pub:
	c+=(int(line[3] is ""))
	count = line[3].count("|")
	line.append(str(count + int(line[3] is not "")))
	if line[3] is "":
		print(line[0])
		print(line[2].lower())
		print(line[3])

print(c)


pubmedNdrugs = FM("../PUBMED_DATA/pubmed2606_with_drugs_counter",
	extension = ".txt", olddata_dir = "../OLD_DATA/PUBMED_DATA/")


pubmedNdrugs.set_datastream(pub)

pubmedNdrugs.save()


# with open("../PUBMED_DATA/pubmedNdrugs.latest.txt", "w", encoding = "utf-8") as fp:
# 	for k,v in match.items():
# 		if v[2]:
# 			fp.write("\t".join([str(k),v[0], v[1],v[2][0]])+"\n")
# 		else:
# 			fp.write("\t".join([str(k),v[0], v[1],""])+"\n")


# noDrug = FM("../PUBMED_DATA/pubmed_data_2606_noDRUG", extension = ".txt", olddata_dir = "../OLD_DATA/PUBMED_DATA/")
# with noDrug.get_filepointer() as fp:
# 	for k,v in match.items():
# 		if v == ("","",[],""):
# 			fp.write(str(k)+"\n")
# 	fp.close()
# #### Missing
# with open("../PUBMED_DATA/pubmed_data_2606_noDRUG_4.txt", "w", encoding = "utf-8") as fp:
# 	for k,v in match.items():
# 		if v == ("","",[],""):
# 			fp.write(str(k)+"\n")



# #### Positive control generator


# pop = list(range(0,2606-missing))
# samp1 = random.sample(pop, 50)
# samp2 = random.sample(pop, 40)
# samp3 = random.sample(pop, 40)

# no_miss = match.copy()
# del_keys = []
# for k,v in no_miss.items():
# 	if v==("","",[],""):
# 		del_keys.append(k)

# for k in del_keys:
# 	del no_miss[k]

# with open("../PUBMED_DATA/positiveControl_4.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp1:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")


# with open("../PUBMED_DATA/positiveControl_2.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp2:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")


# with open("../PUBMED_DATA/positiveControl_3.txt", "w", encoding = "utf-8") as fp:

# 	a = []
# 	i=0
# 	for m in no_miss.keys():
# 		if i in samp3:
# 			a.append(m)
# 		i+=1

# 	for k in a:
# 		fp.write("\t".join([str(k), no_miss[k][1], no_miss[k][3], ";".join(no_miss[k][2]) ])+"\n")
