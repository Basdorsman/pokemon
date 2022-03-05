from pokemon_effectiveness import pokemon
import matplotlib.pyplot as plt
pkmn=pokemon()

myTypes=('dragon',)
candidateTypes=('fire','rock','ground','steel','fighting','dark','ghost','psychic','flying')
multiTypeDicts, multiTypeLenghts = pkmn.getMultiOffenseEff(myTypes,candidateTypes,room=3)    
plt.hist(multiTypeLenghts)
multiTypeDicts=sorted(multiTypeDicts.items(),key=lambda k_v: k_v[1]['length'],reverse=True)

