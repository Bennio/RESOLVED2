from utils import File_Reader as FR
from utils import File_Maker as FM

annotation_file = FR("../DRUG_LISTS/drug_pivot_0_1.clean.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8")
drugs_file = FR("../DRUG_LISTS/drug_list_2606_curated_cleaned.latest.txt",
	sep = "", suppress_newlines = True, encoding = "utf-8")


old_drugs = []
annotations = annotation_file.readlines()

header = annotations.pop(0)

old_drug_dict = {}
for line in annotations:
	old_drug_dict[line[0]] = {}
	for i in range(len(header)):
		val = ""
		if i in range(len(line)):
			val = line[i]
		old_drug_dict[line[0]][header[i]] = val

print(header)

for line in annotations:
	old_drugs.append(line[0])


new_dict = {}

new_drugs = drugs_file.readlines()

for oldd in old_drugs:

	index = []
	old = oldd.split(";")
	for o in old:
		for new in new_drugs:
			if o in new.split(";"):
				index.append(new_drugs.index(new))

	index = list(set(index))

	# if len(index)==0:
		# print("missing")
		# print(oldd)
		# for i in range(len(header)):
		# 	new_drugs[old][header[i]] = ""

	if len(index)==1:
		ind = index.pop()
		new_dict[new_drugs[ind]] = {}
		for i in range(len(header)):
			new_dict[new_drugs[ind]][header[i]] = old_drug_dict[oldd][header[i]]
		# print("aa")
		# print(new_dict[new_drugs[ind]])

	if len(index)>1:
		choices = [new_drugs[c] for c in index]
		print("conflict")



print(len(new_dict))


for new in new_drugs:
	if not new in new_dict:
		new_dict[new] = {}
		for i in range(len(header)):
			new_dict[new][header[i]] = ""

print(len(new_dict))

for new in new_drugs:
	new_dict[new]["DRUG_NAMES"] = new

pool_file = FM("../DRUG_LISTS/drug_pivot_2606",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/PUBMED_DATA")


pool_data = []
pool_data.append(header)

for drug,values in sorted(new_dict.items()):
	pool_data.append(values.values())

pool_file.set_datastream(pool_data)
pool_file.save()
pool_file.close()




