import os
import itertools

# Basisverzeichnis setzen
base_dir = os.path.dirname(os.path.abspath(__file__))

# Ordnerpfade für Texturen, .obj-Dateien, .mtl-Datei und model.sdf-Datei
textures_dir = os.path.join(base_dir, "..","textures") 
obj_dir = os.path.join(base_dir, "..", "Obj")

mass_config_file = os.path.join(base_dir, "mass.config")
mass_config_param = os.path.join(base_dir, "mass_param.txt")

# Arrays für Dateien
letters=[]
colors=[]
forms=[]
mass_param=[]
mass_config=[]
config_data= []

list1 = []
list2 = []
list3 = []


# Alle Dateien im "textures"-Ordner einlesen und Dateinamen speichern
if os.path.exists(textures_dir):
     letters = {f.split('.')[0].split('_')[0] for f in os.listdir(textures_dir) if os.path.isfile(os.path.join(textures_dir, f))}
     letters = list(letters)
     
     colors = {f.split('.')[0].split('_')[1] for f in os.listdir(textures_dir) if os.path.isfile(os.path.join(textures_dir, f))}
     colors = list(colors)
else:
    print(f"Ordner 'textures' nicht gefunden unter {textures_dir}")

# Alle .obj-Dateien im "Obj"-Ordner einlesen und Dateinamen speichern
if os.path.exists(obj_dir):
    forms = [f.split('.')[0] for f in os.listdir(obj_dir) if f.endswith('.obj') and os.path.isfile(os.path.join(obj_dir, f))]
else:
    print(f"Ordner 'Obj' nicht gefunden unter {obj_dir}")


# Prüfen, ob die "mass_param"-Datei existiert
if os.path.isfile(mass_config_param):
    print("Mass_Config_Param-Datei gefunden und wird verarbeitet.")
    with open(mass_config_param, 'r') as mass_param_data:
        for line in mass_param_data:
            # Leere Zeilen oder Zeilen, die mit '#' beginnen, ignorieren
            if line.strip() and not line.strip().startswith('#'):
                mass_param.append(line.strip())
    #print(mass_param)
else:
    print(f"Mass_Config_Param-Datei 'mass_param.txt' nicht gefunden im Ordner {base_dir}")

for row in mass_param:
    list1 = []
    list2 = []
    list3 = []
    tmp = row.split('|')
    if len(tmp) != 4:
        print("Error! ", tmp)
        break;

    list1 = tmp[0].split(",")
    if '' in list1:
        list1 = forms
            
    list2 = tmp[1].split(",")
    if '' in list2:
        list2 = letters
    
    list3 = tmp[2].split(",")
    if '' in list3:
        list3 = colors
        
    config_data_part = [(f'{comb[0]}_{comb[1]}_{comb[2]}',tmp[3]) for comb in itertools.product(list1, list2, list3)]

    # Neues Tupel, nur hinzufügen, wenn der erste Teil noch nicht vorhanden ist
    for i in config_data_part:
        if i[0] not in [x[0] for x in config_data]:
            config_data.append(i)


with open(mass_config_file, "w") as file:
    for comb in config_data:
        
        line = f"{comb[0]} {comb[1]}\n"
        file.write(line)



