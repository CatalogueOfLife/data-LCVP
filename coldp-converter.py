import sys, zipfile, csv, io, re, os
from pybtex.database.input import bibtex

BIB_FILE='raw_data_LCVP/LCVP_104_reference_list.bib'
ZIP_FILE='raw_data_LCVP/LCVP_104.zip'
DATA_FILE='LCVP_103.txt'


familyRefs={}

def idfy(name):
  return re.sub("[.&()]", "", name.replace(" ", "_"))

RE_CANONICAL_ID = re.compile('^.(?: ?[a-z._-]+)+')
def canonicalID(name):
  m = re.match(RE_CANONICAL_ID, name)
  if m:
    return idfy(m.group(0))
  return idfy(name)

RE_SPECIES_ID = re.compile('^(.[a-z._-]+ [a-z._-]+) [a-z.]{2,} ')
def speciesOrFamilyID(name, family):
  m = re.match(RE_SPECIES_ID, name)
  if m:
    return idfy(m.group(1))
  return family

def famRef(name):
  if family not in familyRefs:
    return ''
  else:
    return '|'.join(familyRefs[family])

# read references for families
print("Parsing family references...")
parser = bibtex.Parser()
bib_data = parser.parse_file(BIB_FILE)
for key in bib_data.entries:
  families=bib_data.entries[key].fields['keywords'] 
  for fam in families.split(","):
    fam=fam.strip()
    if fam not in familyRefs:
      familyRefs[fam]=[key]
    else:
      familyRefs[fam].append(key)


# normalize families & orders - dont write 
print("Writing species data...")
with zipfile.ZipFile(ZIP_FILE) as zf:
  with io.TextIOWrapper(zf.open(DATA_FILE), encoding="Latin-1") as f:
    with open('NameUsage.tsv', 'w') as tf:
      families={}
      orders={}
      writer = csv.writer(tf, delimiter='\t')
      writer.writerow(['ID', 'parentID', 'rank', 'scientificName', 'status', 'referenceID'])
      csv_reader = csv.reader(f, delimiter='\t')
      next(csv_reader)
      for line in csv_reader:

        # seen the family before?
        name=line[0]
        status=line[1] # ‘valid’, ‘synonym’, ‘unresolved’,  ‘external’ or ‘blanks’
        family=line[5]
        if family not in families:
          order=line[6]
          if order not in orders:
            orders[order]=True
            writer.writerow([order, '', "order", order, 'accepted', ''])
          families[family]=order
          writer.writerow([family, order, "family", family, 'accepted', famRef(family)])
        if status == 'synonym':
          writer.writerow([idfy(name), canonicalID(line[4]), '', name, status, ''])
        else:
          parent=speciesOrFamilyID(name, family)
          #print(name, "#", family, parent)
          writer.writerow([canonicalID(name), parent, '', name, status, ''])


# zip up nameusage, bibref & metadata
print("Bundling ZIP archive...")
coldp = zipfile.ZipFile('lcvp.zip', 'w', zipfile.ZIP_DEFLATED)
coldp.write('metadata.yaml')
coldp.write(BIB_FILE, arcname='reference.bib')
coldp.write('nameusage.tsv')
coldp.close()

print("Done. ColDP archive completed")
