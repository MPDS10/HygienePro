import json
from collections import defaultdict
from xml.sax.saxutils import escape
from flask import (Flask, Response, g, jsonify,
                   render_template, request, url_for, redirect)
from datetime import datetime
import database
from jsonschema import validate
from database import Database
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

app = Flask(__name__, static_url_path="/static", static_folder="static")

# ajout de la tache qui fera la mise a jour des donnees chaque jour a minuit
maj = BackgroundScheduler(daemon=True)
maj.add_job(database.inserer_donnee_csv, args=(database.url,
                                               database.chemin_db,
                                               database.nom_table),
            trigger=CronTrigger(hour=0))

schema_json_plaintes = {
    "type": "object",
    "properties": {
        "nom_etablissement": {"type": "string"},
        "adresse": {"type": "string"},
        "ville": {"type": "string"},
        "date_visite_client": {"type": "string", "format": "datetime"},
        "nom": {"type": "string"},
        "prenom": {"type": "string"},
        "description_probleme": {"type": "string"}

    },
    "required": ["nom_etablissement", "adresse", "ville", "date_visite_client",
                 "nom", "prenom", "description_probleme"]
}

schema_json_profil = {
    "type": "object",
    "properties": {
        "nom_utilisateur": {"type": "string"},
        "email_utilisateur": {"type": "string", "format": "email"},
        "mdp_utilisateur": {"type": "string"},
        "etablissement_surveiller": {"type": "array",
                                     "items": {"type": "string"}}
    },
    "required": ["nom_utilisateur", "email_utilisateur", "mdp_utilisateur",
                 "etablissement_surveiller"]
}


def obtenir_bd():
    bd = getattr(g, '_database', None)
    if bd is None:
        g._database = Database()
    return g._database


@app.route('/')
def acceuil():
    return render_template("page_acceuil.html")


@app.route('/recherche', methods=['GET'])
def recherche():
    violation = obtenir_bd().obtenir_violations()
    recherche_csv = request.args.get('clavier').lower()
    contraventions = []
    poursuites = set()

    for contravention in violation:
        etablissement = contravention[6]
        proprietaire = contravention[8]
        adresse = contravention[4]

        if (etablissement is not None and recherche_csv in str(etablissement)
                .lower()):
            id_poursuite = contravention[1]

            if id_poursuite not in poursuites:
                contraventions.append(contravention)
                poursuites.add(id_poursuite)

        elif (proprietaire is not None and recherche_csv in
              str(proprietaire).lower()):
            id_poursuite = contravention[1]

            if id_poursuite not in poursuites:
                contraventions.append(contravention)
                poursuites.add(id_poursuite)

        elif adresse is not None and recherche_csv in str(adresse).lower():
            id_poursuite = contravention[1]

            if id_poursuite not in poursuites:
                contraventions.append(contravention)
                poursuites.add(id_poursuite)

    return render_template('page_resultat.html', contraventions=contraventions)


@app.route('/contrevenants', methods=["GET"])
def obtenir_contraventions():
    violation = obtenir_bd().obtenir_violations()
    du = datetime.strptime(request.args.get("du"), "%Y-%m-%d")
    au = datetime.strptime(request.args.get("au"), "%Y-%m-%d")
    contraventions = defaultdict(int)

    for contravention in violation:
        date_infraction = datetime.strptime(str(contravention[2]), "%Y%m%d")
        if du <= date_infraction <= au:
            contraventions[contravention[6]] += 1

    # Convertir le dictionnaire en une liste de dictionnaires pour
    # correspondre au format attendu
    contraventions_liste = [{"nom_etablissement": nom_etablissement,
                             "nb_infractions": nb_infractions} for
                            nom_etablissement, nb_infractions in
                            contraventions.items()]

    return jsonify(contraventions_liste)


@app.route('/contrevenants/noms', methods=["GET"])
def obtenir_noms_restaurants():
    noms_restaurants = obtenir_bd().obtenir_noms_restaurants()
    return jsonify(noms_restaurants)


@app.route('/doc')
def documenter_api():
    return render_template('page_documentation_api.html')


@app.route('/liste_etablissements')
def afficher_liste_etablissements():
    liste_etablissements = obtenir_bd().obtenir_violations()
    liste_etablissements_tri = defaultdict(int)

    # compnter les infractions pas etablissements
    for liste_etablissement in liste_etablissements:
        etablissements = liste_etablissement[6]
        liste_etablissements_tri[etablissements] += 1

    liste_etablissements_filtre = sorted(liste_etablissements_tri.items(),
                                         key=lambda x: x[1], reverse=True)
    etablissements = [{"nom_etablissment": etablissements,
                       "nb_infractions": nb_infractions} for
                      etablissements, nb_infractions
                      in liste_etablissements_filtre]

    return render_template("page_liste_etablissement_infractions.html",
                           etablissements=etablissements)


