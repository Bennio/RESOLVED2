import xml.etree.ElementTree as ET
import pandas as pd
import sys
import os
import getopt
import datetime

# Global vars
def usage():
	message = ['Descritption: Drugbank .xml mining tool by XPath queries supported by the ElementTree module of Python. Output is a pandas dataframe.',
	'\tUsage: -d <drug_list> -x <query_list> -b <drugbank.xml_file> -o <save_file>',
	'\tType --help for more details.']
	for m in message:
		notification(m)

def help():
	message = ['Descritption: Drugbank .xml mining tool by XPath queries supported by the ElementTree module of Python. Output is a pandas dataframe.',
	'\tInput:',
	'\t\t-d, --druglist: Path to file of Drugbank entities to query.',
	'\t\t-b, --drugbank: Path to drugbank xml file. Namespacing in xml file may mess up the parsing.',
	'\t\t-x, --query_file: Path to file of queries.',
	'\tOptions:',
	'\t\t-o, --out: Name of save file. If not supplied, the result can be redirected, but some may trigger issues with encoding and windows.',
	'\t\t-D, --drugs: Manually supply a \"'+COMMAND_LINE_SEP+'\" seperated list of entities to query.',
	# '\t\t-O, --old_dir: Directory of archived files.',
	'\t\t-Q, --Query: Manually supply a \"'+COMMAND_LINE_SEP+'\" seperated query.',
	'\t\t-E, --encoding: File encoding.',
	'\t\t-h, --help: Dispay info message.',
	'\t\t-q, --quiet: Suppress any progression messages.',
	'\t\t-a, --autosave: Saves individual dataframes for each query.',
	'\t\t-C, --nocolnamesadjustment: Suppress hanges to column names and use default result field.',
	'\t\t-f, --fasta: Outputs a fasta-like file for when quering sequences. Incompatible formating with normal output.',
	'\tQueries:',
	'\t\tA query consist of 4 ordered fields: XPATH, MODE, FILENAME, BY_QUERY.',
	'\t\tThe infile seperator is '+QUERY_SEP+'(tab) and the command line separator is '+COMMAND_LINE_SEP+'.',
	'\t\t\tXPATH: A valid ElementTree accepted XPath. Ex: ./drug[name="'+QUERY_SPLITTER+'"]/categories/category/category. '+QUERY_SPLITTER+' is used as a placeholder for inserting drugbank entities at run time.',
	'\t\t\tMODE: Format of results.',
	'\t\t\t\t-tabled: columns are the entity wide results and cells have value 1 if the field applies for the entity else 0.',
	'\t\t\t\t-listed: cells lists the result for each entity and columns correspond to each query.',
	'\t\t\t\t-fasta: similar to listed, by used to retrive fasta-like sequences and format them to fit in a dataframe. Use -f flag to keep the fasta format.',
	'\t\t\t\t-cross: used for when the column name and the desired infrormation are separeted. A second XPATH is supplied to target infrormation to search. Example of cross query: ./drug[name="*Query*"]/calculated-properties/property/kind;crossed;calculated-properties;./drug[name="*Query*"]/experimental-properties/property[kind="'+QUERY_SPLITTER_2+'"]/value. '+QUERY_SPLITTER_2+' is similarly as a placeholder.' ,
	'\t\t\tFILENAME: Filename of individual dataframe. Also used to distinguish columns for the final dataframe.',
	'\t\t\tBY_QUERY: Second XPath for cross mode.',
	'']
	for m in message:
		notification(m)

