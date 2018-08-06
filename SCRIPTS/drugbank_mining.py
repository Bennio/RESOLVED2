from utils import File_Reader as FR
from utils import Task_Follower as TF
from utils import File_Maker as FM
from utils import head
import xml.etree.ElementTree as ET
import re
import pandas as pd

drugbank_alias_file = FR("../PUBMED_DATA/drugbank2606.latest.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0)

drugbank_dict = drugbank_alias_file.as_dict()

drugbank_names = [key for key in drugbank_dict.keys()]

XPaths_file = FR("../DRUGBANK/drugbank_mining_XPaths.txt",
	sep = "\t", suppress_newlines = True, encoding = "utf-8", skiplines = 0, comment_char = '#')

def prepared_XP(xpath, query, spliter = "*Query*"):
	escape_chars = ["'"]
	if any([c in query for c in escape_chars]):
		# query = "".join([c if c not in escape_chars else "\\'" for c in query])
		query = "'"+query+"'"
	if spliter in xpath:
		return query.join(xpath.split(spliter))
	else:
		return xpath

def gen_result_dataframe(command, query_list,
	auto_save = False, alter_colnames = False):

	xpath = command["QUERYS"]
	mode = command["MODE"]
	file_name = command["FILENAME"]
	BY_QUERY = command["BY_QUERY"]

	meta = (xpath, mode, file_name, BY_QUERY)

	if BY_QUERY:
		xpath = [xpath,BY_QUERY]
	procedure = {
		"tabled":tabled_mode,
		"listed":listed_mode,
		"fasta":fasta_mode,
		"crossed":crossed_mode
	}
	df,col_names = procedure[mode](xpath, query_list)
	col_names.sort()
	xpath = xpath[0]
	if alter_colnames:
		altered = []
		for i in range(len(col_names)):
			altered.append(":".join([file_name, col_names[i]]))
		for key in df.keys():
			for c in col_names:
				df[key][altered[col_names.index(c)]] = df[key].pop(c)
		col_names = altered

	if auto_save:
		if not file_name:
			file_name = "_".join(xpath.split("/")[2:])
		file_name = "drugbank_mining_"+file_name
		fmt = "" if mode=="fasta" else "tsv"
		save_file = FM("../DRUGBANK/VARIABLE_MINING/"+file_name,
			extension = ".txt", format = fmt, olddata_dir = "../OLD_DATA/DRUGBANK/VARIABLE_MINING")

		save_file.set_datastream(nested_dict_to_list(df, col_names,
			keep_colnames = False if mode=="fasta" else True))
		save_file.save()
		save_file.close()


	return df,col_names


def fasta_mode(xpath,query_list):
	df = {}
	col_names = set()

	for query in query_list:
		df[query] = {}
	
	q = TF(len(query_list), "Quering "+xpath+": ")
	key = xpath.split("/")[-1]
	for query in query_list:
		q.step()
		x = prepared_XP(xpath, query)
		df[query][key] = ""
		for res in [elem.text for elem in root.findall(x)]:
			if res:
				df[query][key] = '\n'+res+'\n' if not df[query][key] else df[query][key]+res+'\n'
				col_names.add(key)
	col_names = list(col_names)
	for res in col_names:
		for query in query_list:
			if res not in df[query]:
				df[query][res] = '\n'
	return df,col_names


def listed_mode(xpath,query_list):
	df = {}
	col_names = set()

	for query in query_list:
		df[query] = {}
	for xp in xpath.split(";"):
		q = TF(len(query_list), "Quering "+xp+": ")
		key = xp.split("/")[-1]
		for query in query_list:
			q.step()
			x = prepared_XP(xp, query)
			for res in [elem.text for elem in root.findall(x)]:
				if res:
					df[query][key] = res
					col_names.add(key)
	col_names = list(col_names)
	for res in col_names:
		for query in query_list:
			if res not in df[query]:
				df[query][res] = ""
	return df,col_names

def crossed_mode(xpath_cross,query_list):
	df = {}
	col_names = set()
	for query in query_list:
		df[query] = {}

	xpath = xpath_cross[0]
	cross = xpath_cross[1]

	q = TF(len(query_list), "Quering "+xpath+": ")

	for query in query_list:
		q.step()
		xp = prepared_XP(xpath, query)
		cr = prepared_XP(cross, query)

		for res in [elem.text for elem in root.findall(xp)]:
			if res:
				c = prepared_XP(cr, res, spliter = "*Cross*")
				df[query][res] = ";".join([elem.text for elem in root.findall(c)])
				col_names.add(res)
				# print(res)
				# print(df[query][res])

	col_names = list(col_names)

	for res in col_names:
		for query in query_list:
			if res not in df[query]:
				df[query][res] = ""

	return df,col_names



def tabled_mode(xpath,query_list):
	df = {}
	col_names = set()
	for query in query_list:
		df[query] = {}

	q = TF(len(query_list), "Quering "+xpath+": ")

	for query in query_list:
		q.step()
		xp = prepared_XP(xpath, query)

		for res in [elem.text for elem in root.findall(xp)]:
			if res:
				df[query][res] = 1
				col_names.add(res)

	col_names = list(col_names)

	for res in col_names:
		for query in query_list:
			if res not in df[query]:
				df[query][res] = 0

	return df,col_names



def nested_dict_to_list(df, header = [],
	infer_header = False, first_col_is_not_data = True, keep_colnames = True, metadata = ()):
	
	to_save = []
	cols = set()
	if infer_header:
		for nested_key in df.keys():
			for k in df[nested_key].keys():
				cols.add(k)
		header = sorted(list(cols)) 

	if header and keep_colnames:
		if first_col_is_not_data:
			to_save.append(['']+header)
		else:
			to_save.append(header)
	

	for nested_key in df.keys():
		line = []
		line.append(nested_key)
		for head in header:
			line.append(str(df[nested_key][head]))
		to_save.append(line)

	return to_save


print("parsing xml")
tree = ET.parse('../DRUGBANK/drugbank_db.xml')
root = tree.getroot()
print("done")


xpaths_to_process = XPaths_file.as_dict()


# df = gen_result_dataframe(xpaths_to_process[list(xpaths_to_process.keys())[-1]],
# 	drugbank_names, auto_save = True)
# df = gen_result_dataframe(xpaths_to_process[list(xpaths_to_process.keys())[-3]],
# 	drugbank_names, auto_save = True)
# df1 = gen_result_dataframe(xpaths_to_process[list(xpaths_to_process.keys())[8]], drugbank_names, auto_save = False)
# df2 = gen_result_dataframe(xpaths_to_process[list(xpaths_to_process.keys())[9]],
# 	drugbank_names, auto_save = False)
# for command in xpaths_to_process.values():
# 	df = gen_result_dataframe(command,
# 		drugbank_names, auto_save = True)


# datas =[]
# datas.append(df1)
# datas.append(df2)
# dii = df1.copy()

# dii.update(df2)
# res_dict = {}

# for i in drugbank_names:
# 	res_dict[i] = {}

def invertdict(df, cols):
	res = {}
	keys = []
	for k in df.keys():
		keys.append(k)
	keys.sort()
	res["Drugs"] = keys
	for c in cols:
		res[c] = []
		for kk in keys:
			res[c].append(df[kk][c])
	return(res)


datas = [gen_result_dataframe(command,
	drugbank_names, auto_save = False,
	alter_colnames = True) for command in xpaths_to_process.values()]


new_dicts = [invertdict(d[0], d[1]) for d in datas]

pds = [pd.DataFrame(d) for d in new_dicts]
res = pds[0]
for p in pds[1:]:
	res = pd.merge(res, p, on="Drugs")

res.to_csv("../DRUGBANK/VARIABLE_MINING/poolfile.txt", sep='\t', encoding='utf-8', index=False)

# col_names = []
# res_dict = datas[0][0].copy()
# for drugs in drugbank_names:
# 	for df in datas:
# 		res_dict[drugs].update(df[0][drugs])
# 		col_names.extend(df[1])


# merge_file = FM("../DRUGBANK/VARIABLE_MINING/poolfile",
# 	extension = ".txt", format = "tsv", olddata_dir = "../OLD_DATA/DRUGBANK/VARIABLE_MINING")

# merge_file.set_datastream(nested_dict_to_list(res_dict, header = col_names,
# 	keep_colnames = True))
# merge_file.save()
# merge_file.close()