@app.route('/liste_etablissements_xml')
def afficher_liste_etablissements_xml():
    liste_etablissements = obtenir_bd().obtenir_violations()
    liste_etablissements_tri = defaultdict(int)

    # Sert à compter les infractions par établissement
    for liste_etablissement in liste_etablissements:
        etablissements = liste_etablissement[6]
        liste_etablissements_tri[etablissements] += 1

    # Pour TRIER les établissements par nombre d'infractions
    liste_etablissements_filtre = sorted(liste_etablissements_tri.items(),
                                         key=lambda x: x[1],
                                         reverse=True)

    # Créer une liste d'établissements au format XML
    donnee_liste_xml = '<etablissements>\n'
    for etablissement, nb_infractions in liste_etablissements_filtre:
        # Échapper les caractères spéciaux dans les données XML
        etablissement_escaped = escape(etablissement)
        donnee_liste_xml += (f'\t<etablissement>\n\t\t'
                             f'<nom>{etablissement_escaped}'
                             f'</nom>\n\t\t<nb_infractions>'
                             f'{nb_infractions}</nb_infractions>'
                             f'\n\t</etablissement>\n')

    donnee_liste_xml += '</etablissements>'

    # Retourner la réponse avec le contenu XML et le type MIME approprié
    return Response(donnee_liste_xml, mimetype='text/xml; charset=utf-8')


@app.route('/liste_etablissements_csv')
def afficher_liste_etablissements_csv():
    liste_etablissements = obtenir_bd().obtenir_violations()
    liste_etablissements_tri = defaultdict(int)

    # Compter les infractions par établissement
    for liste_etablissement in liste_etablissements:
        etablissements = liste_etablissement[6]
        liste_etablissements_tri[etablissements] += 1

    # Trier les établissements par nombre d'infractions
    liste_etablissements_filtre = sorted(liste_etablissements_tri.items(),
                                         key=lambda x: x[1],
                                         reverse=True)

    # Créer une liste d'établissements au format CSV
    donnee_liste_csv = "Nom établissement,Nombre infractions\n"
    for etablissement, nb_infractions in liste_etablissements_filtre:
        donnee_liste_csv += f'"{etablissement}",{nb_infractions}\n'

    # Retourner la réponse avec le contenu CSV et le type MIME approprié
    return Response(donnee_liste_csv, mimetype='text/csv; charset=utf-8',
                    headers={'Content-Disposition': 'attachment; '
                                                    'filename='
                                                    'etablissements.csv'})


@app.route('/deposer_plainte')
def deposer_plainte():
    return render_template('page_plaintes.html')


@app.route('/soumettre_plainte', methods=['POST'])
def soumettre_plainte():
    valeur = request.get_json()
    try:
        validate(valeur, schema_json_plaintes)

        enregistrement = obtenir_bd().enregistrer_plaintes(valeur)

        if enregistrement:
            return jsonify({'Message': 'Plainte enregistrée avec succès',
                            'redirect': url_for('acceuil')})

    except IOError:
        return jsonify({'Erreur': 'lors de l\'enregistrement de '
                                  'la plainte dans la base de données'}), 500


@app.route('/inscription')
def inscription():
    return render_template('page_utilisateur.html')


@app.route('/creer_compte', methods=['POST'])
def creer_compte():
    compte = request.get_json()
    try:
        validate(compte, schema_json_profil)
        verifier_compte = (obtenir_bd().chercher_dans_bd
                           (compte['email_utilisateur']))

        if verifier_compte:
            return jsonify({'erreur': 'Un compte avec cette adresse courriel '
                                      'existe déjà',
                            'existing_account': True}), 200

        verif_compte_ok = obtenir_bd().enregistrer_utilisateur(compte)

        if verif_compte_ok:
            return jsonify({'redirect': url_for('acceuil')}), 302, {'Location':
                                                                        url_for('acceuil')}
        else:
            return jsonify({'erreur': 'Lors de l\'enregistrement du compte dans '
                                      'la base de données'}), 500

    except IOError as e:
        print("Erreur IO:", e)
        return jsonify({'erreur': str(e)}), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template("page_404.html"), 404
