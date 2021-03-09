from flask import Flask
from flask import render_template
from flask import g
from flask import make_response
from flask import request
from flask import redirect
from flask import url_for
from datetime import datetime, date, timedelta
from .database import Database
import calendar
import re
from calendar import monthrange

app = Flask(__name__)

msg_err_date = "La date doit avoir un format ISO 8601"
msg_err_matricule = "Le matricule doit avoir le format XXX-NN"
msg_err_date_matricule = (
    "Le matricule doit avoir le format XXX-NN \n La date doit avoir le format ISO 8601"
)
msg_err_id = "Utilisateur non existant"
msg_err_champs = "Tout les champs sont obligatoires"
msg_mois_invalide = "Mois invalide"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.disconnect()

@app.errorhandler(404)
def page_not_found(error):
    return render_template("erreur.html"), 404


def valider_matricule(matricule):
    pattern = "^[A-Z][A-Z][A-Z]-\d\d$"
    resultat = re.match(pattern, matricule)
    if resultat:
        return True
    else:
        return False


def valider_date(date_du_jour):
    patternISO = "^((1[6789]|[2-9][0-9])[0-9]{2}-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))$|^((1[6789]|[2-9][0-9])[0-9]{2}-(0[469]|11)-(0[1-9]|[12][0-9]|30))$|^((16|[248][048]|[3579][26])00)|(1[6789]|[2-9][0-9])(0[48]|[13579][26]|[2468][048])-02-(0[1-9]|1[0-9]|2[0-9])$|^(1[6789]|[2-9][0-9])[0-9]{2}-02-(0[1-9]|1[0-9]|2[0-8])$"
    resultat = re.match(patternISO, date_du_jour)
    if resultat:
        return True
    else:
        return False


def valider_mois(mois):
    patternMois = "^\d{4}-([0]\d|1[0-2])$"
    resultat = re.match(patternMois, mois)
    if resultat:
        return True
    else:
        return False


def calculer_nb_jours_par_mois(mois):
    _mois = datetime.strptime(mois, "%Y-%m")
    return monthrange(_mois.year, _mois.month)[1]


def calculer_min_par_jour(matricule, date_du_jour):
    min_par_jour = get_db().get_total_min_jour(matricule, date_du_jour)
    if min_par_jour is None:
        return 0
    else:
        return min_par_jour

def obtenir_liste_mois(dates_string, liste_dates, liste_mois_mult):
    liste_mois = []
    # transformer liste de dates (String) en objet Datetime
    for dates in dates_string:
        date = datetime.strptime(str(dates[0]), "%Y-%m-%d")
        liste_dates.append(date)
    # extraire le mois et l'annee de la date
    for dates in liste_dates:
        mois = []
        mois_iso = dates.strftime("%Y-%m")
        mois_string = dates.strftime("%B %Y")
        mois.append(mois_iso)
        mois.append(mois_string)
        liste_mois_mult.append(mois)
    
    duplicate = set()
    for i in liste_mois_mult:
        srtd = tuple(sorted(i))
        if srtd not in duplicate:
            liste_mois.append(i)
            duplicate.add(srtd)
    return liste_mois


def get_calendar(matricule,mois):
    nb_jours = calculer_nb_jours_par_mois(mois)
    liste_jours_par_mois = []
    day_month_min = []
    for i in range(1, nb_jours + 1):
        data = []
        nb_min = 0
        if i < 10:
            day_of_month = "0" + str(i)
        if i >= 10:
            day_of_month = "" + str(i)
        liste_jours_par_mois.append(mois + "-" + day_of_month)
        nb_min = calculer_min_par_jour(matricule, liste_jours_par_mois[i - 1])[1]
        data.append(liste_jours_par_mois[i - 1])
        if nb_min is None:
            nb_min = 0
            data.append(nb_min)
        else:
            data.append(nb_min)
        day_month_min.append(data)
    
    return day_month_min

def reculer_un_jour(matricule, date_du_jour):
    _matricule = matricule
    _date = date_du_jour
    day_before = datetime.strptime(_date, "%Y-%m-%d")
    day_before -= timedelta(days=1)
    day_before = day_before.strftime("%Y-%m-%d")
    return day_before

def avancer_un_jour(matricule, date_du_jour):
    _matricule = matricule
    _date = date_du_jour
    day_after = datetime.strptime(_date, "%Y-%m-%d")
    day_after += timedelta(days=1)
    day_after = day_after.strftime("%Y-%m-%d")
    return day_after

def reculer_un_mois(matricule, mois):
    mois_precedent = datetime.strptime(mois, "%Y-%m")
    mois_precedent -= timedelta(weeks=4)
    mois_precedent = mois_precedent.strftime("%Y-%m")
    return mois_precedent

def avancer_un_mois(matricule, mois):
    mois_suivant = datetime.strptime(mois, "%Y-%m")
    mois_suivant += timedelta(weeks=5)
    mois_suivant = mois_suivant.strftime("%Y-%m")
    return mois_suivant

def get_mois_string(mois):
    _mois = datetime.strptime(mois, "%Y-%m")
    mois_string = datetime.strftime(_mois,"%B %Y")
    return mois_string


