"""
Re-generate the world and all models, potentially with new parameters, in folder 'world'. Concretely, 
models subdirs are created based on combinations on all obj's and all textures. In addition, an sdf is created with all the models placed inside it.

Inputs: 
- png Files in folder 'textures'
- Files in folder 'obj'
Outputs: 
- model folders in folder 'world'
- world/different_forms.sdf(used by Gazebo)
- world/obj_data.txt (used by the DifferetnForms environment)

Objects are arranged in a straight line with 2m between them. Masses for objects are assigned as 0 or 20 depending on whether the index of the 
object is odd or even.
"""

import os
import shutil
import subprocess

# Basisverzeichnis setzen
base_dir = os.path.dirname(os.path.abspath(__file__))

# Globale Variable für den Abstand zwischen den Modellen
DISTANCE = 2.0  # Abstand zwischen den Modellen in der X- und Y-Achse

# Ordnerpfade für Texturen, .obj-Dateien, .mtl-Datei und model.sdf-Datei
textures_dir = os.path.join(base_dir, "textures") 
obj_dir = os.path.join(base_dir, "obj")
world_dir = os.path.join(base_dir, "world")
mtl_file = os.path.join(obj_dir, "default.mtl")
default_model_dir = os.path.join(base_dir, "default_model")
sdf_file = os.path.join(default_model_dir, "model.sdf")
config_file = os.path.join(default_model_dir, "model.config")

mass_config_file = os.path.join(base_dir, "config", "mass.config")
obj_data_file_path = os.path.join(world_dir, "obj_data.txt")

# Arrays für Dateien
texture_files = []
obj_files = []
folders = []  # Array zum Speichern der Ordnernamen
mass_config=[]


#Pos der Obj
Pos_map = {
    "Cube": "0 0 0.00 -3.14 0 -3.14",
    "Cylinder": "0 0 -0.01 -1.57 0 0",
    "Diamand": "0 0 0.04 1.57 0 0",
    "Pyramide":"0 0 0.00 1.57 0 0",
    "Sphere":"0 0 -0.01 1.57 0 0",
    "D8":"0 0 0.01 1.57 0 0"
}


# Alle Dateien im "textures"-Ordner einlesen und Dateinamen speichern
if os.path.exists(textures_dir):
    texture_files = [f for f in os.listdir(textures_dir) if os.path.isfile(os.path.join(textures_dir, f))]
else:
    print(f"Ordner 'textures' nicht gefunden unter {textures_dir}")

# Alle .obj-Dateien im "Obj"-Ordner einlesen und Dateinamen speichern
if os.path.exists(obj_dir):
    obj_files = [f for f in os.listdir(obj_dir) if f.endswith('.obj') and os.path.isfile(os.path.join(obj_dir, f))]
else:
    print(f"Ordner 'Obj' nicht gefunden unter {obj_dir}")

# Prüfen, ob die "default.mtl"-Datei existiert
if not os.path.isfile(mtl_file):
    print(f"MTL-Datei 'default.mtl' nicht gefunden im Ordner {obj_dir}")
else:
    print("MTL-Datei gefunden und wird verarbeitet.")

# Prüfen, ob die "model.sdf"-Datei existiert
if not os.path.isfile(sdf_file):
    print(f"SDF-Datei 'model.sdf' nicht gefunden im Ordner {default_model_dir}")
else:
    print("SDF-Datei gefunden und wird verarbeitet.")

# Prüfen, ob die "model.config"-Datei existiert
if not os.path.isfile(config_file):
    print(f"Config-Datei 'model.config' nicht gefunden im Ordner {default_model_dir}")
else:
    print("Config-Datei gefunden und wird verarbeitet.")

# Prüfen, ob die "mass.config"-Datei existiert
if os.path.isfile(mass_config_file):
    print("Mass.Config-Datei gefunden und wird verarbeitet.")
    with open(mass_config_file, 'r') as mass_config_file_data:
        for line in mass_config_file_data:
            parts = line.strip().split()
            item = (parts[0], int(parts[1]))
            mass_config.append(item)
    print(mass_config)
else:
    print(f"Config-Datei 'mass.config' nicht gefunden im Ordner {base_dir}")
   

# "world"-Ordner erstellen
os.makedirs(world_dir, exist_ok=True)


