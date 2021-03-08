window.onload = () => {
    var formulaireAuthentification = document.getElementById("authentification");
    var formulaireAjoutHoraire = document.getElementById("ajouthoraire");
    var formulaireModificationHoraire = document.getElementById("modificationhoraire");

    formulaireAuthentification.addEventListener("submit", (event) => {
        var authValide = true;
        var matricule = document.getElementById("matricule").value;
        var matriculeRegex = new RegExp("^[A-Z][A-Z][A-Z]-\\d\\d$");
        if (matricule === "") {
            document.getElementById("auth-err").innerHTML = "Ce champs est obligatoire.";
            document.getElementById("auth-err").style.color = "#7a5454";
            authValide = false;
        }
        else if (!matriculeRegex.test(matricule)) {
            document.getElementById("auth-err").innerHTML = "Le matricule doit avoir un format XXX-NN";
            document.getElementById("auth-err").style.color = "#7a5454";
            authValide = false;
        }

        if (authValide == false) {
            event.preventDefault();
        }
        
    });

    formulaireAjoutHoraire.addEventListener("submit", (event) => {
       var ajoutValide = true;
       codeProjet = document.getElementById("codeprojet").value;
       duree = document.getElementById("duree").value;

       if (codeProjet === "") {
           document.getElementById("code-projet-err").innerHTML = "Le code de projet est un champs obligatoire";
           document.getElementById("code-projet-err").style.color =  "#7a5454";
           ajoutValide = false;
       }

       if (duree === "") {
        document.getElementById("duree-err").innerHTML = "La duree est un champs obligatoire";
        document.getElementById("duree-err").style.color =  "#7a5454";
        ajoutValide = false;
       }

       if (ajoutValide == false) {
           event.preventDefault();
       }
    });

    formulaireModificationHoraire.addEventListener("submit", (event) => {
        var modifValide = true;
        codeProjetModif = document.getElementById("codeprojet").value;
        dureeModif = document.getElementById("duree").value;

        if (codeProjetModif === "") {
            document.getElementById("code-projet-modif-err").innerHTML = "Le code de projet est un champs obligatoire";
            document.getElementById("code-projet-modif-err").style.color =  "#7a5454";
            ajoutValide = false;
        }
 
        if (dureeModif === "") {
            document.getElementById("duree-modif-err").innerHTML = "La duree est un champs obligatoire";
            document.getElementById("duree-modif-err").style.color =  "#7a5454";
            modifValide = false;
        }
 
        if (modifValide == false) {
            event.preventDefault();
        }
        
    });
}

