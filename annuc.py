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
		self.pos_in_iter = 147
		self.endstart    = list()


	def clean(self):
		with open("malbac_4.freebayes.bwa.vcf", "rb") as file_in:
			with open("cleaned_hassle.vcf", "wb") as file_out:
				for i, line in enumerate(file_in):
					if i < 50000:
						file_out.write(line)
					else:
						break
		with open("malbac_4_vcfoutput", "rb") as file_in:
			with open("cleaned_sample", "wb") as file_out:
				for i, line in enumerate(file_in):
					if i < 10000:
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
			for i, line in enumerate(hass_file):
				line = line.split("\t")
				if len(line) >= 4:
					temp = [ line[0],line[1], line[3], line[4] ]
					if self.chr_ and self.pos in temp:
						self.pos_in_iter = i
						yield temp
				else:
					pass


	def chunk_search(self):
		import re, itertools

		with open(self.hass_input, "r") as file:
			search_list = list(itertools.islice(file, self.slicesize))
			while True:
				# print("wut")
				if not search_list:
					break


				search_for = re.compile("{}\\t{}\\t.*".format(self.chr_, self.pos))
				finding = list(filter(search_for.match, search_list))
				# print(finding)
				if finding:
					finding_list = finding[0].split("\t")
					result = [finding_list[0],finding_list[1],finding_list[3],finding_list[4]]
					# print(result)
					yield result
					# print("2")
				elif not finding:
					# print("no finding")
					search_list = list(itertools.islice(file, self.slicesize))
				
				else:
					print("We have an issue")
					


	def filter(self, slicesize):
		import time	
		self.slicesize = slicesize
		# for pos_of_file in range(self.amount):
			# self.output = "{}_{}_results.vcf".format(self.header, pos_of_file)
			# self.hass_input = "{}_{}_{}".format(self.header, pos_of_file, self.taildata)
			# self.spec_input = "{}_{}_{}".format(self.header, pos_of_file, self.tailsample)
			# print(self.hass_input, self.spec_input)


		with open(self.output, "w") as file:
			spec_gen = self.specific_input()
			if self.searchtype == "hassle":
				gen = self.hass()
			elif self.searchtype == "chunk":
				gen = self.chunk_search()
			else:
				print("Please enter searchtype:")
			try:
				text = ""
				count = 0
				start = time.time()
				start2 = time.time()
				for self.chr_, self.pos in spec_gen:

					append_this = next(gen)
					# print(append_this)
					text = text + "{}\t{}\t{}\t{}\n".format(*append_this)
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

	def timed_completion(self):
		print("Tot time: {}".format(self.endstart))

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