# Für jede .obj-Datei und jede Textur-Datei einen Unterordner erstellen
for obj_file in obj_files:
    for texture_file in texture_files:
        # Ordnername für Kombination aus obj-Datei und Textur erstellen
        folder_name = f"{os.path.splitext(obj_file)[0]}_{os.path.splitext(texture_file)[0]}"
        obj_folder_path = os.path.join(world_dir, folder_name)
        os.makedirs(obj_folder_path, exist_ok=True)
        
        # Füge den Ordnernamen zur "folders"-Liste hinzu
        folders.append(folder_name)
        
        # .obj-Datei kopieren
        source_obj_path = os.path.join(obj_dir, obj_file)
        destination_obj_path = os.path.join(obj_folder_path, obj_file)
        shutil.copy2(source_obj_path, destination_obj_path)
        
        # Textur-Datei kopieren
        source_texture_path = os.path.join(textures_dir, texture_file)
        destination_texture_path = os.path.join(obj_folder_path, texture_file)
        shutil.copy2(source_texture_path, destination_texture_path)
        
        # MTL-Datei kopieren und umbenennen, dann Texturzeile hinzufügen
        new_mtl_filename = os.path.splitext(obj_file)[0] + ".mtl"
        destination_mtl_path = os.path.join(obj_folder_path, new_mtl_filename)
        shutil.copy2(mtl_file, destination_mtl_path)
        
        # Zeile "map_Kd <Texture-Name>" zur .mtl-Datei hinzufügen
        with open(destination_mtl_path, 'a') as mtl_file_copy:
            mtl_file_copy.write(f"\nmap_Kd {texture_file}")
        
        # Verweis auf .mtl-Datei in die erste Zeile der .obj-Datei einfügen
        with open(destination_obj_path, 'r+') as obj_file_copy:
            original_content = obj_file_copy.read()  # Originalinhalt lesen
            obj_file_copy.seek(0, 0)  # An den Anfang der Datei gehen
            obj_file_copy.write(f"mtllib {new_mtl_filename}\n" + original_content)

        # model.sdf kopieren und <model name="PLS_Replace"> und <uri> ersetzen
        destination_sdf_path = os.path.join(obj_folder_path, "model.sdf")
        shutil.copy2(sdf_file, destination_sdf_path)
        
        # <model name="PLS_Replace"> und <uri>model://UNKOWN</uri> anpassen
        with open(destination_sdf_path, 'r+') as sdf_file_copy:
            sdf_content = sdf_file_copy.read()
            sdf_content = sdf_content.replace('##Koordinaten##', f'{Pos_map.get(os.path.splitext(obj_file)[0], "0 0 0 0 0 0")}')
            sdf_content = sdf_content.replace('<model name="PLS_Replace">', f'<model name="{folder_name}">')
            sdf_content = sdf_content.replace('<uri>model://UNKOWN</uri>', f'<uri>model://{folder_name}/{os.path.splitext(obj_file)[0]}.obj</uri>')
            sdf_file_copy.seek(0)
            sdf_file_copy.write(sdf_content)
            sdf_file_copy.truncate()

        # model.config kopieren und <name>PLS_Replace</name> ersetzen
        destination_config_path = os.path.join(obj_folder_path, "model.config")
        shutil.copy2(config_file, destination_config_path)

        with open(destination_config_path, 'r+') as config_file_copy:
            config_content = config_file_copy.read()
            config_content = config_content.replace('<name>PLS_Replace</name>', f'<name>{folder_name}</name>')
            config_file_copy.seek(0)
            config_file_copy.write(config_content)
            config_file_copy.truncate()
        
# world.sdf in den world-Ordner kopieren
world_sdf_file = os.path.join(default_model_dir, "different_forms.sdf")
destination_world_sdf_path = os.path.join(world_dir, "different_forms.sdf")
shutil.copy2(world_sdf_file, destination_world_sdf_path)

obj_data = []

# Koordinaten für die Platzierung der Modelle berechnen
includes = []
for index, folder in enumerate(folders):
    x = 0.0
    y = (index - (len(folders) - 1) / 2) * DISTANCE
    # Erzeuge den Include-Block
    include_block = f"""        
        <include>
            <uri>
                model://{folder}
            </uri>
            <pose>{x} {y} 0 0 0 0</pose>
        </include>"""
    includes.append(include_block.strip())

    
    # Check if the element exists in the list of tuples and get the second part
    found_tuple = next((item for item in mass_config if item[0] == folder), None)
    
    if found_tuple:
        mass = found_tuple[1]
    else:
        mass = 0
 
    obj_data.append((folder, x, y, mass))


# Objekt-Data schreiben
with open(obj_data_file_path, 'w') as obj_data_file:
    
    for count, (name, x, y, mass)  in enumerate(obj_data):
        mass = 20. if (count % 2 == 0) else 0.
        line = f"{name} {x} {y} {mass}\n"
        obj_data_file.write(line)

# "world.sdf" lesen und den Platzhalter ##Insert_Here## ersetzen
with open(destination_world_sdf_path, 'r') as world_file:
    world_content = world_file.read()

# Platzhalter ersetzen
world_content = world_content.replace('##Insert_Here##', '\n        '.join(includes))

# Die aktualisierte "world.sdf"-Datei speichern
with open(destination_world_sdf_path, 'w') as world_file:
    world_file.write(world_content)

print("Skript erfolgreich ausgeführt.")
print(f"Texturdateien: {texture_files}")
print(f"Obj-Dateien: {obj_files}")
print(f"Erstellte Ordner: {folders}")


## Überprüfen, ob der Ordner existiert
#if os.path.isdir(world_dir):
#    # Öffne ein neues Terminal und wechsle in den Ordner
#    subprocess.run(['gnome-terminal', '--', 'bash', '-c', f'cd {world_dir} && exec bash'])
#else:
#    print(f"Der Ordner {world_dir} existiert nicht.")

