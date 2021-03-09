window.onload = () => {
    var formulaireModificationHoraire = document.getElementById("modificationhoraire");

    formulaireModificationHoraire.addEventListener("submit", (event) => {
        var modifValide = true;
        codeProjetModif = document.getElementById("codeprojet").value;
        dureeModif = document.getElementById("duree").value;

        if (codeProjetModif === "") {
            document.getElementById("code-projet-modif-err").innerHTML = "Le code de projet est un champs obligatoire. <br>";
            document.getElementById("code-projet-modif-err").style.color =  "#d1a2a2";
            ajoutValide = false;
        }
 
        if (dureeModif === "") {
            document.getElementById("duree-modif-err").innerHTML = "La duree est un champs obligatoire. <br>";
            document.getElementById("duree-modif-err").style.color =  "#d1a2a2";
            modifValide = false;
        }
 
        if (modifValide == false) {
            event.preventDefault();
        }
        
    });
}

