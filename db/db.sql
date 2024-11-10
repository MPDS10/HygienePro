create table if not exists violations(
    identifiant    INTEGER PRIMARY KEY,
    id_poursuite   INT,
    business_id    INT,
    date           INT,
    description    TEXT,
    adresse        VARCHAR,
    date_jugement  INT,
    etablissement  VARCHAR,
    montant        INT,
    proprietaire   VARCHAR,
    ville          INT,
    statut         VARCHAR,
    date_statut    INT,
    categorie      TEXT

);

create table if not exists plaintes(
    identifiant             INTEGER PRIMARY KEY,
    nom_etablissement       VARCHAR,
    adresse                 VARCHAR,
    ville                   VARCHAR,
    date_visite_client      INT,
    nom_client              VARCHAR,
    prenom_client           VARCHAR,
    description_probleme    TEXT
);

create table if not exists utilisateur(
    indentifiant                INTEGER PRIMARY KEY,
    nom_utilisateur             VARCHAR,
    etablissement_surveiller    VARCHAR,
    email_utilisateur           VARCHAR,
    mdp_utilisateur             VARCHAR,
    salt                        VARCHAR,
    photo_utilisateur           BLOB
);







