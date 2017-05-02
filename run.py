# Running annuc
# (c) 2017 Ali Rassolie

def run_annuc(searchtype=None, amount=2, header=None, taildata=None, tailsample=None):
	import annuc
	for pos_of_file in range(amount):
		output = "{}_{}_results.vcf".format(header, pos_of_file)
		hass_input = "{}_{}_{}".format(header, pos_of_file, taildata)
		spec_input = "{}_{}_{}".format(header, pos_of_file, tailsample)
		output_counter = "{}_{}_counter.vcf".format(header, pos_of_file)
		print(hass_input, spec_input)


		a = annuc.annuc(searchtype=searchtype, output=output, dictinput=spec_input, hass=hass_input)
		a.filter(slicesize=1)
		a.prod_counter(infile=output, outcountfile=output_counter)




if __name__ == '__main__':
	run_annuc(searchtype="hassle", header="malbac", tailsample="sampleoutput.vcf", taildata="vcfoutput.vcf", amount=2)