# Strip a comma separated list, return values separated by newlines in a .txt file.

places =['Abarra', 'Guparta', 'Koyo Isu', 'Bozeg', 'Phodai', 'Teraat', 'Qabis',
'Chakiragar', 'Tismin Insu', 'Kalmoro', 'Ethar', 'Kotelga', 'Altaxa', 'Nebay',
'Nebayanat', 'Aamidal', 'Standing', 'Bhidra', 'Oret Soi', 'Sudarai', 'Bhojo Patal',
'Matra Dhor',  'Niyat Dhor', 'Grahisa', 'Kono Manoi', 'Turagai', 'Jamosom', 'Ekanga',
'Desh', 'Yaburah', 'Tsugge', 'Harai', 'Rumid', 'Siur', 'Ksu', 'Vo', 'Su', 'Kusaslu',
'Bhanusri', 'Nasiraat', 'Santhe', 'Sestab','Kano Insu', 'Kusequ', 'Kanoyariya', 
'Turaatrah', 'Guparahid', 'Joyen Bor']

with open("stripped_names.txt", 'w') as f:
    for name in places:
        f.write(name + '\n')

