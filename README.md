# ddRadSeqWebTool

This project is structured in a JavaScript frontend (see directory ./api/static/js) and a Python backend (see directory ./backend/service).
Backbone for this project is the Django framework.

## Frontend:

- beginnerForm.js:

	Script to build the form for the 'I have no idea!' section.

- dataFrame.js:

	Script to build the table for the results. Also includes the calculation of the following results of the table: No. SNPs in digestion, No. samples multiplexable, Sequencing efficiency, Fragments under x, Fragments under 2x.
	The calculation is done here, because of the size selection. 

- explanations.js:

	Script to build the explanation page.

- fileUpload.js:

	Script to manage the overall form (connected with the beginnerForm and tryOutForm).

- form.js:

	Script to build the form for the 'Lemme try out!' section.

- popovers.js:

	Script to build the popovers.

- screenUtils.js:

	Script to provide frontpage support.

- tryOutForm.js:

	Script to build the form for the 'Lemme try out!' section.

- util.js:

	Script to provide calculation support. Helps to calculate the results for the result table (see dataFrame.js)

## Backend:

The backend is responsible for uploading the genome file to the backend (django-chunkedupload), so it can be processed by the server:

- HandleFastafile.py:

	This script takes the fasta file and loops over it to cut it with the chosen restriction enzymes by using the DigestSequence file.
	The counted fragments are filtered for fragments having either restriction site end on each site.
	
	Depending on the chosen method, the method to count varies (one method for 'I have no idea!' and the other method for 'Lemme try out!')

- DigestSequence.py:

	This scripts provides the tools for the HandleFastafile section. Here, the fragments are cut in each scaffold and filtered for both ends of the restriction enzymes. The script finds for each restriction enzyme the cutting position and then the size is calculated. 
	The numbers of for each scaffold is then stored in a pandas dataFrame for further procession. Moreover, the number of base pairs are calculated in this script.
	

- DoubleDigestedDnaComparison.py:

	This script calculates the further results for the table, like the number of basepairs for each genome. It also filters for restriction enzyme pairs that does not have enough cut sizes for each restriction enzyme.
	Moreover, this script provides the graph presented in the website.

- ExtractRestrictionEnzymes.py:
	
	read in enzymes stored in csv

- ReadInJsonFiles.py:

	read in text stored in JSON files
