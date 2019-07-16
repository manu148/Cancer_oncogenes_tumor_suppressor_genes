import sys
import os
import csv

data_sources = {
	"cosmic": "cosmic/cancer_gene_census.csv",
	"Science_Vogelstein_2013": "Science_Vogelstein_2013/1235122TablesS1-4.csv",
	"TSGene": "TSGene/Human_TSGs.txt",
	"ongene.bioinfo-minzhao.org": "ongene.bioinfo-minzhao.org/ongene_human.txt" 
}


gene_role_map = {}
def add_gene(gene, role):
	if role:
		role_bit = 0
		if role == "Oncogene" or role == "oncogene":
			role_bit = 1
		elif role == "TSG":
			role_bit = 2
		if role_bit:
			if gene not in gene_role_map:
				gene_role_map[gene] = 0
			gene_role_map[gene] = gene_role_map[gene] | role_bit

def parse_cosmic(file_name):
	with open(file_name) as inf:
		reader = csv.reader(inf)
		for row in reader:
			roles = row[14].split(',')
			for role in roles:
				role = role.strip()
				add_gene(row[0], role)	

def parse_science_vogelstein_2013(file_name):
	with open(file_name) as inf:
		reader = csv.reader(inf)
		for row in reader:
			add_gene(row[0], row[5].strip())
			
def parse_tsgene(file_name):
	with open(file_name) as inf:
		for line in inf:
			parts = line.split('\t')
			add_gene(parts[1], "TSG")

def parse_minzhao(file_name):
	with open(file_name) as inf:
		for line in inf:
			parts = line.split('\t')
			add_gene(parts[1], "Oncogene")

for data_source in data_sources:
	if data_source == "cosmic":
		parse_cosmic(data_sources[data_source])
	if data_source == "Science_Vogelstein_2013":
		parse_science_vogelstein_2013(data_sources[data_source])
	if data_source == "TSGene":
		parse_tsgene(data_sources[data_source])
	if data_source == "ongene.bioinfo-minzhao.org":
		parse_minzhao(data_sources[data_source])


def get_role_string(role):
	if role == 1:
		return "oncogene"
	if role == 2:
		return "TSG"
	if role == 3:
		return "both"

print "gene,role"		
for gene in gene_role_map:
	print gene + ',' +  get_role_string(gene_role_map[gene])