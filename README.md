# Jeux tetris en ligne de commande pour apprentissage base Python
mise en place environement de dev pour tout le monde

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

# ajout de branche pour travail partagé (avec 2 participants)

Étape 1 : Cloner le Dépôt (si ce n'est pas déjà fait par votre fils)

Si votre fils n'a pas encore une copie locale du dépôt sur son ordinateur, il doit le "cloner" depuis GitHub. Il trouvera l'URL du dépôt sur la page GitHub de tetris_pedago_python (bouton "Code").

Dans son terminal Git :

Bash

git clone [URL_du_dépôt]
cd tetris_pedago_python

Étape 2 : S'assurer que la branche main locale est à jour

Avant de commencer un nouveau travail, il est bon de s'assurer que votre version locale de la branche main est synchronisée avec celle sur GitHub.
Sur l'ordinateur de la personne qui va travailler (disons, votre fils) :

Bash

git checkout main      # Se placer sur la branche main
git pull origin main   # Récupérer les derniers changements de main depuis GitHub
Étape 3 : Créer une nouvelle Branche pour la fonctionnalité

Votre fils va créer une branche spécialement pour le système de score. Un nom descriptif est une bonne idée.

Bash

# Crée une nouvelle branche nommée 'feature/systeme-score' et bascule dessus
git checkout -b feature/systeme-score
Maintenant, tout le travail de votre fils sur le score se fera dans cette branche, sans impacter main.

Étape 4 : Travailler sur la fonctionnalité (Coder !)

Votre fils modifie le code, ajoute les fonctions pour le score, etc. Il fait des "commits" réguliers pour sauvegarder ses progrès localement.

Bash

# Après avoir modifié des fichiers
git add .  # Ajoute tous les fichiers modifiés pour le prochain commit
git commit -m "Ajout initial du calcul du score pour une ligne"
# (Il peut faire plusieurs commits au fur et à mesure de son avancée)
Conseil pour les messages de commit : Encouragez des messages clairs qui expliquent ce qui a été fait et pourquoi.

Étape 5 : Pousser (Push) la branche sur GitHub

Une fois que votre fils a fait quelques commits et qu'il veut partager son travail (ou simplement le sauvegarder sur GitHub), il "pousse" sa branche :

Bash

git push origin feature/systeme-score
Maintenant, la branche feature/systeme-score existe aussi sur le dépôt GitHub.

Étape 6 : Créer une "Pull Request" (PR) – C'est ici que vous comparez !

Quand votre fils pense que sa fonctionnalité est prête (ou qu'il aimerait avoir votre avis), il va sur la page du dépôt tetris_pedago_python sur GitHub.

GitHub détecte souvent les nouvelles branches poussées et propose de créer une "Pull Request".
Il clique pour créer une PR, en s'assurant que la PR veut fusionner feature/systeme-score (sa branche) vers main (la branche principale).
Il peut ajouter un titre et une description à sa PR, expliquant ce qu'il a fait.
Étape 7 : Examiner la Pull Request (Code Review)

C'est le moment clé de la collaboration et de la "comparaison" :

Vous (le père, ou tous les deux ensemble) allez sur GitHub pour voir la PR.
Onglet "Files changed" : Vous verrez exactement toutes les modifications apportées par votre fils (les lignes ajoutées en vert, supprimées en rouge). C'est la comparaison ligne par ligne !
Discussion : Vous pouvez ajouter des commentaires directement sur des lignes de code spécifiques pour poser des questions, suggérer des améliorations, ou simplement dire "Bien joué !". Votre fils peut répondre, faire des modifications sur sa branche et les re-pousser (la PR se mettra à jour automatiquement).
C'est un excellent outil d'apprentissage et de dialogue sur le code.
Étape 8 : Fusionner (Merge) la Pull Request

Si tout vous semble bon et que la fonctionnalité est prête à être intégrée à la version principale :

Depuis la page de la PR sur GitHub, vous (ou celui qui a les droits) cliquez sur le bouton "Merge pull request".
Cela intègre les modifications de feature/systeme-score dans la branche main.
GitHub propose souvent de supprimer la branche de fonctionnalité (feature/systeme-score) après la fusion, ce qui est une bonne pratique pour garder le dépôt propre.
Étape 9 : Mettre à jour les copies locales

Une fois la PR fusionnée dans main sur GitHub, vous devez tous les deux mettre à jour vos branches main locales :

Bash

git checkout main
git pull origin main
Et voilà ! Le cycle recommence pour la prochaine fonctionnalité.




