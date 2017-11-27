# imageCropper
ImageCropper ist ein Python Skript, welches automatisch eingescannte Bilder freistellt und entsprechende Namen gibt.

Python 2.7 und [PythonImageLibrary](http://www.pythonware.com/products/pil/) werden benötigt. Funktioniert auf Windows, Mac und Linux.

## Programmstart
Die Konsole muss in dem Ordner geöffnet werden und das Programm dort mit `python picture.py` ausgeführt werden.

## Vorbereitungen
### Config
Die Config Datei in `/config/config.json` muss bearbeitet werden. `offset` stell die Verschiebung des Ursprungs im Quellbild dar, `source_size` und `destination_size` definieren die Größe. Sind die Werte unterschiedlich, so wird das Bild skaliert. Die Datei `/config/lastnum.json` kann ignoriert werden.

### Ordner
In `/image_source` müssen die Unterordner angelegt werden. Folgende Struktur ist zwingend:
```
-+ image_source
 +--+ 2015
 |  +--+ 03
 |  +--+ 07
 |  +--+ 12
 +--+ 2016
 |  +--+ 07
 +--+ 2017
    +--+ 01
    +--+ 02
```
In den innersten Ordnern befinden sich beliebig benannte Bilder.

## Ablauf
Das Programm durchläuft anschließend die Ordner und verarbeitet alle Bilder. Diese werden auf die gewünschte Größe zugeschnitten und nach dem Schema `PRE_YYYY_MM_XXX.jpg` benannt, wobei `XXX` fortlaufende Nummern beginnend bei `000` sind.

**zum Beispiel:** `PIC_2017_02_000.jpg`
