from sproget import skribbl

URL = 'https://www.stengaardkirke.dk'

skribbl = skribbl()

skribbl.fetch(URL)

ord = skribbl.get_results()

skribbl.to_txt()

print(ord)