def parseArgs(argv):
	global QUEIT
	global DRUG_LIST_FILE
	global DRUG_LIST
	global DRUGBANK_FILE
	global QUERY_FILE
	global QUERY_LIST
	global QUERY_SEP
	global QUERY_MANUAL
	global QUERY_SPLITTER
	global QUERY_SPLITTER_2
	global SUPPRESS_ADJUST_COLNAMES
	global FASTA_SPLITTER
	global OUTPUT_AS_FASTA
	global AUTO_SAVE
	global SAVE_DIRECTORY
	global OLD_SAVE_DIRECTORY
	global SAVE_FILE
	global ENCODING

	if len(sys.argv[1:])==0:
		usage()
		sys.exit(2)
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'd:D:b:x:o:O:Q:E:hqaCf', ['druglist=', 'drugs=','drugbank=','query_file='
			'out=','old_dir=','Query=','encoding=','help', 'quiet','autosave','nocolnamesadjustment','-fasta'])
	except getopt.GetoptError:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt in ('-h'):
			usage()
			sys.exit(2)
		elif opt in ('--help'):
			help()
			sys.exit(2)
		elif opt in ('-d', '--druglist'):
			DRUG_LIST_FILE = arg
		elif opt in ('-D', '--drugs'):
			DRUG_LIST.append(arg.split(COMMAND_LINE_SEP))
		elif opt in ('-b', '--drugbank'):
			DRUGBANK_FILE = arg
		elif opt in ('-x', '--query_file'):
			QUERY_FILE = arg
		elif opt in ('-o', '--outfile'):
			SAVE_FILE = arg
		elif opt in ('-O', '--old_dir'):
			OLD_SAVE_DIRECTORY = arg
		elif opt in ('-Q', '--Query'):
			QUERY_MANUAL.extend(arg.split(COMMAND_LINE_SEP))
		elif opt in ('-q', '--quiet'):
			QUEIT = True
		elif opt in ('-a', '--autosave'):
			AUTO_SAVE = True
		elif opt in ('-E', '--encoding'):
			ENCODING = arg
		elif opt in ('-C', '--nocolnamesadjustment'):
			SUPPRESS_ADJUST_COLNAMES = True
		elif opt in ('-f', '--fasta'):
			OUTPUT_AS_FASTA = True
		else:
			usage()
			sys.exit(2)


QUEIT = False

DRUG_LIST_FILE = ""
DRUG_LIST = []

now = datetime.datetime.now()
DRUGBANK_FILE = ""

QUERY_FILE = ""
QUERY_LIST = []
QUERY_SEP = '\t'
QUERY_MANUAL = []
QUERY_SPLITTER = "*Query*"
QUERY_SPLITTER_2 = "*Cross*"

SUPPRESS_ADJUST_COLNAMES = False

FASTA_SPLITTER = ";"
OUTPUT_AS_FASTA = False

AUTO_SAVE = False
SAVE_DIRECTORY = ""
OLD_SAVE_DIRECTORY = ""
SAVE_FILE = ""

ENCODING = "utf-8"

COMMAND_LINE_SEP = ";"

CR_NL_REPLACE = '&#13;'
# XP_MANUAL = ""
# MODE_MANNUAL = ""
# FILENAME_MANNUAL = ""
# BY_QUERY_MANNUAL = ""

# Adding classes from utils module to avoid dependency

class File_Reader():
	"""Wrapper class for simple standard file reader (txt, csv, tsv...) with in-built generator.
	
	:param file_name: path to file
	:param sep: field seperator, none by default.
	:param suppress_newlines: Deletes \n at the end of every line, True by default
	:param skiplines: number of lines to skip, 0 by default
	:param strip_chars_pattern: regular expression for pattern deleting, none by default
	:param encoding: file encoding, utf8 by default

	:example:

	#Init
	my_file = File_Reader("path/to/file")
	#Read line by line
	for line in my_file.iter():
		do_something(line)

	my_file2 = File_Reader("path/to/file")
	#Get all lines in a python list
	all_lines = my_file2.readlines()
	"""
	def __init__(self, file_name, sep = "",
		suppress_newlines = True, skiplines = 0,
		strip_chars_pattern = "", encoding = "",
		comment_char = "#"):

		self.file_name = file_name
		self.sep = sep
		self.suppress_newlines = suppress_newlines
		self.skiplines = skiplines
		self.strip_chars_pattern = strip_chars_pattern
		self.encoding = encoding if encoding else "utf-8"
		self.comment_char = comment_char

	def char_strip(self,string, pattern):
		return re.sub(pattern, '', string)

	def iter(self):
		
		self.fp = open(self.file_name, encoding = self.encoding)
		self.line = self.fp.readline()

		for i in range(self.skiplines):
			self.line = self.fp.readline()

		while self.line:
			
			if self.comment_char:
				while self.line[0:len(self.comment_char)]==self.comment_char:
					self.line = self.fp.readline()
				if not self.line:
					break


			if self.suppress_newlines:
				self.line = self.line[:-1]

			if self.sep:
				self.line = self.line.split(self.sep)
				if self.strip_chars_pattern:
					for i in range(len(self.line)):
						self.line[i] = self.char_strip(self.line[i], self.strip_chars_pattern)
			
			if self.strip_chars_pattern and type(self.line)!=list:
				self.line = self.char_strip(self.line, self.strip_chars_pattern)

			yield self.line
			self.line = self.fp.readline()

		self.fp.close()

	def readlines(self):
		text = []
		for self.line in self.iter():
			text.append(self.line)
		return(text)

	def as_dict(self, header = "", key_column = 0, lines_askeys = False, ret_header = False):
		lines = self.readlines()
		ret = {}
		gen = (l for l in range(0,len(lines)))
		if not header:
			header = lines.pop(0)
		for line in lines:
			n = next(gen)
			if not lines_askeys:
				ret[line[key_column]] = {}
			else:
				ret[n] = {}

			for i in range(len(header)):
				if not lines_askeys:
					ret[line[key_column]][header[i]] = line[i]
				else:
					ret[n][header[i]] = line[i]
		if ret_header:
			return ret,header
		else:
			return ret

	def as_pandas_dict(self, header = "", ret_header = False):
		lines = self.readlines()
		ret = {}
		gen = (l for l in range(0,len(lines)))
		if not header:
			header = lines.pop(0)
		for h in header:
			ret[h] = []
		for line in lines:
			n = next(gen)
			for i in range(len(line)):
				ret[header[i]] = line[i]
		if ret_header:
			return ret,header
		else:
			return ret

