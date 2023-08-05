# QIIME 2 OMXWare plugin

This is a QIIME 2 plugin. For details on QIIME 2, see https://qiime2.org.

This plugin connects QIIME 2 with OMXWare, an IBM cloud platform to study microbial life at scale. This is the first implementation to retrieve genes based on given keyword/term. Expanded capabilities are soon to come.

## Install
Within the QIIME 2 environment and `q2_omxware` directory, install the plugin by running `python setup.py install`.

## Usage
To invoke this plugin from Python use:
```
import qiime2.plugins.omxware.actions as q2_omxware
genes_artifact = q2_omxware.genes(gene_names="<search-term>", genome_ids=[<genome-ids>], genus_names=[<genus-names>], go_terms=[<go-terms>], max_results=<int>)
```

Returns: QIIME 2 artifact of type FeatureData[Sequence]

To invoke this plugin from the command line:  
```qiime omxware genes --p-gene-names "<search-term>" --p-genome-ids="genome-ids" --p=genus-names="genus-names" --p-go-terms="go-terms" --p-max-results <int> --output-dir <output_directory path>```  
Returns: QIIME 2 artifact of type FeatureData[Sequence]

_Parameters:_  
`--p-gene-names` 
string or substring describing gene names of interest.

`--p-genome-ids`
comma separated list of genome ids

`--p-genus-names`
comma separated list of genus names

`--p-go-terms`
comma separated list of go terms

`--p-max-results` 
Integer value for number of results to return. Can be used to limit results while exploring query and results or set to maximum value for all results.


All of the parameters are optional, but at least one among gene_names, genome_ids, genus_names or go_terms is required

## Examples
`qiime omxware genes --p-gene-names "CONTAINS spore" --p-page-size 1000 --output-dir ./output` . 

`qiime omxware genes --p-gene-names "16S ribosomal RNA" --p-genus-names="salmonella,shigella,campylobacter" --p-max-results 1000 --output-dir ./output`
