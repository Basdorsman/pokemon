# https://pokeapi.co/docs/v2#pokemon-section
import pokebase as pb
import matplotlib.pyplot as plt
from itertools import combinations
import math

class pokemon():
    def __init__(self):
        self.types = [pb.type_(index) for index in range(1,19)]
        self.typeNames = [item.name for item in self.types]
        self.resistanceDict = {typeName : [item.name for item in pkmnType.damage_relations.half_damage_from] for typeName, pkmnType in zip(self.typeNames, self.types)}
        self.weaknessDict = {typeName : [item.name for item in pkmnType.damage_relations.double_damage_from] for typeName, pkmnType in zip(self.typeNames, self.types)}
        self.immuneDict = {typeName : [item.name for item in pkmnType.damage_relations.no_damage_from] for typeName, pkmnType in zip(self.typeNames, self.types)}
        self.superEffectiveDict = {typeName : [item.name for item in pkmnType.damage_relations.double_damage_to] for typeName, pkmnType in zip(self.typeNames, self.types)}
        
    def getDefenseEff(self, myTypeName, effDict=None):
        if effDict == None:
            effDict = {'0':[],'0.5':[],'1':[],'2':[]}
        for type2test in self.typeNames:
            if (type2test in self.resistanceDict[myTypeName]):
                 effDict['0.5'].append(type2test)
            elif (type2test in self.weaknessDict[myTypeName]):
                 effDict['2'].append(type2test)
            elif (type2test in self.immuneDict[myTypeName]):
                 effDict['0'].append(type2test)
            else:
                effDict['1'].append(type2test)
        return effDict

    def getDefenseEffDual(self, myTypeNames, effDict=None):
        if effDict == None:
            effDict = {'0':[],'0.5':[],'1':[],'2':[]}
        for myTypeName in myTypeNames:
            effDict=self.getDefenseEff(myTypeName, effDict)
        effDictDual = {'0':[],'0.25':[],'0.5':[],'1':[],'2':[],'4':[]}
        for typeName in self.typeNames:
            if typeName in effDict.get('0'):
                effDictDual['0'].append(typeName)
            elif effDict.get('0.5').count(typeName)==2:
                effDictDual['0.25'].append(typeName)
            elif (typeName in effDict.get('0.5') and typeName in effDict.get('2')):
                continue
            elif effDict.get('2').count(typeName)==2:
                effDictDual['4'].append(typeName)
            elif effDict.get('0.5').count(typeName)==1:
                effDictDual['0.5'].append(typeName)
            elif effDict.get('2').count(typeName)==1:
                effDictDual['2'].append(typeName)
            else:
                effDictDual['1'].append(typeName)
        return effDictDual

    def getMultiOffenseEff(self, typeNames, combineN):
        multiTypeLengths=[]
        multiTypeDicts={}
        for multiTypes in list(combinations(typeNames, combineN)):
            allTypeCombination=[]
            for typeName in multiTypes:
                for item in self.superEffectiveDict[typeName]:
                    allTypeCombination.append(item)
            multiTypeCombination = list(dict.fromkeys(allTypeCombination))
            multiTypeCombination.sort()
            multiTypeLength = len(multiTypeCombination)
            multiTypeLengths.append(multiTypeLength)
            multiTypeDicts[" ".join(multiTypes)]={'types' : multiTypeCombination, 'length' : multiTypeLength}
        return multiTypeDicts, multiTypeLengths


pkmn=pokemon()
# Offensive stuff
# multiTypeDicts, multiTypeLenghts = pkmn.getMultiOffenseEff(pkmn.typeNames, 3)    
# plt.hist(multiTypeLenghts)
# multiTypeDicts=sorted(multiTypeDicts.items(),key=lambda k_v: k_v[1]['length'],reverse=True)

typeNames = pkmn.typeNames
typeNamesFull = []
for typeName in typeNames:
    typeNamesFull.append(typeName)

# effDictDual={}
# for dualType in list(combinations(typeNames, 2)):
#     effDictDual = pkmn.getDefenseEffDual(dualType)

def getWeights(effect):
    if effect == '0':
        weight = 1.5
    if effect == '0.25':
        weight = 1
    elif effect == '0.5':
        weight = 0.5
    elif effect == '1':
        weight = 0
    elif effect == '2':
        weight = -0.5
    elif effect == '4':
        weight = -1
    return weight

defenseEffScore={}
for dualType in list(combinations(typeNames, 2)):
    defenseEffDual = pkmn.getDefenseEffDual(dualType)
    dualTypeString=' '.join(list(dualType))
    defenseEffScore[dualTypeString]=0
    for multiplier in defenseEffDual:
        defenseEffScore[dualTypeString]+=float(multiplier)*len(defenseEffDual[multiplier])

for singleType in typeNames:
    defenseEff = pkmn.getDefenseEff(singleType)
    defenseEffScore[singleType]=0
    for multiplier in defenseEff:
        defenseEffScore[singleType]+=float(multiplier)*len(defenseEff[multiplier])

#defenseEffScore=sorted(defenseEffScore.items(),key=lambda k_v: k_v[1])

defenseEffScoreList = []
for key in defenseEffScore:
    defenseEffScoreList.append(defenseEffScore[key])

fig, ax = plt.subplots()
ax.set_xlabel('score = sum defensive effectiveness for all types')
ax.set_ylabel('N (dual) typings per score')
ax.hist(defenseEffScoreList,bins=20)