class Task_Follower():
	"""Mini barre de progression en pourcentage pour les executions linéaire longues.

	#initialiser avec le nombre d'opérations
	t = Task_Follower(count)
	#incrémenter l'avencement
	t.step()
	"""
	def __init__(self, taskcount, message = "Completion: ", quiet = False):
		self.taskcount = taskcount-1
		self.done = 0
		self.message = message
		self.gen = self.ini()
		self.quiet = quiet

	def ini(self):
		return self.next()

	def step(self):
		notification(next(self.gen), self.quiet, suppress_newline = True)
		if self.taskcount <= self.done:
			notification('\n', self.quiet)

	def next(self):
		while self.done < self.taskcount+1:
			yield str('\r'+self.message + "%.2f" % (100*self.done/self.taskcount))
			self.done+=1
		# while True:
		# 	yield "Task Done!\n"
		return("\nTask Done")

class File_Maker():
	'''Wrapper class for simple file writting with version control. Auto-renaming of files to keep old files.
	The last file will be tagged .latest (by default) et previous versions with a number (.1, .2, .3, etc).
	The current working directory is the directory where the file is being saved.

	:param path: path to save file WITHOUT extension and NO tags. Supply the extension in parameters. 
	:param data_stream: If not empty, will be written to the file with the save() method.
	:param format: define the field separator for save() method. By default "". Other supported formats are csv, tsv et "".
	:param extension: extension of save file. If none given, it will be infered with the path name or the format.
	:param encoding: file encoding.
	:param latest_string: Last version annotation tag. ".latest" by default.
	:param olddata_dir: If given, path to directory where current ".latest" version will be moved. Number tags
	will be added as needed.

	:example:

	from utils import File_Maker as FM

	data = [["This", "is"], "my", 'data']
	
	# Init
	# Moving and renaming old files is only done when save() or get_filepointer() are called.
	save_file = FM("../test", data_stream = data, extension = ".txt", olddata_dir = "../OLD_DATA/") 

	# Writting data in ../test.latest.txt
	save_file.save()

	# Get the file pointer for further operations.	
	with save_file.get_filepointer() as fp:
		fp.write("adzaf")
		fp.write("sth")
		fp.write("rthter")
		fp.write("rthet")
		fp.close()
	# File pointer disapears when close() is called.
	'''
	def __init__(self, path, data_stream = "", format = "tsv", extension = "", encoding = "utf-8",
	latest_string = ".latest", olddata_dir = ""):
	
		self.path = path
		
		self.file_name = self.get_filename()

		self.extension = extension
		if not extension:
			self.extension = self.get_extension()
			if not self.extension:
				self.extension = "."+format

		self.olddata_dir = os.path.abspath(olddata_dir)
		self.current_script_dir = os.getcwd()

		self.set_savedir()

		# self.replace_old = replace_old
		# self.version_control = version_control

		self.mode = "w"
		self.encoding = encoding

		if self.mode is not 'a' and self.mode is not 'w':
			notification("Warning, file oppening mode is not supported.")

		
		self.fp = None
		self.data_stream = data_stream

		self.format = format

		self.format_dict = {
		"tsv":'\t',
		"csv":';',
		"":""
		}

		self.sep = self.format_dict[format]
		self.latest_string = latest_string


	def get_filename(self):
		name = (self.path.split("/")[-1])
		if '.' in name:
			name = ".".join(name.split('.')[0:-1])
		return name

	def get_extension(self):
		ext = self.path
		if ".." in ext:
			ext = self.path.split("..")[-1]

		if '.' in ext:
			ext = ext.split(".")[-1]
			return "."+ext
		return ""

	def set_datastream(self, data_stream):
		self.data_stream = data_stream

	def set_savedir(self):
		sd_path = self.path.split("/")[0:-1]
		if len(sd_path) is not 0:
			os.chdir("/".join(sd_path))

	def get_filepointer(self):
		if self.fp:
			return self.fp

		save_name = self.file_name+self.latest_string+self.extension

		if not self.olddata_dir:
			files = [f for f in os.listdir() if os.path.isfile(f)]

			if save_name in files:
				i = 1
				rename = save_name
				while rename in files:
					rename = self.file_name+"."+str(i)+self.extension
					i+=1
				os.rename(save_name, rename)

		else:
			dest_files = [f for f in os.listdir(self.olddata_dir) if os.path.isfile(os.path.join(self.olddata_dir,f))]
			local_files = [f for f in os.listdir() if os.path.isfile(f)]	

			if save_name in local_files:
				i = 1
				rename = self.file_name+"."+str(i)+self.extension
				while rename in dest_files:
					rename = self.file_name+"."+str(i)+self.extension
					i+=1
				new_path = os.path.join(self.olddata_dir,rename)
				os.rename(save_name, new_path)

		self.fp = open(save_name, self.mode, encoding = self.encoding)
		return self.fp


	def save(self):
 
		if not self.fp:
			self.fp = self.get_filepointer()

		if self.data_stream and self.fp:
			for i in self.data_stream:
				if type(i) is not str:
					self.fp.write(self.sep.join(i)+'\n')
				else:
					self.fp.write(i+'\n')

		else:
			notification("Missing/Incorrect data_stream or no file to write to.\n")

		os.chdir(self.current_script_dir)
		

	def close(self):
		if self.fp:
			self.fp.close()
			self.fp = None
		else:
			notification("Can't close undefined file pointer.\n")
			
		os.chdir(self.current_script_dir)

