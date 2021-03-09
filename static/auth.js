window.onload = () => {
    var formulaireAuthentification = document.getElementById("authentification");

    formulaireAuthentification.addEventListener("submit", (event) => {
        var authValide = true;
        var matricule = document.getElementById("matricule").value;
        var matriculeRegex = new RegExp("^[A-Z][A-Z][A-Z]-\\d\\d$");
        if (matricule === "") {
            document.getElementById("auth-err").innerHTML = "Ce champs est obligatoire. <br>";
            document.getElementById("auth-err").style.color = "#d1a2a2";
            authValide = false;
        }
        else if (!matriculeRegex.test(matricule)) {
            document.getElementById("auth-err").innerHTML = "Le matricule doit avoir un format 'XXX-NN'. <br>";
            document.getElementById("auth-err").style.color =  "#d1a2a2";
            authValide = false;
        }

        if (authValide == false) {
            event.preventDefault();
        }
        
    });
}

