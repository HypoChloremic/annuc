# Nucleotide analysis from VCF files
# (c) 2017	Ali Rassolie


class annuc:
	def __init__(self, **kwargs):
		self.spec_input = kwargs["dictinput"]
		self.hassle_input = kwargs["hassle"]
		self.threads = kwargs["threads"]
		# where to start from. 
		self.pos_in_iter = 147

	def specific_input(self):
		with open(self.spec_input, "r") as spec_file:	
			for spec_line in spec_file:
				temp_info = spec_line.split("\t")
				yield str(temp_info[0]), str(temp_info[1].replace("\n",""))

	def hassle(self):
		with open(self.hassle_input, "r") as hassle_file:
			for i, line in enumerate(hassle_file):
				
				if i > self.pos_in_iter:
					line = line.split("\t")
					temp = [ line[0],line[1], line[3], line[4] ]
					if self.chr_ and self.pos in temp:
						self.pos_in_iter = i
						yield temp
					else:
						self.i = i	
				else:
					self.i = i
					

	def filter(self):
		with open("defínitive_output_v3.vcf", "a") as file:
			spec_gen = self.specific_input()
			hassle_gen = self.hassle()
			try:
				while True:
					self.chr_, self.pos = next(spec_gen)
					append_this = next(self.hassle())
					text = "{}	{}	{}	{}\n".format(append_this[0],append_this[1],append_this[2],append_this[3])
					print(text)
					file.write(text)
			
			except Exception as e:
				print(e)





if __name__ == '__main__':
	a = annuc(dictinput="malbac_4_vcfoutput", hassle="malbac_4.freebayes.bwa.vcf", threads=2)
	a.filter()