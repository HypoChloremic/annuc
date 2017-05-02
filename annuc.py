# Nucleotide analysis from VCF files
# (c) 2017 Ali Rassolie


import time	
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
					

	def filter(self):
		with open(self.output, "a") as file:
			spec_gen = self.specific_input()
			hass_gen = self.hass()
			try:
				text = ""
				count = 0
				start = time.time()
				for self.chr_, self.pos in spec_gen:
					append_this = next(self.hass())
					text = text + "{}\t{}\t{}\t{}\n".format(*append_this)
					if count == self.count:
						file.write(text)
						text = ""
						end = time.time()
						print(end-start)
						start = time.time()
						count = 0
					count += 1
			
			except Exception as e:
				print(e)





if __name__ == '__main__':
	a = annuc(dictinput="malbac_4_vcfoutput", hass="malbac_4.freebayes.bwa.vcf", threads=2, count=100, output="1.vcf")
	a.filter()




	# with open("malbac_4.freebayes.bwa.vcf", "r") as hass_file:
	# 	print(hass_file.tell())
		# a = hass_file.readlines(100000)
		# print(a)