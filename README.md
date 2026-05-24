# Automated-functional-annotation-via-STRING

A python script used to batch query STRING's database for functional annotation, GO-term enrichment and protein interaction networks of a given sub-cellular localization from a given strain's proteome in the context of all the observed strain's proteome for the given cell sublocalization. The program produces:

 - STRING .tsv enrichment tables,
 - STRING .svg enrichment figures,
 - STRING .png protein interaction network images,
 - Links to the STRING query performed on the STRING website

# Example Outputs

```
category	term	number_of_genes	number_of_genes_in_background	ncbiTaxonId	inputGenes	preferredNames	p_value	fdr	description
COMPARTMENTS	GOCC:0030313	5	18	176279	176279.SERP0574,176279.SERP1994,176279.SERP2288,176279.SERP2372,176279.SERP2398	oppA,SERP1994,SERP2288,SERP2372,aap	2.55e-05	0.0052	Cell envelope
COMPARTMENTS	GOCC:0030288	4	14	176279	176279.SERP0574,176279.SERP1994,176279.SERP2288,176279.SERP2372	oppA,SERP1994,SERP2288,SERP2372	0.00017	0.0121	Outer membrane-bounded periplasmic space
COMPARTMENTS	GOCC:0042597	5	26	176279	176279.SERP0574,176279.SERP1994,176279.SERP1999,176279.SERP2288,176279.SERP2372	oppA,SERP1994,SERP1999,SERP2288,SERP2372	0.00012	0.0121	Periplasmic space
Component	GO:0042597	3	3	176279	176279.SERP0574,176279.SERP1994,176279.SERP2372	oppA,SERP1994,SERP2372	8.28e-05	0.0052	Periplasmic space
Function	GO:0008924	4	4	176279	176279.SERP1955,176279.SERP2168,176279.SERP2312,176279.SERP2412	mqo-1,mqo-2,mqo-3,mqo-4	4.31e-06	0.0022	Malate dehydrogenase (quinone) activity
```

# Getting Started

# Function Overview

# Limitations

