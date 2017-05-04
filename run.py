# Running annuc
# (c) 2017 Ali Rassolie


class constants:
	counter_files = list()

def run_annuc(searchtype=None, amount=2, header=None, taildata=None, tailsample=None):
	import annuc


	for pos_of_file in range(amount):
		output = "{}_{}_results.vcf".format(header, pos_of_file)
		hass_input = "{}_{}_{}".format(header, pos_of_file, taildata)
		spec_input = "{}_{}_{}".format(header, pos_of_file, tailsample)
		output_counter = "{}_{}_counter.vcf".format(header, pos_of_file)
		print(hass_input, spec_input)
		constants.counter_files.append(output_counter)

		a = annuc.annuc(searchtype=searchtype, output=output, dictinput=spec_input, hass=hass_input)
		a.filter(slicesize=1)
		a.prod_counter(infile=output, outcountfile=output_counter)

def histogram_plot(infile=None):
	import matplotlib.pyplot as plt
	import numpy as np 

	with open(infile, "r") as file:
		info  = [ line.replace("\n", "") for line in file ]
		combo = [ combo.split("\t")[0] for combo in info  ]
		amount = [ float(appearances.split("\t")[1]) for appearances in info  ]
	base = range(len(combo))
	rects = plt.bar(base, amount, align="center", width=0.5)
	plt.xticks(base, combo)
	plt.ylabel("Occurences")
	plt.xlabel("Nucleotide transitions in variant cells uniquely detected in single cells")
	plt.title("{}".format(infile))
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')
	plt.show()

if __name__ == '__main__':
	import argparse as ap

	the_arguments = ap.ArgumentParser(
		prog="NUCLEOTIDE ANALYSIS")

	the_arguments.add_argument("-n", "--number",  help="Number of files", nargs=1)

	# Storing the parsed arguments
	opts = the_arguments.parse_args()
	try:
		number = int(opts.number[0]) 
	except Exception as e:
		raise e

	run_annuc(searchtype="hassle", header="malbac", tailsample="sampleoutput.vcf", taildata="vcfoutput.vcf", amount=number)
	for file in constants.counter_files:
		histogram_plot(infile=file)
