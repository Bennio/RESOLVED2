"""
Deuxieme pivot entre drugbank et druglist
"""

from utils import File_Reader as FR
from utils import File_Maker as FM
from utils import head
import re

pivot_file = FR("../DRUG_LISTS/drug_pivot_2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8",skiplines = 1)
bank_file = FR("../DRUGBANK/drugbank_extracted_identifiers.latest.txt",
	skiplines = 1, sep = '', suppress_newlines = True)


drug_data = pivot_file.readlines()
bank = bank_file.readlines()

head(drug_data)
head(bank)



match_file = FM("../PUBMED_DATA/pivot2606_in_drugbank",
	extension = ".txt", format = "csv", olddata_dir = "../OLD_DATA/PUBMED_DATA")
no_match_file = FM("../PUBMED_DATA/pivot2606_notin_drugbank",
	format = "csv", extension = ".txt", olddata_dir = "../OLD_DATA/PUBMED_DATA")


nm = []


none = 0

with match_file.get_filepointer() as fp:
	fp.write("DB_NAME	DB_SYNONYMS	DRUGNAMES	DB_PRODUCTS	DB_ID	CAS_NUMBER	UNII\n")
	for drugs in drug_data:
		DB_NAME = ""
		DB_SYNONYMS = ""
		DB_PRODUCTS = ""
		DB_ID = ""
		CAS_NUMBER = ""
		UNII = ""

		found = False
		alias = drugs[0].split(";")
		PRIMITIVE_COMPOUND = drugs[10]
		COMMON_DRUGBANK_ALIAS = drugs[11]
		COMMON_ALIAS = drugs[12]
		
		if PRIMITIVE_COMPOUND:
			alias.append(PRIMITIVE_COMPOUND)
		if COMMON_DRUGBANK_ALIAS:
			alias.append(COMMON_DRUGBANK_ALIAS)
		if COMMON_ALIAS:
			alias.append(COMMON_ALIAS)
		alias = list(set(alias))

		for d in alias:
			for line in bank:
				pat = r'\b'+re.escape(d.lower())+r'\b'
				if re.search(pat, line.lower()):
					DB_NAME = line.split('\t')[0]
					DB_SYNONYMS = line.split('\t')[1]
					DB_PRODUCTS = line.split('\t')[2]
					DB_ID = line.split('\t')[3]
					CAS_NUMBER = line.split('\t')[4]
					UNII = line.split('\t')[5]

					found = True
					break
				if found: break
			if found: break
		if not found:
			none+=1
			nm.append(drugs[0])
		else:
			fp.write("\t".join([DB_NAME, DB_SYNONYMS, drugs[0], DB_PRODUCTS, DB_ID, CAS_NUMBER, UNII])+'\n')
	fp.close()

print(none)

no_match_file.set_datastream(nm)

no_match_file.save()