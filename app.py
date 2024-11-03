from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from datetime import date, timedelta
import os
import uuid
from flask_bcrypt import Bcrypt
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
bcrypt = Bcrypt(app)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='horaire_enseignant'
    )
db = get_db_connection()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cours')
def cours():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM cours")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('cours.html', data=data, status=status, msg=msg)

@app.route('/enregistrer_cours',methods=['GET','POST'])
def enregistrer_cours():
    idUp = request.form['idUp']
    nom = request.form['nom']
    
    if(idUp == ""): 
        val = (nom,)
        req = 'INSERT INTO `cours`( `nom`) VALUES (%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('cours',status='sucsess',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (nom,idUp)

             req = 'UPDATE `cours` SET `nom`=%s WHERE cours_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('cours',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_cours", methods=['POST', 'GET'])
def supprimer_cours():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        # Supprimer le cours
        cursor.execute("DELETE FROM cours WHERE cours_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('cours', status='info', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('cours', status='info', msg='La suppression a été effectuée avec succès'))

#GESTION DES NIVEAU DE CLASSE
@app.route('/niveaux')
def niveaux():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM niveaux")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('niveaux.html', data=data, status=status, msg=msg)

@app.route('/enregistrer_niveaux',methods=['GET','POST'])
def enregistrer_niveaux():
    idUp = request.form['idUp']
    nom = request.form['nom']
    
    if(idUp == ""): 
        val = (nom,)
        req = 'INSERT INTO `niveaux`( `nom`) VALUES (%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('niveaux',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (nom,idUp)

             req = 'UPDATE `niveaux` SET `nom`=%s WHERE niveau_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('niveaux',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_niveaux", methods=['POST', 'GET'])
def supprimer_niveaux():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM niveaux WHERE niveau_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('niveaux', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('niveaux', status='info', msg='La suppression a été effectuée avec succès'))

            #GESTION DES OPTIONS 
@app.route('/options')
def options():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM options")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('options.html', data=data, status=status, msg=msg)

@app.route('/enregistrer_options',methods=['GET','POST'])
def enregistrer_options():
    idUp = request.form['idUp']
    nom = request.form['nom']
    
    if(idUp == ""): 
        val = (nom,)
        req = 'INSERT INTO `options`( `nom`) VALUES (%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('options',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (nom,idUp)

             req = 'UPDATE `options` SET `nom`=%s WHERE option_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('options',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_options", methods=['POST', 'GET'])
def supprimer_options():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM options WHERE option_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('options', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('options', status='info', msg='La suppression a été effectuée avec succès'))

  #GESTION DES classes 
@app.route('/classe')
def classe():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT classes.classe_id,classes.nom,classes.niveau_id,classes.option_id,options.nom AS options ,niveaux.nom AS niveaux FROM classes JOIN options ON options.option_id=classes.option_id JOIN niveaux ON niveaux.niveau_id=classes.niveau_id")
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM options')
    options = cursor.fetchall()

    cursor.execute('SELECT * FROM niveaux')
    niveaux = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('classe.html', data=data, options=options,niveaux=niveaux,status=status, msg=msg)

@app.route('/enregistrer_classe',methods=['GET','POST'])
def enregistrer_classe():
    idUp = request.form['idUp']
    nom = request.form['nom']
    option = request.form['option']
    niveau = request.form['niveaux']
    
    if(idUp == ""): 
        val = (nom,niveau,option)
        req = 'INSERT INTO `classes`( `nom`,niveau_id,option_id) VALUES (%s,%s,%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('classe',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (nom,niveau,option,idUp)

             req = 'UPDATE `classes` SET `nom`=%s, niveau_id = %s, option_id = %s WHERE classe_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('classe',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_classe", methods=['POST', 'GET'])
def supprimer_classe():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM classes WHERE classe_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('classe', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('classe', status='info', msg='La suppression a été effectuée avec succès'))

#GESTION DES atributions des cours 
@app.route('/attributions_cours')
def attributions_cours():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT attributions_cours.attribution_id,attributions_cours.enseignant_id,attributions_cours.classe_id,attributions_cours.cours_id ,CONCAT(niveaux.nom,' ',classes.nom,' ',options.nom)AS classes,CONCAT(enseignants.nom,' ',enseignants.prenom) AS enseignant ,cours.nom AS cour FROM attributions_cours JOIN classes ON classes.classe_id=attributions_cours.classe_id JOIN cours ON attributions_cours.cours_id=cours.cours_id JOIN enseignants ON enseignants.enseignant_id=attributions_cours.enseignant_id JOIN  niveaux ON niveaux.niveau_id=classes.niveau_id JOIN options ON options.option_id=classes.option_id")
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM cours')
    cours = cursor.fetchall()

    cursor.execute('SELECT classes.classe_id,classes.nom,options.nom AS options ,niveaux.nom AS niveaux FROM classes JOIN options ON options.option_id=classes.option_id JOIN niveaux ON niveaux.niveau_id=classes.niveau_id')
    classes = cursor.fetchall()

    cursor.execute('SELECT * FROM enseignants')
    ensignants = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('attributions_cours.html', data=data,ensignants=ensignants, cours=cours,classes=classes,status=status, msg=msg)

@app.route('/enregistrer_attributions_cours',methods=['GET','POST'])
def enregistrer_attributions_cours():
    idUp = request.form['idUp']
    enseignant = request.form['enseignant']
    cours = request.form['cours']
    classe = request.form['classe']
    
    if(idUp == ""): 
        val = (enseignant,cours,classe)
        req = 'INSERT INTO `attributions_cours`( `enseignant_id`,cours_id,classe_id) VALUES (%s,%s,%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('attributions_cours',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (enseignant,cours,classe,idUp)

             req = 'UPDATE `attributions_cours` SET `enseignant_id`=%s, classe_id = %s, cours_id = %s WHERE attribution_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('attributions_cours',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_attributions_cours", methods=['POST', 'GET'])
def supprimer_attributions_cours():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM attributions_cours WHERE attribution_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('attributions_cours', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('attributions_cours', status='info', msg='La suppression a été effectuée avec succès'))


#GESTION DES atributions des cours 
@app.route('/horaires')
def horaires():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT attributions_cours.attribution_id,CONCAT(niveaux.nom,' ',classes.nom,' ',options.nom)AS classes,CONCAT(enseignants.nom,' ',enseignants.prenom) AS enseignant ,cours.nom AS cour FROM attributions_cours JOIN classes ON classes.classe_id=attributions_cours.classe_id JOIN cours ON attributions_cours.cours_id=cours.cours_id JOIN enseignants ON enseignants.enseignant_id=attributions_cours.enseignant_id JOIN  niveaux ON niveaux.niveau_id=classes.niveau_id JOIN options ON options.option_id=classes.option_id")
    attributions_cours = cursor.fetchall()

    

    cursor.execute("SELECT horaires.horaire_id ,horaires.attribution_id,horaires.jour_semaine,horaires.heures,CONCAT(enseignants.nom,' ',enseignants.prenom) AS enseignants,CONCAT(niveaux.nom,' ',classes.nom,' ',options.nom) AS classes,cours.nom AS cours FROM horaires JOIN attributions_cours on attributions_cours.attribution_id=horaires.attribution_id JOIN enseignants ON enseignants.enseignant_id=attributions_cours.enseignant_id JOIN classes ON attributions_cours.classe_id=classes.classe_id JOIN cours on cours.cours_id=attributions_cours.cours_id JOIN niveaux ON niveaux.niveau_id=classes.niveau_id JOIN options ON options.option_id=classes.option_id")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('horaires.html', data=data,attributions_cours=attributions_cours,status=status, msg=msg)

@app.route('/enregistrer_horaires',methods=['GET','POST'])
def enregistrer_horaires():
    idUp = request.form['idUp']
    attributions = request.form['attribution']
    jour = request.form['jours']
    heure = request.form['heure']
    
    if(idUp == ""): 
        val = (attributions,jour,heure)
        req = 'INSERT INTO `horaires`( `attribution_id`,jour_semaine,heures) VALUES (%s,%s,%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('horaires',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (attributions,jour,heure,idUp)

             req = 'UPDATE `horaires` SET attribution_id=%s, `jour_semaine`=%s, heure = %s WHERE horaire_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('horaires',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_horaires", methods=['POST', 'GET'])
def supprimer_horaire():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM horaires WHERE horaire_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('horaires', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('horaires', status='info', msg='La suppression a été effectuée avec succès'))

    #Pour generer les matricules automatiquement
def generate_matricule(): 
    db = get_db_connection() 
    cursor = db.cursor() 
    cursor.execute("SELECT MAX(CAST(SUBSTR(matricule, 4) AS UNSIGNED)) FROM enseignants") 
    max_id = cursor.fetchone()[0] 
    cursor.close() 
    db.close() 
    if max_id is None: 
        max_id = 0 
    return f"Mat{max_id + 1}"


#GESTION DES atributions des cours 
@app.route('/enseignants')
def enseignants():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM enseignants")
    data = cursor.fetchall()
    cursor.close()
    db.close()
    status = request.args.get('status')
    msg = request.args.get('msg')
    return render_template('enseignants.html', data=data,status=status, msg=msg)

@app.route('/enregistrer_enseignants',methods=['GET','POST'])
def enregistrer_enseignants():
    idUp = request.form['idUp']
    nom = request.form['nom']
    prenom = request.form['prenom']
    matricule = generate_matricule()
    date = request.form['date']
    adresse = request.form['adresse']
    telephone = request.form['telephone']
    password = request.form['password']
    email = request.form['email']
    matiere = request.form['matiere']
    
    if(idUp == ""): 
        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        val = (nom,prenom,matricule,date,adresse,telephone,hash,email,matiere)
        req = 'INSERT INTO `enseignants`(nom,prenom,matricule,date_naissance,adresse,telephone,password_hash,email,matiere) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor = db.cursor()
        cursor.execute(req,val)
        db.commit()
        return redirect(url_for('enseignants',status='info',msg='enregistrement effectuer avec succès'))
    else:
         if request.method == 'POST':
            
             val = (nom,prenom,date,adresse,telephone,email,matiere,idUp)

             req = 'UPDATE `enseignants` SET nom=%s, `prenom`=%s, date_naissance = %s ,adresse = %s ,telephone = %s, email=%s,matiere=%s WHERE enseignant_id=%s'
             curseur = db.cursor()
             curseur.execute(req,val)
             db.commit()
             return redirect(url_for('enseignants',status='info',msg='La modification effectuer avec succès'))

@app.route("/supprimer_enseignants", methods=['POST', 'GET'])
def supprimer_enseignants():
    id = request.form['idDel']
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:        
        cursor.execute("DELETE FROM enseignants WHERE enseignant_id = %s", (id,))
        
        db.commit()
    except mysql.connector.Error as err:
        db.rollback()
        print(f"Erreur: {err}")
        return redirect(url_for('enseignants', status='danger', msg='Erreur lors de la suppression'))
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('enseignants', status='info', msg='La suppression a été effectuée avec succès'))



if __name__ == '__main__':
    app.run(debug=True)
