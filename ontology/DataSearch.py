import os
import xml.etree.ElementTree as ET
import re
from unicodedata import normalize
from difflib import SequenceMatcher


class DataSearch:

    def __init__(self):
        cwd = os.getcwd()
        self.root = ET.parse(cwd + '/utils/cti.owl').getroot()

    def search(self, toSearch):     
        self.data(toSearch)
        print("toSearch: {}".format(toSearch))
        

    def lemmatization(self, name):
        
        lemma = []
        for i in name:
            lemma.append(normalize("NFD", i).encode("ascii", "ignore").decode("utf-8").lower())
        return lemma

    def similary(self, a, b):
        similary = SequenceMatcher(None,a,b).ratio()

        return similary

    def likehood(self, name_1, name_2):
        c = 0
        sumSimilary = 0

        for i in name_1:
            for j in name_2:
                similary = self.similary(i, j)
                sumSimilary+=similary
                c+=1

                if similary > 0.9:
                    name_2.remove(j)
                    break

        totalSimilary = sumSimilary/c

        return totalSimilary

    def data(self, toSearch):

        datas = {'Name': None, 'Divisao': None, 'Ramal': None, 'E-mail': None}
        name = toSearch['names']
        tags = {'D': toSearch['D'], 'R': toSearch['R'], 'E': toSearch['E']}
        n_names = False
        
        self.listData = []  

        #self.listData.append(tags)


        name = name.split()  

        name = self.lemmatization(name)

        for person in self.root.findall('{http://www.w3.org/2002/07/owl#}NamedIndividual'):
            nameBase = person.find('{http://people.cti.gov.br/~paulo/cti.owl#}nome_completo')

            if(nameBase is not None):
                fullName = re.split("\s",nameBase.text)  

                fullNameLemma = self.lemmatization(fullName)

                compatibility = self.likehood(name, fullNameLemma)

                if compatibility > 0.6:

                    #print("Compatibilidade: {}".format(compatibility))                  
                    datas['Name'] = " ".join(fullName)
                    #print(datas['Name'])
                    datas['Divisao'] = person.find('{http://people.cti.gov.br/~paulo/cti.owl#}divisão').text
                    #print(datas['Divisão'])
                    datas['Ramal'] = person.find('{http://people.cti.gov.br/~paulo/cti.owl#}ramal').text
                    #print(datas['Ramal'])
                    datas['E-mail'] = person.find('{http://people.cti.gov.br/~paulo/cti.owl#}e-mail').text
                    #print(datas['E-mail'])
                    self.listData.append(datas.copy())
                    n_names=True

        #if n_names == False:
            #self.listData.append({'Name': None, 'Divisao': None, 'Ramal': None, 'E-mail': None})
        
        self.listData.insert(0,tags)
        #print(self.listData)

    def getdata(self):
        return self.listData