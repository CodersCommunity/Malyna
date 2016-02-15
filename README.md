# Malyna
Bot do naszego IRC: freenode.net #mzforum

## Wymagania
```
$ apt-get install python-pip
$ apt-get install xclip
```
## Instalacja
1. Pobrać kod Malyny

  ```
  $ git clone https://github.com/CodersCommunity/Malyna.git
  $ cd Malyna
  ```
2. Instalacja zależności

  ```
  $ pip install -r requirements.txt
  ```

### Uruchomienie
```
$ python malyna.py
````
### Wdrożenie własnego pluginu - Przykładowy plugin
1. W katalogu plugins dodać plik nazwapluginu.py

  ```
  # -*- coding: utf-8 -*-

  from yapsy.IPlugin import IPlugin


  class NazwaPluginu(IPlugin):
      def execute(self, channel, username, command):
          if not command:
              yield channel, ("Podstawowy plugin")

  ```
2. W katalogu plugins dodać plik nazwapluginu.yapsy-plugin
  ```
  [Core]
  Name = nazwapluginu
  Module = nazwapluginu

  [Documentation]
  Author = autor
  Website = strona
  Description = krótka dokumentacja pluginu, dostępna pod >help nazwapluginu.
  ```
3. Krótka dokumentacja - dodawania pluginów
  ```
  from yapsy.IPlugin import IPlugin - wymagane
  class NazwaPluginu(IPlugin): - wymagne, nazwa pluginu z dużej litery
  def execute(self, channel, username, command): -- wymagane, wywołuje plugin

  channel -- określa odbiorce wiadomości jako aktualny kanał
  username -- określa odbiorce wiadomości jako usera wywołujący funkcje
  command -- arguent przesłany dla pluginu. >nazwapluginu argument
  if not command - gdy wywolujemy sam plugin bez argumentów, np: >nazwapluginu
  yield username, ("Przykład") - wysyła wiadomoc "Przykład" dla usera
  ```











