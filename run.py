# Running annuc
# (c) 2017 Ali Rassolie
# Important to note that this has to be run in the command line environment
# bokeh serve --show first_plot.py


from collections import OrderedDict
from bokeh.charts import Bar, output_file, show
from bokeh.io import curdoc

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import annuc

class constants:
	counter_files = list()

def start_annuc(searchtype=None, amount=2, header=None, taildata=None, tailsample=None):
	
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



def histo_matplot(infile=None):

	with open(infile, "r") as file:
		info  = [ line.replace("\n", "") for line in file ]
		combo = [ combo.split("\t")[0] for combo in info  ]
		amount = [ float(appearances.split("\t")[1]) for appearances in info  ]
	data_as_dict = { combo[pos]: amount[pos] for pos in range(len(combo)) }
	base = range(len(combo))
	rects = plt.bar(base, amount, align="center", width=0.5)
	plt.xticks(base, combo)
	plt.ylabel("Number of appearances")
	plt.xlabel("Ref-Alt combination")
	plt.title("{}".format(infile))
	for rect in rects:
		height = rect.get_height()
		plt.text(rect.get_x() + rect.get_width()/2., 1.05*height,'%d' % int(height),ha='center', va='bottom')
	plt.show()

def histo_bokeh(infile=None):
	with open(infile, "r") as file:
		info  = [ line.replace("\n", "") for line in file ]
	
	combo = [ combo.split("\t")[0] for combo in info  ]
	amount = [ int(appearances.split("\t")[1]) for appearances in info  ]

	data_as_dict = { combo[pos]: amount[pos] for pos in range(len(combo)) }
	

	ordered_data_as_dict = OrderedDict(data_as_dict)
	ordered_data_as_dict = pd.Series(ordered_data_as_dict, index=ordered_data_as_dict.keys())
	bar = Bar(ordered_data_as_dict, title="Stacked bars")
	output_file("stacked_bar.html")
	curdoc().add_root(bar)
	show(bar)

histo_bokeh(infile="malbac_0_counter.vcf")


# histo_bokeh()
# Using this with bokeh, is not wanted.. took me hours to figure debug this. 
# Nothing was provided which made this clear
# if __name__ == '__main__':