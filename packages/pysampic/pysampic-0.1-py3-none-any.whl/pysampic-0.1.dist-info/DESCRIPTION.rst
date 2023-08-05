# SAMPIC DECODER 
The package `sampic_decoder` is a simple python packaged used to read 
the binary files produced with the SAMPIC board from LAL in python/numpy. 

It depends on numpy and runs with both Python2.7 and Python3.x. 

Example: 
	from pysampic import Dataset 

	ds = Dataset ( "sample.bin" ) 

	print (ds.keys()) #Prints the available keys 
	print (ds['HitNumber']) # Reads the hit numbers of all entries as a ndarray 


