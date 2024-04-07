# INSTALACE
Python download
```sh
https://www.python.org/downloads/windows/
```
Pokud se vám neukáže verze pythonu po napsání příkazu python do terminálu, tak jste udělali při instalaci chybu
```sh
python
```
> Output např. Python 3.9.13 

clone repozitáře
```sh
$ git clone https://github.com/gyarab/2023-4e-hruska-func_game.git
```
Frontend
```sh
$ cd gaydb/
```
```sh
$ npm install
```
```sh
$ npm run dev
```

Backend
```sh
$ cd beckend/
```
Vytvoření virtual enviromentu
```sh
$ python -m venv myvenv
```
Aktivace
```sh
cd myvenv/Scripts/
```
```sh
$ . activate
```
```sh
cd ..
```
```sh
cd ..
```
Stažení requirements.txt
```sh
$ pip install -r requirements.txt
```
Zapnutí backendu
```sh
uvicorn main:app --reload --port 8000
```