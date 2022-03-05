from pokemon_effectiveness import pokemon

pkmn=pokemon()
typeNames = pkmn.typeNames

def getPartner(myType1, myType2=None):
    allPkmnTypes = pkmn.getAllPkmnTypes()
    
    effDict = {}
    effDictTwoPkmnCombined={}
    for pkmnType in allPkmnTypes:
        if myType2 == None:
            typings = [myType1, pkmnType]
        else:
            typings = [myType1, myType2, pkmnType]
        for typing in typings:
            effDict=pkmn.getEffDictByTypeAny(typing, effDict=effDict)
    
        typeNameList = pkmn.getTypeNameList(typings)
        typeNameString = str(typeNameList)
        effDictTwoPkmnCombined[typeNameString]={}
        effDictTwoPkmnCombined[typeNameString]['myType1']= pkmn.getEffDictByTypeAny(myType1)
        if not myType2 == None:
            effDictTwoPkmnCombined[typeNameString]['myType2']= pkmn.getEffDictByTypeAny(myType2)
            effDictTwoPkmnCombined[typeNameString]['myTypes'] = pkmn.combineEffByType([myType1, myType2], effDictByType=effDict)
        effDictTwoPkmnCombined[typeNameString]['otherType']= pkmn.getEffDictByTypeAny(pkmnType)
        effDictTwoPkmnCombined[typeNameString]['effectiveness'] = pkmn.combineEffByType(typings, effDictByType=effDict)
        effDictTwoPkmnCombined[typeNameString]['effScore'] = pkmn.getEffScore(effDictTwoPkmnCombined[typeNameString]['effectiveness'])
    
    effDictTwoPkmnCombined=sorted(effDictTwoPkmnCombined.items(),key=lambda k_v: k_v[1]['effScore'])
    return effDictTwoPkmnCombined

myType1 = ('ground','water')
myType2 = ('steel', 'flying')
matchups = getPartner(myType1, myType2)


# to do: find two complementary pokemon (defensive or offensive)
# to do: improve offensive calc to include other effectivities
# to do: sample pokemon, not all types
# to do: include stab in offensive calc -> get dict that has best effectiveness for all defending types
# to do: include required types in offensive calc
