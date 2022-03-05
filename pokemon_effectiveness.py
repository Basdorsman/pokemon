# https://pokeapi.co/docs/v2#pokemon-section
import pokebase as pb
from itertools import combinations

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
    
    def combineEff(self, myTypeNames, effDict=None):
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
    
    def getDefenseEffByType(self, myTypeName):
        effDictByType={}
        for typeName in self.typeNames:
            if typeName in self.immuneDict[myTypeName]:
                effDictByType[typeName] = '0'
            elif typeName in self.resistanceDict[myTypeName]:
                effDictByType[typeName] = '0.5'
            elif typeName in self.weaknessDict[myTypeName]:
                effDictByType[typeName] = '2'
            else:
                effDictByType[typeName] = '1'
        return effDictByType
        
    def getEffDictByType(self):
        effDictByType = {}
        for typeName in self.typeNames:
            effDictByType[typeName]=self.getDefenseEffByType(typeName)
        return(effDictByType)
    
    def combineEffByType(self, types, effDictByType=None):
        '''Combine effectiveness of two types. 
        
        By cycling through all types and multiplying the effectiveness of 
        either, it finds the combined effectiveness for a dual type. Producing
        the dictionary containing all the effectiveness takes time, so passing
        a prepared effectiveness dictionary can speed up the process.
        
        Parameters
        ----------
        typeNameDual (iterable) : Contains two strings of two types.
        effDictByType : Prepared dictionary of all type effectivenesses.
        
        Returns
        -------
        effDictByTypeDual : effectiveness of dual typing.
        
        '''
        
        if effDictByType==None:
            effDictByType={}
            for typing in types:
                effDictByType=self.getEffDictByTypeAny(typing, effDictByType)
        
        typeNameList = self.getTypeNameList(types)

        effDictByTypeDual={}
        for typeName in self.typeNames:
            effDictByTypeDual[typeName]=float(effDictByType[typeNameList[0]][typeName])*float(effDictByType[typeNameList[1]][typeName])
        return effDictByTypeDual
    
    def getEffDictByTypeAny(self, types, effDict=None):
        if effDict == None:
            effDict = {}
        if isinstance(types, str):
            try:
                effDict[types]
            except KeyError:
                effDict[types]=self.getDefenseEffByType(types) 
        elif isinstance(types, tuple):
            typeString = ' '.join(list(types))
            try: 
                effDict[typeString]
            except KeyError:
                effDict[typeString]=self.combineEffByType(types)
        return effDict

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
    
    def getEffScore(self,effDict):
        effScore = 0
        for typeName in self.typeNames:
            effScore += float(effDict[typeName])
        return effScore

    def getAllPkmnTypes(self):
        dualTypes = list(combinations(self.typeNames, 2))
        allPkmnTypes = dualTypes
        for typeName in self.typeNames:
            allPkmnTypes.append(typeName)
        return allPkmnTypes
    
    def getTypeNameList(self, types):
        typeNameList = []
        for typing in types:
            if isinstance(typing, str):
                typeNameList.append(typing)
            elif isinstance(typing, tuple):
                typeNameList.append(' '.join(list(typing)))
        return typeNameList

if __name__ == '__main__':
    pkmn = pokemon()
    combined = pkmn.combineEffByType(('ice','dark'))
    