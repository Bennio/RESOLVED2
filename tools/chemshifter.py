import pubchempy as pcp
import cirpy
import sys
import getopt


def usage():
	message = ['n']
	for m in message:
		notification(m)


def parseArgs(argv):
	global DB_EXTRACTION_FILE
	global DRUG_QUERY_FILE
	global DRUG_QUERY_LIST
	global QUIET
	global ENCODING

	try:
		opts, args = getopt.getopt(argv, 'd:D:b:o:E:s:S:hqaCf', ['druglist=', 'drugs=','extraction='
			'out=','encoding=','smiles=','smiles_list=','help', 'quiet'])
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
			DRUG_QUERY_FILE = arg
		elif opt in ('-D', '--drugs'):
			DRUG_QUERY_LIST.append(arg.split(COMMAND_LINE_SEP))
		elif opt in ('-b', '--extraction'):
			DB_EXTRACTION_FILE = arg
		elif opt in ('-x', '--query_file'):
			QUERY_FILE = arg
		elif opt in ('-o', '--outfile'):
			SAVE_FILE = arg
		elif opt in ('-q', '--quiet'):
			QUIET = True
		elif opt in ('-E', '--encoding'):
			ENCODING = arg
		elif opt in ('-s', '--smiles'):
			SMILES_QUERY_FILE = arg
		elif opt in ('-S', '--smiles_list'):
			SMILES_QUERY_FILE = arg

DB_EXTRACTION_FILE = "drugbank_extracted_identifiers.v_5.1.1.txt"

DRUG_QUERY_FILE = ""
DRUG_QUERY_LIST = []

SMILES_QUERY_FILE = ""
SMILES_QUERY_LIST = []

SAVE_FILE = ""

DRUGBANK = {}
HEADER = []

INTERACTIVE_MODE = False
FIND_MORE = True

QUIET = False

ENCODING = 'utf-8'
COMMAND_LINE_SEP = ';'


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
				ret[header[i]].append(line[i])
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



# Local Funcitons

def cirpy_getter(drug, request = 'names'):
	c = cirpy.resolve(drug, request)
	if c:
		return ";".join(c)
	else:
		return ""

def pcp_getter(drug, request = 'name'):
	p = pcp.get_synonyms(drug, request)
	if p:
		return ";".join(p[0]["Synonym"])
	else:
		return ""

def db_getter(drug, drugbank = DRUGBANK, header = HEADER):
	res = set()
	if not drug:
		return ''
	for nested in drugbank.keys():
		for field in drugbank[nested].keys():
			if drug.lower() in drugbank[nested][field].lower().split(";"):
				res.add(nested)

	if len(res)>1:
		notification("Warning, found multiple references in Drugbank for: "+drug, QUIET)
		return ";".join(list(res))
	elif len(res)==1:
		return ";".join(list(res))
	else:
		notification("Warning, found no references in Drugbank for: "+drug, QUIET)
		return ''

def query_drug(dql):
	res = [db_getter(q, drugbank = DRUGBANK, header = HEADER) for q in dql.split(";")]
	
	if FIND_MORE:
		for i in range(len(res)):
			if not res[i]:
				notification("Trying to find alternative aliases for: "+dql[i], QUIET)
				pub = pcp_getter(dql[i])
				cir = cirpy_getter(dql[i])
				alt = []
				alt.extend(pub.split(";"))
				alt.extend(cir.split(";"))
				if pub or cir:
					if pub:
						notification("Found following aliases in Pubchem: "+pub, QUIET)
					if cir:
						notification("Found following aliases with CIR: "+cir, QUIET)

					QUIET = True
					res[i] = ";".join(list(set([db_getter(q, drugbank = DRUGBANK, header = HEADER) for q in alt if db_getter(q, drugbank = DRUGBANK, header = HEADER)])))
					QUIET = False

				else:
					notification("No alternative aliases found :( ", QUIET)

	return res



if __name__ == '__main__':

	parseArgs(sys.argv[1:])

	if DB_EXTRACTION_FILE:
		notification("Using pre-extracted Drugbank file at: "+DB_EXTRACTION_FILE)
	else:
		notification("No pre-extracted Drugbank file found, please supply.")

	drugbank_file = File_Reader(DB_EXTRACTION_FILE,
		sep = '\t', skiplines = 0, encoding = ENCODING)

	DRUGBANK,HEADER = drugbank_file.as_dict(ret_header = True)

	# print(db_getter('DB00018', drugbank = DRUGBANK, header = HEADER))

	# notification("Quering Pubchem...")
	# DRUG_QUERY_LIST.append("CHEBI:6402")

	if DRUG_QUERY_FILE:
		drug_file = File_Reader(DRUG_QUERY_FILE,
			sep = '', skiplines = 0, encoding = ENCODING)

		DRUG_QUERY_LIST.extend(drug_file.readlines())
	if len(DRUG_QUERY_LIST)>0:
		res = [query_drug(q) for q in DRUG_QUERY_LIST]

		for r in res:
			sys.write.
	else:
		notification("Please supply some drugs to this tool.")