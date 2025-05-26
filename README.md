# Jeux tetris en ligne de commande pour apprentissage base Python
mise en place environement de dev

python -m venv env_tetris
.\env_tetris\Scripts\activate

# installation dépendance

pip install keyboard

# initialisation dépot local

git init

# copie/lien vers dépot distant

git remote add origin https://github.com/"yourName"/tetris_pedago_python.git

git config user.name "jerome"

git config user.email "mail@gmail.com"

# ajout .gitignore

add .gitignore

git commit -m "Initial commit avec .gitignore"

# création branche principale

git branch -M main

# push vers dépôt distant

git push -u origin main

# création fichier configuration des dépendances python

touch "requirements.txt"

pip freeze > requirements.txt

# ajout readme à un commit et à un push

git add README.md




