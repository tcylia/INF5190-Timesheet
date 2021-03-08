# Copyright 2017 Jacques Berger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/heures.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None
    
    def get_horaire(self,id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM heures WHERE id like ?",(id,))
        horaire = cursor.fetchall()
        return horaire[0]

    def get_heures_jour(self, matricule, date_du_jour):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, code_de_projet, duree FROM heures WHERE matricule LIKE ? AND date_publication LIKE ?",(matricule, date_du_jour,))
        heures = cursor.fetchall()
        return heures

    def get_dates(self, matricule):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT DISTINCT date_publication FROM heures WHERE matricule LIKE ? ORDER BY date_publication", (matricule,))
        dates = cursor.fetchall()
        return dates
    
    def insert_heures(self, matricule, code_de_projet, date_publication, duree):
        connection = self.get_connection()
        cursor = self.get_connection().cursor()
        cursor.execute("INSERT INTO heures(matricule,code_de_projet,date_publication,duree) VALUES (?,?,?,?)",(matricule, code_de_projet, date_publication,duree))
        connection.commit()

    def modifier_heures(self, id, code_de_projet, duree):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE heures SET code_de_projet = ? , duree = ? WHERE id = ?", (code_de_projet,duree,id,))
        connection.commit()

    def supprimer_heures(self,id):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM heures WHERE id = ?", (id,))
        connection.commit()
    
    def get_jours_travailles(self, matricule, mois):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT date_publication FROM heures WHERE matricule LIKE ? AND date_publication LIKE ? ORDER BY date_publication", (matricule, mois+"%",))
        jours_travailles = cursor.fetchall()
        return jours_travailles

    def get_total_min_jour(self, matricule, date_du_jour):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT date_publication, SUM(duree) AS minutes FROM heures WHERE matricule LIKE ? AND date_publication LIKE ?", (matricule,date_du_jour,))
        min_par_jour = cursor.fetchall()
        return min_par_jour[0]