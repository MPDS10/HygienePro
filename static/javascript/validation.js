function rechercherContraventions() {
    const du = document.getElementById("du").value;
    const au = document.getElementById("au").value;

    fetch(`/contrevenants?du=${du}&au=${au}`)
        .then(response => response.json())
        .then(data => {
            let tableHtml = "<table><tr><th>Nom de l'établissement</th><th>Nombre de contraventions</th></tr>";
            data.forEach(contrevenant => {
                tableHtml += `<tr><td>${contrevenant.nom_etablissement}</td><td>${contrevenant.nb_infractions}</td></tr>`;
            });
            tableHtml += "</table>";
            document.getElementById("resultats").innerHTML = tableHtml;
        })
        .catch(error => console.error('Erreur lors de la récupération des contrevenants :', error));
}

function remplirListeDeroulante() {
    fetch('/contrevenants/noms')
        .then(response => response.json())
        .then(data => {
            const select = document.getElementById("nomRestaurant");
            select.innerHTML = ""; // Effacer les anciennes options

            data.forEach(nomRestaurant => {
                const option = document.createElement("option");
                option.value = nomRestaurant;
                option.textContent = nomRestaurant;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Erreur lors de la récupération des noms de restaurants :', error));
}

function rechercherContraventionsParNom() {
    const nomRestaurant = document.getElementById("nomRestaurant").value;
    fetch(`/contrevenants/nom?nomRestaurant=${nomRestaurant}`)
        .then(response => response.json())
        .then(data => {
            let tableHtml = "<table><tr><th>Nom de l'établissement</th><th>Nombre de contraventions</th></tr>";
            data.forEach(contrevenant => {
                tableHtml += `<tr><td>${contrevenant.nom_etablissement}</td><td>${contrevenant.nb_infractions}</td></tr>`;
            });
            tableHtml += "</table>";
            document.getElementById("resultats").innerHTML = tableHtml;
        })
        .catch(error => console.error('Erreur lors de la récupération des contrevenants :', error));
}

window.onload = function() {
    remplirListeDeroulante();
};

// Cette fonction servira à valider le formulaire de plainte rempli par le client
function valider_plainte() {
    const valeur = {
        "nom_etablissement": document.getElementById("nom_etablissement").value,
        "adresse": document.getElementById("adresse").value,
        "ville": document.getElementById("ville").value,
        "date_visite_client": document.getElementById("date_visite_client").value,
        "nom": document.getElementById("nom_client").value,
        "prenom": document.getElementById("prenom_client").value,
        "description_probleme": document.getElementById("description_probleme").value
    };
    fetch('/soumettre_plainte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(valeur)
    })
    .then(validation => validation.json())
    .then(valeur => {
        if (valeur.redirect) {
            window.location.href = valeur.redirect;
        }
    })
    .catch(erreur => {
        console.error("Erreur : ", erreur);
    });
}

function creer_compte() {
    const compte = {
        "nom_utilisateur": document.getElementById("nom_utilisateur").value,
        "email_utilisateur": document.getElementById("email_utilisateur").value,
        "mdp_utilisateur": document.getElementById("mdp_utilisateur").value,
        "etablissement_surveiller": [document.getElementById("etablissement_surveiller").value]
    };
    fetch('/creer_compte', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(compte)
    })
        .then(validation => validation.json())
        .then(compte => {
            console.log("Réponse reçue après création de compte:", compte); // Ajout du print
            if (compte.redirect) {
                console.log("redirection accepte:", compte.redirect)
                window.location.href = compte.redirect;
            }
            if (compte.existing_account) {
                alert('Un compte avec cette adresse courriel existe déjà');
            }


        })
        .catch(erreur => {
            console.error("Erreur : ", erreur);
        });
}
