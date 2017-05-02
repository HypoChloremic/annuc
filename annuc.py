# Nucleotide analysis from VCF files
# (c) 2017 Ali Rassolie
# Lumina sequencing


class annuc:
	def __init__(self, **kwargs):
		# Imports

		# Kwarg handling
		self.spec_input = kwargs["dictinput"]
		self.hass_input = kwargs["hass"]
		self.threads = kwargs["threads"]
		self.count = kwargs["count"]
		self.output = kwargs["output"]
		
		# where to start from. 
		self.pos_in_iter = 147
		self.endstart    = list()

	def specific_input(self):
		with open(self.spec_input, "r") as spec_file:	
			for spec_line in spec_file:
				temp_info = spec_line.split("\t")
				yield str(temp_info[0]), str(temp_info[1].replace("\n",""))

	def hass(self):
		with open(self.hass_input, "r") as hass_file:
			for i, line in enumerate(hass_file):

				if i > self.pos_in_iter:
					line = line.split("\t")
					temp = [ line[0],line[1], line[3], line[4] ]
					if self.chr_ and self.pos in temp:
						self.pos_in_iter = i
						yield temp
					else:
						pass	
				else:
					pass

	def chunk_search(self):
		import re, itertools

		with open(self.hass_input, "r") as file:
			while True:
				search_list = list(itertools.islice(file, 1000))
				if not search_list:
					break


				search_for = re.compile("{}\\t{}\\t.*".format(self.chr_, self.pos))
				finding = list(filter(search_for.match, search_list))
				if finding:
					finding_list = finding[0].split("\t")
					result = [finding_list[:3], finding_list[4:5]]
					yield result
				
				elif not finding:
					pass
				
				else:
					print("We have an issue")
					

	def filter_hassle(self):
		import time	
		with open(self.output, "w") as file:
			spec_gen = self.specific_input()
			hass_gen = self.hass()
			chunk_gen = self.chunk_search()
			try:
				text = ""
				count = 0
				start = time.time()
				start2 = time.time()
				for self.chr_, self.pos in spec_gen:
					append_this = next(self.hass())
					# append_this = next(self.chunk_search())
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

	def filter_chunk(self):
		import time	
		with open(self.output, "w") as file:
			spec_gen = self.specific_input()
			hass_gen = self.hass()
			chunk_gen = self.chunk_search()
			try:
				text = ""
				count = 0
				start = time.time()
				start2 = time.time()
				for self.chr_, self.pos in spec_gen:
					append_this = next(self.hass())
					# append_this = next(self.chunk_search())
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




	def plot_results(self, infile=None):
		import matplotlib.pyplot as plt
	


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

	def timed_completion(self):
		print(self.endstart)




if __name__ == '__main__':
	

	a = annuc(dictinput="cleaned_sample", hass="cleaned_hassle.vcf", threads=2, count=100, output="3.vcf")
	a.filter_hassle()
	a.timed_completion()
