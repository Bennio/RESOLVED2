from utils import File_Reader as FR
from utils import File_Maker as FM
from utils import head
import re

drug_file = FR("../DRUG_LISTS/original_drug_list_2606.txt",
	sep = "", suppress_newlines = True, encoding = "utf-8")

modifications_file = FR("../DRUG_LISTS/old_pubmed_with_drugs.latest.manually.annotated.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", strip_chars_pattern = "^\"|\"$", skiplines = 1)

drugs = []

for line in drug_file.iter():
	drugs.append(line)


for line in modifications_file.iter():
	
	current_Drugs = line[3].split("|")
	New_alias_identifier = line[5]
	Drug_manually_found_in_0drug_titles = line[6]
	Alias_to_delete = line[7]

	while '' in current_Drugs:
		current_Drugs.pop(current_Drugs.index(''))
		

	if Alias_to_delete in drugs and Alias_to_delete:
		drugs.pop(drugs.index(Alias_to_delete))
	else:
		if ";" in Alias_to_delete:
			a = Alias_to_delete.split(";")
			for i in a:
				if i in drugs:
					drugs.pop(drugs.index(i))


	if Drug_manually_found_in_0drug_titles:
		drugs.extend(Drug_manually_found_in_0drug_titles.lower().split("|"))

	if New_alias_identifier:
		New_alias_identifier = New_alias_identifier.lower().split("|")
		for n in New_alias_identifier:
			if n in drugs:
				drugs.pop(drugs.index(n))
		drugs.append(";".join(New_alias_identifier))

# Manuel Changes

drugs[drugs.index("interleukin 6")] = ";".join([drugs[drugs.index("interleukin 6")],"interleukin-6".lower()])
drugs.pop(drugs.index("5-fluorouracil 5-fluorouracil"))

# drugs.append("apalutamide;Apalutamide;ARN-509")
# drugs.append("Lutetium Lu 177 dotatate")
# drugs.append("brigatinib")
# drugs.append("ribociclib")
# drugs.append("necitumumab")
# drugs.append("talimogene laherparepvec")
# drugs.append("Dinutuximab;ch14.18")
# drugs.append("lanreotide")
# drugs.append("Peginterferon alfa-2b;Pegylated interferon alfa-2b")
# drugs.append("Iobenguane sulfate I-123;123I-iobenguane")
# drugs.append("Pegaspargase;polyethylene glycol-conjugated L-asparaginase")
# drugs.append("abarelix")
# drugs.append("fulvestrant")
# drugs.append("zoledronic acid")
# drugs.append("Valrubicin;N-trifluoroacetyladriamycin-14-valerate;AD-32")
# drugs.append("anastrozole")



for d in range(len(drugs)):
	drugs[d] = ";".join(sorted(drugs[d].split(";")))


drugs = list(set(drugs))
drugs.sort()

# Get rid of single alias duplicates
for query in drugs:
	for d in drugs:
		if query in d.split(";") and drugs.index(query)!=drugs.index(d):
			drugs.pop(drugs.index(query))
			break

for d in range(len(drugs)):
	drugs[d] = ";".join(sorted(drugs[d].split(";")))


drugs = list(set(drugs))
drugs.sort()


# Join partially similar names
join = []
for query in drugs:
	for d in drugs:
		for q in query.split(";"):
			if q in d.split(";") and drugs.index(query)!=drugs.index(d):
				join.append(sorted([drugs.index(query),drugs.index(d)]))
				break
# print(drugs[drugs.index("et 743")] in drugs[drugs.index("et-743;trabectedin;et 743")])

merge = []
while join:
	tomerge = [line for line in join.pop(0)]
	while tomerge in join:
		join.pop(join.index(tomerge))
	if join:
		for couple in join:
			for line in couple:
				if line in tomerge:
					tomerge.extend(join.pop(join.index(couple)))
					while couple in join:
						join.pop(join.index(couple))
					break
	merge.append(tomerge)

todel = []
maxdel = len(drugs)

for lines in merge:
	d = []
	for index in lines:
		todel.append(drugs[index])
		d.extend(drugs[index].split(";"))
	drugs.append(";".join(sorted(list(set(d)))))


for d in todel:
	if d in drugs and drugs.index(d) < maxdel-len(todel):
		drugs.pop(drugs.index(d))



for d in range(len(drugs)):
	drugs[d] = ";".join(sorted(drugs[d].split(";")))


drugs = list(set(drugs))
drugs.sort()


pool_file = FM("../DRUG_LISTS/drug_list_2606_curated_cleaned",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/DRUG_LISTS", encoding = "utf-8")

pool_file.set_datastream(drugs)
pool_file.save()
pool_file.close()


# annotations = annotation_file.readlines()

# header = annotations.pop(0)
# drug_dict = {}
# for line in annotations:
# 	drug_dict[line[0]] = {}
# 	for i in range(len(header)):
# 		val = ""
# 		if i in range(len(line)):
# 			val = line[i]
# 		drug_dict[line[0]][header[i]] = val


# fulldl = []


	# for d in current_Drugs:
	# 	topop = []
	# 	for i in current_Drugs:
	# 		if d in i and len(d) != len(i) and d not in topop:
	# 			topop.append(d)
	# 			print(d)
	# 	for p in topop:
	# 		current_Drugs.pop(current_Drugs.index(p))

	# for d in current_Drugs:
	# 	if "recombinant humanized" in d:
	# 		print("aaaa")

# 	fulldl.append(current_Drugs)


# print(fulldl[0])
# print(fulldl[1])
# print(fulldl[2])

# print(len(fulldl))


# newlist = []

# for f in fulldl:
# 	for d in f:
# 		if not d:
# 			print(d)
# 		newlist.append(d.lower())

# newlist = list(set(newlist))

# print(len(newlist))
# newlist.sort()


# topop = []
# for n in newlist:
# 	for j in newlist:
# 		if n in j and len(n) < len(j):
# 			topop.append(n)

# topop = list(set(topop))
# for p in topop:
# 	newlist.pop(newlist.index(p))





# print(len(drug_dict))
# print("deleting some keys")
# for delete in listing:
# 	if delete[7]:
# 		print(delete[7])
# 	if delete[7] and delete[7] in drug_dict:
# 		del drug_dict[delete[7]]

# print(len(drug_dict))

# cat = []
# for c in listing:
# 	if c[5]:
# 		cat.append(c[5])

# cat = list(set(cat))

# print(len(cat))
# count = 0
# for c in cat:
# 	drugs = c.split("|")
# 	for d in drugs:
# 		if d.lower() not in drug_dict:
# 			# print(d)
# 			# print(drugs)
# 			count+=1
# 			break

# print(count)

