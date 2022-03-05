from itertools import combinations
from pokemon_effectiveness import pokemon
import matplotlib.pyplot as plt

pkmn=pokemon()
typeNames = pkmn.typeNames

def getPartner(myType):
    allPkmnTypes = pkmn.getAllPkmnTypes()
    
    effDict = {}
    effDictTwoPkmnCombined={}
    for pkmnType in allPkmnTypes:
        typings = [myType, pkmnType]
        for typing in typings:
            effDict=pkmn.getEffDictByTypeAny(typing, effDict=effDict)
    
        typeNameList = pkmn.getTypeNameList(typings)
        typeNameString = ' '.join(typeNameList)
        effDictTwoPkmnCombined[typeNameString]={}
        effDictTwoPkmnCombined[typeNameString]['myType']= pkmn.getEffDictByTypeAny(myType)
        effDictTwoPkmnCombined[typeNameString]['otherType']= pkmn.getEffDictByTypeAny(pkmnType)
        effDictTwoPkmnCombined[typeNameString]['effectiveness'] = pkmn.combineEffByType(typings, effDictByType=effDict)
        effDictTwoPkmnCombined[typeNameString]['effScore'] = pkmn.getEffScore(effDictTwoPkmnCombined[typeNameString]['effectiveness'])
    
    effDictTwoPkmnCombined=sorted(effDictTwoPkmnCombined.items(),key=lambda k_v: k_v[1]['effScore'])
    return effDictTwoPkmnCombined

myType = ('ghost','ice')
matchups = getPartner(myType)

# to do: find two complementary pokemon (defensive or offensive)
# to do: improve offensive calc to include other effectivities
# to do: sample pokemon, not all types
# to do: include stab in offensive calc -> get dict that has best effectiveness for all defending types
# to do: include required types in offensive calc