# Utility Funcitons

def head(l, start = 0, stop = 5):
	"""Equivalent de l'outil linux head."""
	print(l[start:stop])

def qprint(message, quiet):
	if not quiet:
		print(message)

def qsys_out(message, quiet):
	if not quiet:
		sys.stdout.write(message)
		sys.stdout.flush()

def notification(message, quiet = False, suppress_newline = False):
	message = str(message)
	if not message:
		sys.stderr.write('\n')
		sys.stderr.flush()
		return
	if not suppress_newline and message[-1]!='\n':
		message+='\n'
	if not quiet:
		sys.stderr.write(message)
		sys.stderr.flush()


# Local Functions
def strip_newline(s, strip = CR_NL_REPLACE):
	while '\r\n' in s:
		s = s.replace('\r\n', CR_NL_REPLACE)
	while '\n' in s:
		s = s.replace('\n', CR_NL_REPLACE)
	return s

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

def prepared_XP(xpath, query, spliter = QUERY_SPLITTER):
	escape_chars = ["'"]
	if any([c in query for c in escape_chars]):
		# query = "".join([c if c not in escape_chars else "\\'" for c in query])
		query = "'"+query+"'"
	if spliter in xpath:
		return query.join(xpath.split(spliter))
	else:
		return xpath

def gen_result_dataframe(command, query_list,
	auto_save = AUTO_SAVE, adjust_colnames = not SUPPRESS_ADJUST_COLNAMES):

	xpath = command[0]
	mode = command[1]
	file_name = command[2]
	BY_QUERY = command[3]

	if not mode:
		notification("Incorrect or missing result format. Using listed mode by default.")
		mode = "listed"

	if mode=="crossed":
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

	if adjust_colnames:
		altered = []
		for i in range(len(col_names)):
			altered.append(":".join([file_name, col_names[i]]))
		for key in df.keys():
			for c in col_names:
				df[key][altered[col_names.index(c)]] = df[key].pop(c)
		col_names = altered

	if AUTO_SAVE:
		if not file_name:
			file_name = "_".join(xpath.split("/")[2:])
		file_name = "drugbank_mining_"+file_name
		notification("Saving at "+file_name, QUEIT)
		fmt = "" if mode=="fasta" else "tsv"
		save_file = File_Maker(SAVE_DIRECTORY+file_name,
			extension = ".txt", format = fmt, olddata_dir = OLD_SAVE_DIRECTORY)

		save_file.set_datastream(nested_dict_to_list(df, col_names,
			keep_colnames = False if mode=="fasta" else True))
		save_file.save()
		save_file.close()

	i = invertdict(df, col_names)
	return pd.DataFrame(i)

