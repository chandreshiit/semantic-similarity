The script contains code for finding semantic similarity between two sentences. The code is an implementation of the paper :
>@article{pawar2018calculating,
  title={Calculating the similarity between words and sentences using a lexical database and corpus statistics},
  author={Pawar, Atish and Mago, Vijay},
  journal={arXiv preprint arXiv:1802.05667},
  year={2018}
}

with little differences.  I have used default disambiguation function from pywsd library instead of max_similarity. 

### Dependency:
1. Python 3.5 or greater
2. Pywsd library

### To run:
just type python script name to run the file. Alternatively, you can call the getSimilarity function directly passing the two sentences being compared.
