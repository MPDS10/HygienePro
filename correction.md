## A1
J'ai cree les tables (_violations_) dans le fichier qui s'appelle _db.sql_ inclu dans le repertoire **db** et j'ai lu les donnees du fichier csv grâce à la methode `inserer_donnees_csv` qui se trouve dans le script `database.py`
puis la classe `Database` se charge de _connecter/deconnecter_ la base de donnee.
**Pour executer: il faut cliquer sur la base de donnees `db.sql`**

## A2
La methode `obtenir_violations` de la classe `Database` permet d'obtenir les violations depuis la base de donnée puis je fais les recherches dans le template html `page_acceuil.html` et le template html `page_resultat.html` affiche le resultat.
la fonction `recherche()` dans app.py permettra de faire correspondre les recherches en fonction de l'etablissement,du proprietaire et de l'adresse. 
**Pour executer: taper `montreal` dans la barre de recherche**

## A3
Afin d'extraire et faire les mise a jour des données hebdomadairement à minuit, j'ai utilisé ma fonction `inserer_donnees_csv` qui se trouve dans le script `database.py` puis dans mon application flask, j'ai crée un planificateur de tâches en arrière-plan **(BackgroundScheduler)** avec L'argument **daemon=True** qui indique que le planificateur s'exécutera en arrière-plan et ne bloquera pas le programme principal.
Ensuite, j'ai specifier la fonction à exécuter à intervalle regulier et defini un declancheur qui indiquera l'exécution de la tâche à minuit chaque jour.


## A4
Pour afficher les contraventions en fonction de l'intervalle de date, j'ai utilisé la methode `obtenir_violations` de la classe `Database` permet d'obtenir les violations depuis la base de donnée puis j'ai crée les variables `du` et `au` qui permettront de reconnaitre les intervalles.
A propos de la documentation j'ai cree un bouton **DOCUMENTATION** à l'acceuil qui permettra d'acceder aux details du service. 
**Appuyer sur le bouton `DOCUMENTATION` pour voir la documentation **

## A5
Pour afficher le tableau j'ai utilise la methode `rechercherContraventions` qui se trouve dans le fichier `validation.js` puis grace a **A4** j'ai pu afficher la liste dans le template `page_acceuil.html`
Pour executer: faire sa recherche en utilisant le calendrier et mettre les date du et au puis appuyer sur le bouton `rechercher`/

## A6
Pour afficher la liste deroulante j'ai utilise la methode `remplirListeDeroulante` qui se trouve dans le fichier `validation.js` pour recuperer les nom des differents etablissements et la methode `rechercherContraventionsParNom` va afficher la liste dans le template `page_acceuil.html`
Pour executer: faire sa recherche en utilisant la liste deroulante

## C1
Pour afficher la liste des etablissements de façon decroissante, j'ai utilisé `defaultdict` afin d'optimiser le tri j'ai cree un bouton **LISTE DES ETABLISSEMENTS AVEC INFRACTIONS** à l'acceuil qui permettra d'acceder à la liste.
**Pour executer: appuyer sur le bouton `LISTE DES ETABLISSEMENTS AVEC INFRACTIONS`**

## C2
Pour afficher la liste des etablissements de façon decroissante en format **xml**, j'ai utilisé `defaultdict` afin d'optimiser le tri j'ai cree un bouton puis j'ai utilisé escape qui permettais d'echapper les caracteres speciaux car il y'avait certaines erreurs puis le bouton  **LISTE DES ETABLISSEMENTS AVEC INFRACTIONS(XML)** à l'acceuil  permettra d'acceder à la liste.
**Pour executer: appuyer sur le bouton `LISTE DES ETABLISSEMENTS AVEC INFRACTIONS(XML)`**

## C3
Pour afficher la liste des etablissements de façon decroissante en format **csv**, j'ai utilisé `defaultdict` afin d'optimiser le tri puis le bouton **LISTE DES ETABLISSEMENTS AVEC INFRACTIONS(csv)** à l'acceuil permettra d'acceder au fichier telechargeable.
**Pour executer: appuyer sur le bouton `LISTE DES ETABLISSEMENTS AVEC INFRACTIONS(XML)`**

## D1
Afin de permettre à l'utilisateur de deposer une plainte qui sera enregistrée, j'ai cree la table `plainte` dans la base de donnee `db.sql` puis j'ai fait la validation dans mon fichier `validation.js` et lu la base de donnée à l'aide de la fonction `enregistrer_plaintes` dans `Database`.
**Pour executer: appuyer sur le bouton `DEPOSER UNE PLAINTE`** puis entrer les donnees correspondantes aux champs.

## E1
Pour permettre à l'utilisateur de se connecter j'ai cree la table `utilisateur` dans la base de donnee `db.sql`  puis j'ai fait la validation dans mon fichier `validation.js` et lu la base de donnée à l'aide de la fonction `enregistrer_utilisateur` sans oublier de verifier s'il n'yavait pas d'emails deja utilise grace a la fonction `chercher_dans_bd` dans `Database`
**Pour executer: appuyer sur le bouton `CREER UN COMPTE`** puis entrer les donnees correspondantes aux champs.