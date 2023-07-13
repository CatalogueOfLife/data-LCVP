# LCVP -> ColDP
R script to convert the Leipzig Plant Catalogue (LCVP) into a ColDP archive suitable for [ChecklistBank](https://www.checklistbank.org).

# Installation
Install R, devtools and LCVP:

```r
install.packages("devtools")
devtools::install_github("idiv-biodiversity/LCVP")
install.packages("stringr")
```

# Build archive

Convert the LCVP data frame into a ColDP compliant one.
TODO: keep unique reference citations in a Reference.csv file

```r
library(LCVP)
library("stringr")
outputFile="/tmp/lcvp/NameUsage.csv"

buildSciName <- function(name){
  str_trim(str_replace_all(name, "([^ ]+)_x\\b", "×\\1"))
}
buildParentID <- function(parentID, status){
	if (exists("parentID") & exists("status")) {
		if (length(status)>1) {
			print (status)
		} else {
			if (status == "synonym") {
				return (parentID)
			}
		}
	}
	return(NULL)
}

write.csv(data.frame(ID=tab_lcvp$global.Id,
		parentID=tab_lcvp$globalId.of.Output.Taxon,
		status=tab_lcvp$Status,
		rank=tab_lcvp$Rank, 
		genericName=buildSciName(tab_lcvp$Input.Genus), 
		specificEpithet=buildSciName(tab_lcvp$Input.Epitheton), 
		infraspecificEpithet=buildSciName(tab_lcvp$Input.Subspecies.Epitheton), 
		authorship=tab_lcvp$Input.Authors, 
		family=tab_lcvp$Family, 
		order=tab_lcvp$Order, 
		publishedIn=tab_lcvp$Literature, 
		acceptedName=tab_lcvp$Output.Taxon, 
		remarks=tab_lcvp$Comments
	), 
	file=outputFile,
	fileEncoding = "UTF-8",
	row.names=FALSE,
	na=''
)
```
