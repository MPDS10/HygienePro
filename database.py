import csv
import requests
import sqlite3
import os
import hashlib


# Fonction pour télécharger les données CSV dans la base de données
def inserer_donnee_csv(url_csv, chemin_db_csv, nom_table_csv):
    try:
        # Télécharger les données du fichier CSV
        r = requests.get(url_csv)
        contenu_csv = r.content.decode('utf-8').splitlines()
        lecture_csv = csv.reader(contenu_csv)

        # Se connecter à la base de données
        connexion = sqlite3.connect(chemin_db_csv)
        cursor = connexion.cursor()

        # Supprimer les données existantes dans la table
        cursor.execute(f'DELETE FROM {nom_table_csv}')

        # lire première ligne du fichier CSV pour obtenir les noms de colonnes
        colonnes_csv = next(lecture_csv)

        # Exclure la colonne id_poursuite si elle existe dans les colonnes
        if 'id' in colonnes_csv:
            colonnes_csv.remove('id')

        # Construire la liste de colonnes de la requête SQL
        colonnes_sql = ", ".join(colonnes_csv)

        # Générer la requête SQL en fonction du nombre de colonnes
        requete_sql = (f'INSERT INTO {nom_table_csv} ({colonnes_sql}) '
                       f'VALUES ({", ".join(["?" for _ in colonnes_csv])})')

        for ligne in lecture_csv:
            if 'id' in colonnes_csv:
                ligne = ligne[1:]
            cursor.execute(requete_sql, ligne)

        # Valider les modifications et fermer la connexion
        connexion.commit()
        connexion.close()

        # Afficher un message de succès
        print("Insertion des données réussie")

    except FileNotFoundError:
        # Afficher un message si le fichier CSV n'est pas trouvé
        print("Erreur: Fichier n'est pas retrouvé")

    except ValueError:
        # Afficher un message en cas d'erreur dans les valeurs du fichier CSV
        print("Erreur: Erreur dans les valeurs")

    except Exception as e:
        # Afficher un message en cas d'échec de l'insertion des données
        print("Erreur: Erreur dans l'insertion des données:", e)


# URL du fichier CSV
url = ('https://data.montreal.ca/dataset/05a9e718-6810-4e73-8bb9-5955efeb91a0'
       '/resource/7f939a08-be8a-45e1-b208'
       '-d8744dca8fc6/download/violations.csv')

# Chemin vers la base de données SQLite
chemin_db = 'db/violation.db'

# Nom de la table dans la base de données
nom_table = 'violations'

# Appel de la fonction pour insérer les données dans la base de données
inserer_donnee_csv(url, chemin_db, nom_table)


# Fonction pour hacher le mot de passe
def hacher_mot_de_passe(mdp_utilisateur):
    salt = os.urandom(32)
    mdp_hache = hashlib.pbkdf2_hmac('sha256',
                                    mdp_utilisateur.encode('utf-8'), salt,
                                    100000)
    salt_hexa = salt.hex()
    mot_de_passe_hache_hexa = mdp_hache.hex()
    return mot_de_passe_hache_hexa, salt_hexa


class Database:

    def __init__(self):
        self.connexion = None

    # Fonction pour se connecter à la base de données
    def obtenir_connexion(self):
        if self.connexion is None:
            try:
                self.connexion = sqlite3.connect('db/violation.db')
            except sqlite3.Error as e:
                print('Erreur lors de la connexion à la base de données :', e)
        return self.connexion

    # Fonction pour se déconnecter
    def deconnexion(self):
        if self.connexion is not None:
            self.connexion.close()

    # Méthode pour obtenir les violations depuis la base de données
    def obtenir_violations(self):
        cursor = self.obtenir_connexion().cursor()
        requete = "SELECT * FROM violations"
        try:
            cursor.execute(requete)
            donnees = cursor.fetchall()
            return donnees
        except sqlite3.Error as e:
            print('Erreur lors de la récupération des violations :', e)
            return []

    def obtenir_noms_restaurants(self):
        cursor = self.obtenir_connexion().cursor()
        requete = "SELECT DISTINCT etablissement FROM violations"
        try:
            cursor.execute(requete)
            noms_restaurants = [row[0] for row in cursor.fetchall()]
            return noms_restaurants
        except sqlite3.Error as e:
            print('Erreur lors de la récupération des noms de restaurants :',
                  e)
            return []

    # Méthode pour enregistrer les plaintes dans la base de donnees
    def enregistrer_plaintes(self, valeur):
        cursor = self.obtenir_connexion().cursor()
        donnees = (valeur['nom_etablissement'], valeur['adresse'],
                   valeur['ville'], valeur['date_visite_client'],
                   valeur['nom'], valeur['prenom'],
                   valeur['description_probleme'])

        requete = ("INSERT INTO plaintes (nom_etablissement, adresse, "
                   "ville, date_visite_client, nom_client, "
                   "prenom_client, description_probleme) "
                   "VALUES (?, ?, ?, ?, ?, ?, ?)")
        try:
            cursor.execute(requete, donnees)

            self.connexion.commit()
            self.connexion.close()
            return True

        except sqlite3.Error as e:
            print('Erreur lors de l\'insertion des plaintes:', e)
            return False

    def chercher_dans_bd(self, email_utilisateur):
        cursor = self.obtenir_connexion().cursor()
        requete = "SELECT * FROM utilisateur WHERE email_utilisateur=?"
        try:

            cursor.execute(requete, (email_utilisateur,))
            recherche = cursor.fetchone()
            return recherche

        except sqlite3.Error as e:
            print('la recherche n\'a pas abouti', e)
            return False

    def enregistrer_utilisateur(self, valeur):
        cursor = self.obtenir_connexion().cursor()
        mdp_utilisateur_hache, salt = hacher_mot_de_passe(
            valeur['mdp_utilisateur'])
        donnees = (valeur['nom_utilisateur'],
                   ",".join(valeur['etablissement_surveiller']),
                   valeur['email_utilisateur'],
                   mdp_utilisateur_hache, salt)

        requete = ("INSERT INTO utilisateur (nom_utilisateur, "
                   "etablissement_surveiller"
                   ",email_utilisateur,mdp_utilisateur,salt) "
                   "VALUES (?, ?, ?, ?,?)")

        try:

            cursor.execute(requete, donnees)

            self.connexion.commit()
            self.connexion.close()
            return True

        except sqlite3.Error as e:
            print('Erreur lors de l\'insertion des utilisateurs :', e)
            return False
