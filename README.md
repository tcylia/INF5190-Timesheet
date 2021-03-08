# TP1 INF5190

#### Auteur:

**Nom:** Tazaïrt 

**Prénom:** Cylia

**Code permanent:** TAZC29579700

## Développement d'une feuille de temps

Ce logiciel permet à des
employés de spécifier les heures travaillées et produire la 

facturation liée au temps travaillé.


##### Création d'un environnement virtuel 

`python3.9 -m venv env`

Pour activer l'environnement virtuel : `source env/bin/activate`


## Routes

**GET /** 

Définit la page d'accueil du site. 

**GET /\<matricule>/\<date_du_jour>** 

Définit la page permettant d'ajouter du temps sur des codes de 
projet pour la journée spécifiée dans l'URL.

La date du jour doit être en format ISO8601 et le matricule doit avoir
le format XXX-NN. 


**GET /\<matricule>/overview/\<mois>** Cette page affiche un résumé des

 heures travaillées pour un mois en particulier avec un calendrier qui
 
 mène vers la page de chaque jour du mois.

**GET /\<matricule>** Cette page doit afficher la liste de tous les mois où ce matricule

 a déclaré des heures travaillées. 


