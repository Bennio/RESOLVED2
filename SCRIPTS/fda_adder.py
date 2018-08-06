from utils import File_Reader as FR
from utils import File_Maker as FM
from datetime import datetime

annotation_file = FR("../PUBMED_DATA/drugbank2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

fda_file = FR("../FDA/FDA_DRUG_DATABASE_cured_cleaned.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

drugbank_alias_file = FR("../DRUGBANK/drugbank_extracted_identifiers.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

lines = annotation_file.readlines()

annotation_header = lines.pop(0)

# print(lines[0])

drug_dict = {}

for line in lines:
	drug_dict[line[0]] = {}
	for i in range(len(annotation_header)):
		drug_dict[line[0]][annotation_header[i]] = line[i]
	drug_dict[line[0]]["FDA_APPROUVED"] = 0



problem_list = []
change_list = []
problem_list.append("L-glutamine oral")
change_list.append("L-glutamine")
problem_list.append("irinotecan liposome")
change_list.append("irinotecan")
problem_list.append("trifluridine/tipiracil")
change_list.append("tas-102")
problem_list.append("paclitaxel protein-bound particles")
change_list.append("paclitaxel")
problem_list.append("vinCRIStine sulfate LIPOSOME")
change_list.append("Vincristine")
problem_list.append("eribulin mesylate")
change_list.append("Eribulin")
problem_list.append("iobenguane I 123")
change_list.append("Iobenguane sulfate I-123")
problem_list.append("Doxorubicin HCl liposome")
change_list.append("Doxorubicin")
problem_list.append("Revlimid (lenalidomide)")
change_list.append("lenalidomide")
problem_list.append("doxorubicin HCl liposome)")
change_list.append("doxorubicin")
# problem_list.append("polifeprosan 20 with carmustine implant")
# change_list.append("")
problem_list.append("Taxotere (Docetaxel)")
change_list.append("Docetaxel")

fda = fda_file.readlines()

fda_header = fda.pop(0)

fda_dict = {}

for line in fda:
	if line[1] not in fda_dict.keys():
		fda_dict[line[1]] = {}
		for i in range(len(fda_header)):
			fda_dict[line[1]][fda_header[i]] = line[i]
		fda_dict[line[1]]["COMMON_DRUG_BANK_ALIAS"] = ""
		if line[1] in problem_list:
			fda_dict[line[1]]["drug"] = change_list[problem_list.index(line[1])]
	else:
		fda_dict[line[1]]["date"] = ";".join([fda_dict[line[1]]["date"], line[4]])




db_alias = drugbank_alias_file.readlines()
db_header = db_alias.pop(0)

alias_dict = {}

for line in db_alias:
	alias_dict[line[0]] = {}
	for i in range(len(db_header)):
		alias_dict[line[0]][db_header[i]] = line[i]


# print(annotation_header)
# print(fda_header)
# print(db_header)

count = 0
# print("Not in COMMON_DRUG_BANK_ALIAS_LIST_final")
to_remove = []
for fda_drug in fda_dict.values():
	found = False
	for drug in drug_dict.values():
		cond1 = fda_drug["drug"].lower() in drug["COMMON_DRUGBANK_ALIAS"].lower()
		cond2 = fda_drug["drug"].lower() in drug["DRUGBANK_SYNONYS_AND_PRODUCTS"].lower()
		cond3 = fda_drug["drug"].lower() in drug["MINED_ALIAS"].lower()
		if cond1 or cond2 or cond3:
			found = True
			drug["FDA_APPROUVED"] = 1

	if not found:
		count+=1
		print(fda_drug["drug"])
		to_remove.append(fda_drug["drug"])
		

# print(count)


# print("Not in DrugBank")
# print()
count = 0
for fda_drug in fda_dict.values():
	found = False
	common_name = ""
	for alias in alias_dict.values():
		cond1 = fda_drug["drug"].lower() in alias["DB_NAME"].lower()
		if cond1:
			found = True
			common_name = alias["DB_NAME"]
			break

	if not found:
		for alias in alias_dict.values():
			cond2 = fda_drug["drug"].lower() in alias["DB_SYNONYMS"].lower()
			cond3 = fda_drug["drug"].lower() in alias["DB_PRODUCTS"].lower()
			if cond2 or cond3:
				found = True
				common_name = alias["DB_NAME"]
				break

	if not found:
		count+=1
		# print(fda_drug["drug"])

	if found:
		fda_drug["COMMON_DRUG_BANK_ALIAS"] = common_name

# print(count)
# 2

app = 0
for d in drug_dict.values():
	# print(d)
	app+=d["FDA_APPROUVED"]

# print(app)
# 132


def setify_lists(l1, l2, sep = ";"):
	return sep.join(sorted(list(set(l1+l2))))

compacted_fda_dict = {}

for key in fda_dict.keys():
	new_key = fda_dict[key]["COMMON_DRUG_BANK_ALIAS"]
	if new_key not in compacted_fda_dict.keys():
		compacted_fda_dict[new_key] = fda_dict[key]
	else:
		compacted_fda_dict[new_key]["drug"] = setify_lists(compacted_fda_dict[new_key]["drug"].lower().split(";"), fda_dict[key]["drug"].split(";"))
		compacted_fda_dict[new_key]["industry"] = setify_lists(compacted_fda_dict[new_key]["industry"].lower().split(";"), fda_dict[key]["industry"].split(";"))
		compacted_fda_dict[new_key]["date"] = setify_lists(compacted_fda_dict[new_key]["date"].split(";"), fda_dict[key]["date"].split(";"))
		compacted_fda_dict[new_key]["indication"] = setify_lists(compacted_fda_dict[new_key]["indication"].lower().split(";"), fda_dict[key]["indication"].split(";"))

# fda["drug"], fda["COMMON_DRUG_BANK_ALIAS"], fda["industry"], fda["date"], fda["min_date"]


pool_file = FM("../FDA/FDA_by_drugbank2606",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/FDA")

pool_data = []

pool_data.append("FDA_APPROUVED_DRUG	COMMON_DRUG_BANK_ALIAS	INDUSTRY	INDICATION	DATES_OF_APPROVAL	FIRST_DATE_OF_APPROVAL")


def try_parsing_date(text):
	for fmt in ("%B %d %Y", "%b. %d %Y", "%b %Y" ,"%B %Y" , "%B %d%Y", "%B %Y", "%B%d %Y", "%B%d%Y"):
		try:
			return datetime.strptime(text, fmt)
		except ValueError:
			pass
	raise ValueError('no valid date format found')

for fda in compacted_fda_dict.values():

	if fda["drug"] not in to_remove:
		dates = []
		for d in fda["date"].split(";"):
			# print(d)
			dates.append(try_parsing_date(d))

		fda["min_date"] = datetime.strftime(min(dates), "%d/%m/%Y")

		pool_data.append([fda["drug"], fda["COMMON_DRUG_BANK_ALIAS"], fda["industry"], fda["indication"], fda["date"], fda["min_date"]])


pool_file.set_datastream(pool_data)
pool_file.save()
pool_file.close()