@app.route("/", methods=["GET", "POST"])
def formulaire():
    if request.method == "GET":
        return render_template("index.html")
    else:
        matricule = request.form["matricule"]
        date_jour = date.today().strftime("%Y-%m-%d")
        if matricule == "":
            return render_template("index.html", error=msg_err_champs)
        if valider_matricule(matricule) == False:
            return render_template("index.html", error=msg_err_matricule)
        else:
            return redirect(
                url_for("heure", matricule=matricule, date_du_jour=date_jour)
            )


@app.route("/<matricule>/<date_du_jour>", methods=["GET"])
def heure(matricule, date_du_jour):
    heures = get_db().get_heures_jour(matricule, date_du_jour)

    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    return render_template(
        "ajouthoraire.html",
        matricule=matricule,
        date_du_jour=date_du_jour,
        heures=heures,
    )


@app.route("/<matricule>/<date_du_jour>/confirmation", methods=["POST"])
def confirmation(matricule, date_du_jour):
    heures = get_db().get_heures_jour(matricule, date_du_jour)
    code_projet = request.form["codeprojet"]
    duree = request.form["duree"]
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    if code_projet == "" or duree == "":
        return render_template(
            "ajouthoraire.html",
            heures=heures,
            matricule=matricule,
            date_du_jour=date_du_jour,
            msgerr=msg_err_champs,
        )
    else:
        get_db().insert_heures(matricule, code_projet, date_du_jour, duree)
    return redirect(url_for("heure", matricule=matricule, date_du_jour=date_du_jour))


@app.route("/delete/<matricule>/<date_du_jour>/<id>", methods=["POST", "GET"])
def supprimer(id, matricule, date_du_jour):
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    if id is None:
        return render_template("erreur.html", err=msg_err_id)
    myID = get_db().get_horaire(id)
    get_db().supprimer_heures(id)
    return redirect(url_for("heure", matricule=matricule, date_du_jour=date_du_jour))


@app.route("/edit/<matricule>/<date_du_jour>/<id>", methods=["POST", "GET"])
def modifier(id, matricule, date_du_jour):
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    if id is None:
        return render_template("erreur.html", err=msg_err_id)
    horaire = get_db().get_horaire(id)
    return render_template(
        "modifierheure.html",
        matricule=matricule,
        date_du_jour=date_du_jour,
        id=horaire[0],
    )


@app.route("/update/<matricule>/<date_du_jour>/<id>", methods=["POST", "GET"])
def mettre_a_jour(id, matricule, date_du_jour):
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    if id is None:
        return render_template("erreur.html", err=msg_err_id)
    code_projet = request.form["codeprojet"]
    duree = request.form["duree"]

    if code_projet == "" or duree == "":
        return render_template(
            "modifierheure.html",
            matricule=matricule,
            date_du_jour=date_du_jour,
            id=id,
            error=msg_err_champs,
        )
    else:
        get_db().modifier_heures(id, code_projet, duree)
    return redirect(url_for("heure", matricule=matricule, date_du_jour=date_du_jour))


@app.route("/<matricule>/overview/<mois>")
def overview(matricule, mois):
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_mois(mois) == False:
        return render_template("erreur.html", err=msg_mois_invalide)
    mois_string = get_mois_string(mois)
    day_month_min = get_calendar(matricule,mois)
    return render_template(
        "overview.html", matricule=matricule, mois=mois, day_month_min=day_month_min,
                        mois_string=mois_string
    )


@app.route("/<matricule>")
def listemois(matricule):
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    dates_string = get_db().get_dates(matricule)
    liste_dates = []
    liste_mois_unsorted = []
    liste_mois = obtenir_liste_mois(dates_string, liste_dates, liste_mois_unsorted)
    return render_template("listemois.html", matricule=matricule, liste_mois=liste_mois)


@app.route("/<matricule>/<date_du_jour>/hier")
def jour_precedent(matricule, date_du_jour):
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    jour_precedent = reculer_un_jour(matricule,date_du_jour)
    return redirect(url_for("heure", matricule=matricule, date_du_jour=jour_precedent))


@app.route("/<matricule>/<date_du_jour>/demain")
def jour_suivant(matricule, date_du_jour):
    if valider_matricule(matricule) == False and valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date_matricule)
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    if valider_date(date_du_jour) == False:
        return render_template("erreur.html", err=msg_err_date)
    jour_suivant = avancer_un_jour(matricule,date_du_jour)
    return redirect(url_for("heure", matricule=matricule, date_du_jour=jour_suivant))


@app.route("/<matricule>/overview/<mois>/mois_precedent")
def mois_precedent(matricule, mois):
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    mois_precedent = reculer_un_mois(matricule,mois)
    return redirect(url_for("overview", matricule=matricule, mois=mois_precedent))


@app.route("/<matricule>/overview/<mois>/mois_suivant")
def mois_suivant(matricule, mois):
    if valider_matricule(matricule) == False:
        return render_template("erreur.html", err=msg_err_matricule)
    mois_suivant = avancer_un_mois(matricule, mois)
    return redirect(url_for("overview", matricule=matricule, mois=mois_suivant))
