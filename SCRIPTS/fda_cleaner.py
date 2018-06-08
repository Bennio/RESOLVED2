'''
Cleaning of the fda database.
Specifically extra trailling spaces and tabs.
'''

from utils import File_Reader as FR


charstrip = "^[ ]+|[ ]+$"
fda_file = FR("../FDA/FDA_DRUG_DATABASE_cured.txt", encoding = "utf-16", sep = "\t", strip_chars_pattern = charstrip)


fda = []
for f in fda_file.iter():
	fda.append(f[:5])

print(fda)


with open("../FDA/FDA_DRUG_DATABASE_cured_cleaned.latest.txt", 'w', encoding = 'utf-8') as fp:
	for i in fda:
		fp.write("\t".join(i)+'\n')