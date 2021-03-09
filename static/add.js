window.onload = () => {
    var formulaireAjoutHoraire = document.getElementById("ajouthoraire");
     
    function clean() {
        document.getElementById("code-projet-err").innerHTML = "";
        document.getElementById("duree-err").innerHTML = "";
    }

    formulaireAjoutHoraire.addEventListener("submit", (event) => {
       clean();
       var ajoutValide = true;
       codeProjet = document.getElementById("codeprojet").value;
       duree = document.getElementById("duree").value;

       if (codeProjet === "") {
           document.getElementById("code-projet-err").innerHTML = "Le code de projet est un champs obligatoire. <br>";
           document.getElementById("code-projet-err").style.color =  "#d1a2a2";
    
           ajoutValide = false;
       }

       if (duree === "") {
        document.getElementById("duree-err").innerHTML = "La duree est un champs obligatoire";
        document.getElementById("duree-err").style.color =   "#d1a2a2";
        ajoutValide = false;
       }

       if (ajoutValide == false) {
           event.preventDefault();
       }
    });

   
}

