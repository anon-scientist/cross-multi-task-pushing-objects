# skript_world

In diesem Ordner finden sich alle notwendigen Dateien und Skripte, um eine Gazebo-Simulationsumgebung mit verschiedenen Objekten und Texturen zu generieren. Nachfolgend eine Übersicht der Ordnerstruktur und deren Inhalte:  
## Ordnerstruktur  

- **`config/`**  
  Enthält Konfigurationsdateien für die Simulation.
  Die Datei `mass.config` dient zur Definition der Massenwerte für die Objekte in der Simulation.
  Diese Werte können entweder manuell eingetragen oder mithilfe des Skripts `config.py` erstellt werden. 


- **`default_model/`**  
  In diesem Ordner befinden sich die Basis-SDF- und Konfigurationsdateien für die Welt und die Objekte.  
  Diese Dateien werden später durch das Skript erweitert und angepasst.  

- **`obj/`**  
  Hier liegen alle `.obj`-Dateien, die die Formen der zu generierenden Objekte definieren.  
  **Wichtig:**  
  - In den `.obj`-Dateien gibt es noch keinen Verweis auf die zugehörige `.mtl`-Datei.  
  - Das Skript fügt diese Verweise während der Verarbeitung hinzu.  
  - Die vorhandene `.mtl`-Datei im `obj/`-Ordner dient als Default-Materialvorlage und wird durch das Skript für jedes Objekt angepasst.  

- **`robot/`**  
  Dieser Ordner enthält die SDF-Dateien für den Roboter, der mit einem zusätzlichen Lidar-Sensor ausgestattet wurde.  

- **`textures/`**  
  Hier befinden sich alle Texturen, die zur Generierung der Objekte verwendet werden sollen.  

- **`textures_TMP/`**  
  Dieser Ordner enthält zusätzliche Texturen, die ebenfalls verwendet werden können.  
  **Hinweis:** Damit diese Texturen in der Generierung verwendet werden können, müssen sie in den `textures/`-Ordner kopiert werden.  

- **`world/`**  
  In diesem Ordner wird die generierte Gazebo-Simulation gespeichert.  

- **`skript.py`**  
  Das Python-Skript dient zur automatischen Generierung einer Gazebo-Simulation basierend auf den angegebenen Objekten und Texturen.

  Das Skript liest alle `.obj`-Dateien aus dem `obj/`-Ordner sowie alle Texturen aus dem `textures/`-Ordner ein. Anschließend wird für jede Kombination aus Objekt und Textur ein entsprechendes Objekt in der Gazebo-Simulation generiert.

  Für jedes generierte Objekt wird der entsprechende Positions- und Massenwerte in die Datei `obj_data.txt` im `world/`-Ordner gespeichert. Die Massenwerte werden zuvor in der `mass.config`-Datei definiert.

  Nach der vollständigen Erstellung der Gazebo-Simulation öffnet das Skript automatisch ein Terminal im erzeugten `world/`-Ordner, um die Simulation zu testen.
  

## Verwendung 

  Das Skript wird mit folgendem Befehl ausgeführt.

```bash
python3 skript.py
```

Anschließend kann die Simulation im sich öffnenden Terminal mit folgendem Befehl getestet werden.
```bash
QT_QPA_PLATFORM=xcb gz sim -v 4 different_forms.sdf 
```