def fasta_mode(xpath,query_list):
	df = {}
	col_names = set()

	for query in query_list:
		df[query] = {}
	
	q = Task_Follower(len(query_list), "Quering "+xpath+": ", QUEIT)
	key = xpath.split("/")[-1]
	for query in query_list:
		q.step()
		x = prepared_XP(xpath, query)
		df[query][key] = ""
		for res in [elem.text for elem in root.findall(x)]:
			if res:
				if not OUTPUT_AS_FASTA:
					res = res.replace('\n', FASTA_SPLITTER)
					df[query][key] = res if not df[query][key] else df[query][key]+res
				else:
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
		q = Task_Follower(len(query_list), "Quering "+xp+": ", QUEIT)
		key = xp.split("/")[-1]
		for query in query_list:
			q.step()
			x = prepared_XP(xp, query)
			df[query][key] = ""
			for res in [elem.text for elem in root.findall(x)]:
				if res:
					res = strip_newline(res)
					df[query][key] = res if not df[query][key] else ";".join([df[query][key], res])
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

	q = Task_Follower(len(query_list), "Quering "+xpath+": ", QUEIT)

	for query in query_list:
		q.step()
		xp = prepared_XP(xpath, query)
		cr = prepared_XP(cross, query)

		for res in [elem.text for elem in root.findall(xp)]:
			if res:
				c = prepared_XP(cr, res, spliter = QUERY_SPLITTER_2)
				res = strip_newline(res)
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

	q = Task_Follower(len(query_list), "Quering "+xpath+": ", QUEIT)

	for query in query_list:
		q.step()
		xp = prepared_XP(xpath, query)

		for res in [elem.text for elem in root.findall(xp)]:
			if res:
				res = strip_newline(res)
				df[query][res] = 1
				col_names.add(res)

	col_names = list(col_names)

	for res in col_names:
		for query in query_list:
			if res not in df[query]:
				df[query][res] = 0

	return df,col_names



if __name__ == '__main__':

	parseArgs(sys.argv)

	notification("Parsing Drugbank xml file at: "+DRUGBANK_FILE, QUEIT)
	tree = ET.parse(DRUGBANK_FILE)
	root = tree.getroot()
	notification("Done.", QUEIT)

	if QUERY_FILE:
		XPaths_file = File_Reader(QUERY_FILE,
			sep = QUERY_SEP, encoding = ENCODING, skiplines = 0, suppress_newlines = True)
		tmp_QUERY_LIST = XPaths_file.readlines()
		if "\t".join(tmp_QUERY_LIST[0])=="QUERYS	MODE	FILENAME	BY_QUERY":
			tmp_QUERY_LIST.pop(0)
		
		# QUERY_LIST = [["","","",""] for i in range(len(tmp_QUERY_LIST))]
		# for i in range(len(tmp_QUERY_LIST)):
		# 	for j in range(len(tmp_QUERY_LIST[i])):
		# 		QUERY_LIST[i][j] = tmp_QUERY_LIST[i][j]
		if QUERY_MANUAL:
			tmp_QUERY_LIST.extend([q.split("\t") for q in QUERY_MANUAL])

		for q in tmp_QUERY_LIST:
			for i in range(4-len(q)):
				q.append("")
			QUERY_LIST.append(q)

	if DRUG_LIST_FILE:
		drugbank_alias_file = File_Reader(DRUG_LIST_FILE,
			encoding = ENCODING)
		DRUG_LIST.extend(drugbank_alias_file.readlines())
	else:
		notification("No list of Drugs supplied, exiting...")
		exit()


	df_res = [gen_result_dataframe(query, DRUG_LIST) for query in QUERY_LIST]

	res = df_res[0]
	if len(df_res)>1:
		for p in df_res[1:]:
			res = pd.merge(res, p, on="Drugs")

	if SAVE_FILE:
		# dummy_file = File_Maker(SAVE_FILE, latest_string = "")
		# dummy_file.save() 
		# dummy_file.close()

		res.to_csv(SAVE_FILE, sep='\t', encoding=ENCODING, index=False, quoting = 0)

	else:
		sys.stdout.write(res.to_csv(None, sep='\t', encoding=ENCODING, index=False, quoting = 0).encode(ENCODING).decode(sys.stdout.encoding))
		sys.stdout.flush()
