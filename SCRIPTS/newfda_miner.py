from utils import File_Reader as FR
from utils import File_Maker as FM
from datetime import datetime

drugs_file = FR("../PUBMED_DATA/drugbank2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

# drugs_file = FR("../PUBMED_DATA/drugbank2606.latest.txt",
# 	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)


fda_file = FR("../FDA/FDA_DATABASE_2018_07.txt",
	sep = "", suppress_newlines = True, encoding = "CP1252", skiplines = 1)

strippattern = "^\"|\"$|^ +| +$"
fda_file2 = FR("../FDA/FDA_DATABASE_2018_07.txt",
	sep = "\t", suppress_newlines = True, encoding = "CP1252", skiplines = 0, strip_chars_pattern = strippattern)


# fda_dict = fda_file.as_dict(lines_askeys = True)
fda_lines = fda_file.readlines()
fda_dict = fda_file2.as_dict(lines_askeys = True)
header,drugs_dict = drugs_file.as_dict(ret_header = True)
fda_cols_retained = ["SubmissionStatusDate", "SubmissionStatus", "SponsorName", "ActiveIngredient"]
app = "FDA_"
header.append("HAS_FDA_ENTRY")
for col in fda_cols_retained:
	header.append(app+col)
for key in drugs_dict.keys():
	# alias = ";".join([drugs_dict[key]["COMMON_DRUGBANK_ALIAS"],
	# 	drugs_dict[key]["MINED_ALIAS"]]) if drugs_dict[key]["MINED_ALIAS"] else drugs_dict[key]["COMMON_DRUGBANK_ALIAS"]
	alias = drugs_dict[key]["COMMON_DRUGBANK_ALIAS"]
	found_indexes = []
	for line in fda_lines:
		# if alias.lower() in line.lower():
		if any([a.lower() in line.lower() for a in alias.split(";")]):
			found_indexes.append(fda_lines.index(line))
	
	drugs_dict[key]["HAS_FDA_ENTRY"] = 0
	for col in fda_cols_retained:
		drugs_dict[key][app+col] = ""

	for i in found_indexes:
		drugs_dict[key]["HAS_FDA_ENTRY"] = 1
		for col in fda_cols_retained:
			if not drugs_dict[key][app+col]:
				drugs_dict[key][app+col] = fda_dict[i][col]
			else:
				drugs_dict[key][app+col] = ";".join([drugs_dict[key][app+col],fda_dict[i][col]])


header.append("FIRST_FDA_SubmissionStatusDate")
header.append("FIRST_DFA_SponsorName")

def try_parsing_date(text):
	for fmt in ("%d/%m/%Y %H:%M","%B %d %Y", "%b. %d %Y", "%b %Y" ,"%B %Y" , "%B %d%Y", "%B %Y", "%B%d %Y", "%B%d%Y"):
		try:
			return datetime.strptime(text, fmt)
		except ValueError:
			pass
	raise ValueError('no valid date format found')

for entry in drugs_dict.values():
	dates = entry[app+"SubmissionStatusDate"].split(";")
	sponsors = entry[app+"SponsorName"].split(";")
	dates_parsed = [try_parsing_date(date) for date in dates if date]
	min_index = dates_parsed.index(min(dates_parsed)) if dates_parsed!=[] else -1

	if min_index!=-1:
		entry["FIRST_FDA_SubmissionStatusDate"] = dates[min_index]
		entry["FIRST_FDA_SponsorName"] = sponsors[min_index]
	else:
		entry["FIRST_FDA_SubmissionStatusDate"] = ""
		entry["FIRST_FDA_SponsorName"] = ""


	entry[app+"SponsorName"] = ";".join(list(set(entry[app+"SponsorName"].split(";"))))
	entry[app+"ActiveIngredient"] = ";".join(list(set(entry[app+"ActiveIngredient"].split(";"))))
	entry[app+"SubmissionStatusDate"] = ";".join(list(set(entry[app+"SubmissionStatusDate"].split(";"))))
	entry[app+"SubmissionStatus"] = ";".join(list(set(entry[app+"SubmissionStatus"].split(";"))))


pool_file = FM("../FDA/FDA2018_by_drugbank2606",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/FDA")


pool_data = []

pool_data.append([head for head in header])

for entry in drugs_dict.values():
	pool_data.append([str(v) for v in entry.values()])


pool_file.set_datastream(pool_data)
pool_file.save()
pool_file.close()


control_file = FM("../FDA/FDA2018_by_drugbank2606_controlpos",
	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/FDA")


control_data = []

control_data.append(["COMMON_DRUGBANK_ALIAS","FDA_ActiveIngredient","OLDEST_PMID"])

for entry in drugs_dict.values():
	
	control_data.append([entry["COMMON_DRUGBANK_ALIAS"],
		entry["FDA_ActiveIngredient"], entry["OLDEST_PMID"]])



control_file.set_datastream(control_data)
control_file.save()
control_file.close()