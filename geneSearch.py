import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GeneReport():
    def __init__(self,gene):
        self.gene = gene
        self.geneID = self.getGeneID()
        self.diseaseInfoDict = {} 
        self.hpoAssociations = {} #Human Phenotype Ontology, get dict 'name' and 'definition'
        if self.geneID is not None:
            self.getGeneInfo()

    def getGeneID(self):
        response = requests.get('https://hpo.jax.org/api/hpo/search/?q={}&max=-1&offset=0&category=genes'.format(self.gene),verify=False).json()
        if response["genes"]:
            return response["genes"][0]['entrezGeneId']
        else:
            return None

    def getGeneInfo(self):
        response = requests.get("https://hpo.jax.org/api/hpo/gene/{}".format(self.geneID),verify=False).json()
        self.hpoAssociations = response["termAssoc"]
        self.diseaseInfoDict = response["diseaseAssoc"]
