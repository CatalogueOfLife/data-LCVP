# LCVP v1.0.4
This is a COL fork of the original R datapackage of the Leipzig Plant Catalogue described in https://doi.org/10.1038/s41597-020-00702-z.
It adds a python script to convert the raw data into a valid Catalogue of Life Data Package (ColDP) suitable for ingestion into COL ChecklistBank where it is hosted at https://data.catalogueoflife.org/dataset/2262/.

# Python Converter Usage

## Requirements
pip install pybtex

## Run ColDP conversion
This makes use of the zipped data and the bibtex citation and references file.
It will generate distinct families in ColDP with references attached.
It then places all the species in those families.

> $ python3 coldp-converter.py
