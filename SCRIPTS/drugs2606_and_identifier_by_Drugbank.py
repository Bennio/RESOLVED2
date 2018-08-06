from utils import File_Reader as FR
from utils import File_Maker as FM
from utils import Task_Follower as TF
import cirpy
import pubchempy as pcp
from datetime import datetime

pivot_file = FR("../PUBMED_DATA/drugs2606minedalias_with_found_identifiers.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8")

lines = pivot_file.readlines()
print(len(lines))

header = lines.pop(0)

def cirpy_getter(drug):
	c = cirpy.resolve(drug, 'names')
	if c:
		return ";".join(c)
	else:
		return ""

def pcp_getter(drug):
	p = pcp.get_synonyms(drug, 'name')
	if p:
		return ";".join(p[0]["Synonym"])
	else:
		return ""

def union_of_2lists(list1, list2):
	if not list1 and not list2:
		return ""
	if not list1:
		return list2
	if not list2:
		return list1
	if type(list1) is str:
		list1 = list1.split(";")
	if type(list2) is str:
		list2 = list2.split(";")
	res = list1+list2
	return ";".join(sorted(list(set(res))))

def do_nothing(args):
	pass

def set_string(string):
	return str(string)

# No cirpy and pubchem
# keys = ["COMMON_DRUGBANK_ALIAS","MINED_ALIAS", "DRUGBANK_SYNONYS_AND_PRODUCTS",
# "DRUGBANK_ID","CAS_NUMBER","UNII","ASSOCIATED_PMID","OLDEST_PMID","OLDEST_DATE_OF_PUBLICATION"]

keys = ["COMMON_DRUGBANK_ALIAS","MINED_ALIAS", "DRUGBANK_SYNONYS_AND_PRODUCTS",
"DRUGBANK_ID","CIR_ALIAS","PUBCHEM_ALIAS","CAS_NUMBER","UNII","ASSOCIATED_PMID","OLDEST_PMID","OLDEST_DATE_OF_PUBLICATION"]

procedure = [set_string, union_of_2lists, union_of_2lists,
union_of_2lists, cirpy_getter, pcp_getter, union_of_2lists, union_of_2lists, union_of_2lists]

# No cirpy and pubchem
# procedure = [set_string, union_of_2lists, union_of_2lists,
# union_of_2lists, union_of_2lists, union_of_2lists, union_of_2lists, do_nothing, do_nothing]


drugbank_drugs = []
drugbank_dict = {}


for line in lines:
	if line[11]:
		drugbank_drugs.append(line[11])

drugbank_drugs = list(set(drugbank_drugs))
print(len(drugbank_drugs))
for drug in drugbank_drugs:
	drugbank_dict[drug] = {}
	for k in keys:
		drugbank_dict[drug][k] = ""

	# drugbank_dict[drug]["COMMON_DRUGBANK_ALIAS"] = drug
print(len(procedure))
t = TF(len(lines))
for line in lines:
	t.step()
	if line[11]:
		# print(line[0])
		# print(line[11])

		db_alias = line[11]

		mined = line[0]
		al = line[13]

		# No cirpy/pubchem
		# args = [db_alias, mined, al, line[14], line[15], line[16], line[17], "", ""]
		args = [db_alias, mined, al, line[14], db_alias, db_alias, line[15], line[16], line[17]]

		for i in range(len(procedure)):
			if i in [1,2,3,6,7,8]:
			# if i in [1,2,3,4,5,6]:
				drugbank_dict[db_alias][keys[i]] = procedure[i](drugbank_dict[db_alias][keys[i]], args[i])
			else:
				drugbank_dict[db_alias][keys[i]] = procedure[i](args[i])




		if line[19]!="":
			line_min = (line[18], datetime.strptime(line[19], "%m/%Y"))
			print(line[0])
			print(line_min)
			print(drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"])
			print("")
			if not drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"]:
				drugbank_dict[db_alias]["OLDEST_PMID"] = line_min[0]
				drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"] = datetime.strftime(line_min[1], "%m/%Y")

			else:
				current_min = (drugbank_dict[db_alias]["OLDEST_PMID"], datetime.strptime(drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"], "%m/%Y"))
				if line_min[0] is not current_min[0]:
					pmids = [line_min[0], current_min[0]]
					dates = [line_min[1], current_min[1]]
					drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"] = datetime.strftime(dates[dates.index(min(dates))], "%m/%Y")
					drugbank_dict[db_alias]["OLDEST_PMID"] = pmids[dates.index(min(dates))]

			print(line[0])
			print(line_min)
			print(drugbank_dict[db_alias]["OLDEST_DATE_OF_PUBLICATION"])
			print(drugbank_dict[db_alias])
			print("")

		# print(drugbank_dict[db_alias])


pool_file = FM("../PUBMED_DATA/drugbank2606",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/PUBMED_DATA")


pool_data = []
pool_data.append(keys)
for drug in drugbank_dict.values():
	pool_data.append(drug.values())
print(len([v for v in drugbank_dict.values()]))
pool_file.set_datastream(pool_data)
pool_file.save()
pool_file.close()