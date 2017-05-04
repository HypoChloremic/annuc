# Nucleotide analysis from VCF files
# (c) 2017 Ali Rassolie
# Lumina sequencing


class annuc:
	def __init__(self, **kwargs):
		# Kwarg handling
		self.spec_input = kwargs["dictinput"]
		self.hass_input = kwargs["hass"]
		self.output		= kwargs["output"]
		self.searchtype = kwargs["searchtype"]
		self.endstart    = list()


	def clean(self, infile=None, max_=None, **kwargs):
		with open(infile, "rb") as file_in:
			with open("cleaned_{}".format(infile), "wb") as file_out:
				for i, line in enumerate(file_in):
					if i < max_:
						file_out.write(line)
					else:
						break

	def specific_input(self):
		with open(self.spec_input, "r") as spec_file:	
			for spec_line in spec_file:
				temp_info = spec_line.split("\t")
				yield str(temp_info[0]), str(temp_info[1].replace("\n",""))

	def hass(self):
		with open(self.hass_input, "r") as hass_file:
			for line in hass_file:
				line = line.split("\t")
				if len(line) >= 4:
					temp = [ line[0],line[1], line[3], line[4] ]
					if self.chr_ and self.pos in temp:
						yield temp
				


	def chunk_search(self):
		import re, itertools

		with open(self.hass_input, "r") as file:
			search_list = list(itertools.islice(file, self.slicesize))
			while True:
				
				if not search_list:
					break


				search_for = re.compile("{}\\t{}\\t.*".format(self.chr_, self.pos))
				finding = list(filter(search_for.match, search_list))
			
				if finding:
					finding_list = finding[0].split("\t")
					result = [finding_list[0],finding_list[1],finding_list[3],finding_list[4]]
					
					yield result
					
				elif not finding:
					
					search_list = list(itertools.islice(file, self.slicesize))
				
				else:
					print("We have an issue")
					


	def filter(self, slicesize):
		import time	
		self.slicesize = slicesize
		with open(self.output, "w") as file:
			spec_gen = self.specific_input()
			if self.searchtype == "hassle":
				gen = self.hass()
			elif self.searchtype == "chunk":
				gen = self.chunk_search()
			else:
				print("Please enter searchtype")
			try:
				text = ""
				count = 0
				start = time.time()
				start2 = time.time()
				for self.chr_, self.pos in spec_gen:
					append_this = next(gen)
					text = text+"{}\t{}\t{}\t{}\n".format( *append_this) # putting text inside format will slow down with 100%, needs inv.
					if count == 100:
						end2 = time.time()
						print(end2-start2)
						start2 = time.time()
						count = 0
					count += 1
				
				file.write(text)
				end = time.time()
				self.endstart = end - start
				
			except:
				raise Exception

	def prod_counter(self, infile=None, outcountfile=None):
		import matplotlib.pyplot as plt
		import numpy as np
		counts=dict()
		for element in self.basepair_gen(infile=infile):
			if element in counts:
				counts[element] += 1
			else:
				counts[element] = 1
		
		ordered_count = iter(counts)
		with open(outcountfile, "w") as file:
			for entry in ordered_count:
				text = "{}	{}\n".format(entry, counts[entry])
				file.write(text)
			
	def basepair_gen(self, infile=None):
		with open(infile, "r") as file:
			for line in file:
				line = line.replace("\n", "").split("\t")
				yield "{}{}".format(line[2],line[3])

	def timed_completion(self):
		return "Tot time: {}".format(self.endstart)

