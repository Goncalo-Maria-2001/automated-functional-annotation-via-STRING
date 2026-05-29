# Automated-functional-annotation-via-STRING

This script was used to batch query STRING's database for functional annotation, GO-term enrichment and protein interaction networks. Each query consists of the intersections of proteomes from different strains of the same bacterium in the context of all the observed strain's proteome for all studied cell sublocalizations. The goal was to better understand and characterize which biological processes are available for each strain or shared across strains and if there is a correlation between any of the strain's biological processes and it's pathogenecity. The program produces:

 - STRING .tsv enrichment tables,
 - STRING .png protein interaction network images,
 - Links to the STRING query performed on the STRING website

# Example Outputs

Excerpt of a STRING .tsv enrichment table:
```TSV
category	term	number_of_genes	number_of_genes_in_background	ncbiTaxonId	inputGenes	preferredNames	p_value	fdr	description
COMPARTMENTS	GOCC:0030313	5	18	176279	176279.SERP0574,176279.SERP1994,176279.SERP2288,176279.SERP2372,176279.SERP2398	oppA,SERP1994,SERP2288,SERP2372,aap	2.55e-05	0.0052	Cell envelope
COMPARTMENTS	GOCC:0030288	4	14	176279	176279.SERP0574,176279.SERP1994,176279.SERP2288,176279.SERP2372	oppA,SERP1994,SERP2288,SERP2372	0.00017	0.0121	Outer membrane-bounded periplasmic space
COMPARTMENTS	GOCC:0042597	5	26	176279	176279.SERP0574,176279.SERP1994,176279.SERP1999,176279.SERP2288,176279.SERP2372	oppA,SERP1994,SERP1999,SERP2288,SERP2372	0.00012	0.0121	Periplasmic space
Component	GO:0042597	3	3	176279	176279.SERP0574,176279.SERP1994,176279.SERP2372	oppA,SERP1994,SERP2372	8.28e-05	0.0052	Periplasmic space
Function	GO:0008924	4	4	176279	176279.SERP1955,176279.SERP2168,176279.SERP2312,176279.SERP2412	mqo-1,mqo-2,mqo-3,mqo-4	4.31e-06	0.0022	Malate dehydrogenase (quinone) activity
```

STRING .png protein interaction:

<img width="524" height="431" alt="11k-13k-RP-s14" src="https://github.com/user-attachments/assets/17f52af1-aeaa-4bd9-bf0e-c4fd92d999db" />

# Getting started

## 1. Clone the github repos:

```bash
git clone https://github.com/Goncalo-Maria-2001/automated-functional-annotation-via-STRING.git
cd automated-functional-annotation-via-STRING
```

## 2. Install dependencies:

Consider using a virtual environment using conda or venv to run the program and install dependencies

```bash
pip install -r requirements.txt
```

## 3. Verify instalation:

Check that everything is running smoothly with this example run:

```bash
python automated-functional-enrichment.py -p docs/examples -s 11k 13k -t 176279 -c 'placeholder id' -e -l
```

Please remember to provide a caller ID so as to satisfy STRING's user guidelines

The results will appear in the same directory and include one folder titled 'ID_tables' containing .csv tables with the protein IDs converted to STRING IDs, a folder titled 'Enrichment' containing the enrichment results for each proteome intersection and a .tsv file containing the links to all interection's STRING query respective pages. All folders contain results organized by subcellular localization and strain intersaction.

To see all available options check

```bash
python automated-functional-enrichment.py -h
```


# Function Overview


# Limitations

- The links provided expire after 2 days and must be generated again,
- Poor handling of edge cases and STRING errors or missing results.

# References
- STRING https://string-db.org
- PSORTb v3.0: N.Y. Yu, J.R. Wagner, M.R. Laird, G. Melli, S. Rey, R. Lo, P. Dao, S.C. Sahinalp, M. Ester, L.J. Foster, F.S.L. Brinkman (2010) PSORTb 3.0: Improved protein subcellular localization prediction with refined localization subcategories and predictive capabilities for all prokaryotes, Bioinformatics 26(13):1608-1615
- Venn diagram tool used: https://bioinformatics.psb.ugent.be/webtools/Venn/ (No citation available as of writing)
