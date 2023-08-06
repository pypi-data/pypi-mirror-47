enumeratime
===============================
Einfaches Programm, um sich in Schleifen eine Prozent und Zeitprognose auszugeben.
Gibt pro Schleifendurchlauf die Zeilennummer zurück, kann also auch enumerate ersetzen.

Der Leser kennt vermutlich das Gefühl, wenn man etwas bei Python verarbeitet und es *dauert, und dauert," und dauert,"\*100*
Mit diesem Programm kann man eine einfache Zeitprognose bekommen, sofern man über Objekte mit bekannter Länge iteriert, bei denen die Verarbeitung der einzelnen Elemente etwa gleich lange dauert.
Bald vielleicht auch noch in "Forschrittsbalken-Version"

```python
from enumeratime import  EnumeraTIME
for n, line in EnumeraTime(myobject)):
    doSomething(myobject)
```
Hinweis:
Die Software ist unter GPL3.0 lizensiert, allerdings in nur 15 Minuten entstanden, um abschätzen zu können, ob die Verarbeitung innerhalb der nächsten Stunde fertig wird.