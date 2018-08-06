from utils import File_Reader as FR
from utils import File_Maker as FM
from utils import head
import re
from datetime import datetime

annotation_file = FR("../DRUG_LISTS/drug_pivot_2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8")



annotations = annotation_file.readlines()

header = annotations.pop(0)
header.append("DRUGBANK_SYNONYS_AND_PRODUCTS")
header.append("DRUGBANK_ID")
header.append("CAS_NUMBER")
header.append("UNII")
header.append("ASSOCIATED_PMID")
header.append("OLDEST_PMID")
header.append("OLDEST_DATE_OF_PUBLICATION")


print(header)


pool_data = []
pool_data.append(header)


drug_dict = {}
for line in annotations:
	drug_dict[line[0]] = {}
	for i in range(len(header)):
		val = ""
		if i in range(len(line)):
			val = line[i]
		drug_dict[line[0]][header[i]] = val



# Add drugbank known names to file

mined_file = FR("../PUBMED_DATA/pivot2606_in_drugbank.latest.txt",
	skiplines = 1, sep = "\t", suppress_newlines = True, encoding = "utf-8")

mined = mined_file.readlines()

for m in mined:
	alias = m[2]
	syn = m[1]
	prod = m[3]
	dbid = m[4]
	cas = m[5]
	unii = m[6]
	drug_dict[alias]["COMMON_DRUGBANK_ALIAS"] = m[0]

	drug_dict[alias]["DRUGBANK_SYNONYS_AND_PRODUCTS"] = ";".join([syn, prod]) if syn and prod else syn if syn else prod if prod else ""
	drug_dict[alias]["DRUGBANK_ID"] = dbid
	drug_dict[alias]["CAS_NUMBER"] = cas
	drug_dict[alias]["UNII"] = unii
	# print(drug_dict[alias]["COMMON_DRUGBANK_ALIAS"])





# Add all known alias from DrugBank

# alias_file = FR("../PUBMED_DATA/drugfinal_DrugB_v2.latest.txt",
# 	sep = "\t", skiplines = 1, suppress_newlines = True, encoding = "utf-8")

# for line in alias_file.iter():
# 	drug_dict[line[2]]["DRUGBANK_SYNONYS_AND_PRODUCTS"] = line[1]



# Search drugbank for alternative aliases from CIR and Pubchem

alternative_alias_file = FR("../DRUG_LISTS/pcp_cir_newalias.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8")

drugbank_db_file = FR("../DRUGBANK/drugbank_extracted_identifiers.latest.txt",
	skiplines = 1, suppress_newlines = True, encoding = "utf-8")

drugbank = drugbank_db_file.readlines()

count = 0
for new in alternative_alias_file.iter():
	key = new[0]

	# print(key)

	if new[1] or new[2]:
		a=''
		if new[1]:
			a = new[1].lower().split(";")
		b=''
		if new[2]:
			b = new[2].lower().split(";")
		aliases = []
		if a:
			aliases.extend(a)
		if b:
			aliases.extend(b)

		aliases = list(set(aliases))

		found = False
		entry = ""
		
		for al in aliases:
			for line in drugbank:
				string = ";".join(line.split("\t")[0:3]).split(";")
				if al.lower() in string:
					found = True
					entry = line
					break
			if found:
				break

		if found:
			# print(aliases)
			# print(entry)
			count+=1
			entry = entry.split("\t")
			drug_dict[key]["COMMON_DRUGBANK_ALIAS"] = entry[0]

			syn = ""
			if entry[1]:
				syn = entry[1]
			if entry[2] and syn:
				syn = ";".join([syn,entry[2]])
			elif entry[2]:
				syn = entry[2]
			drug_dict[key]["DRUGBANK_SYNONYS_AND_PRODUCTS"] = syn

			drug_dict[key]["DRUGBANK_ID"] = entry[3]
			drug_dict[key]["CAS_NUMBER"] = entry[4]
			drug_dict[key]["UNII"] = entry[5]

print("New stuff")
print(count)



# Add knonw associated pmid to drugs


pmid_file = FR("../PUBMED_DATA/pubmed2606_with_drugs.latest.txt", sep = "\t", suppress_newlines = True, encoding = "utf-8")

for line in pmid_file.iter():
	if line[3]:
		drugs = line[3].split("|")
		for d in drugs:
			if drug_dict[d]["ASSOCIATED_PMID"]:
				drug_dict[d]["ASSOCIATED_PMID"] = ";".join([drug_dict[d]["ASSOCIATED_PMID"], line[0]])
			else:
				drug_dict[d]["ASSOCIATED_PMID"] = line[0]



# Add Oldest pmid and date of publication

strippattern = "^\"|\"$"
pubmed_file = FR("../PUBMED_DATA/pubmed_data_2606.txt", sep = "\t",
	suppress_newlines = True, encoding = "CP1252", strip_chars_pattern = strippattern)


pubmed_dict = {}
for line in pubmed_file.iter():
	pubmed_dict[line[1]] = " ".join([line[4], line[3]])

for drug in drug_dict.values():
	if drug["ASSOCIATED_PMID"]:
		pmids = drug["ASSOCIATED_PMID"].split(";")
		date_list = []
		for pmid in pmids:
			date_list.append(pubmed_dict[pmid])
		for i in range(len(date_list)):
			date_list[i] = datetime.strptime(date_list[i], "%m %Y")
		min_index = date_list.index(min(date_list))
		drug["OLDEST_PMID"] = pmids[min_index]
		drug["OLDEST_DATE_OF_PUBLICATION"] = datetime.strftime(date_list[min_index], "%m/%Y")

# Save stuff 

pool_file = FM("../PUBMED_DATA/drugs2606minedalias_with_found_identifiers",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/PUBMED_DATA")

for drug in drug_dict.values():
	pool_data.append(drug.values())

pool_file.set_datastream(pool_data)
pool_file.save()
pool_file.close()


