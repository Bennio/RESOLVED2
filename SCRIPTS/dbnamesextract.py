from utils import File_Reader as FR
drugbank_alias_file = FR("../PUBMED_DATA/drugbank2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

drugbank_dict = drugbank_alias_file.as_dict()

drugbank_names = [key for key in drugbank_dict.keys()]
drugbank_names.sort()

for k in drugbank_names:
	print(k)