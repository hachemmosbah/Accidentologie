#!/usr/bin/env python
# coding: utf-8


# import librery 

from flask import render_template, request
from app.functions import create_plot, create_plot1, create_plot2, prediction
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import input_required
from flask import Blueprint, render_template 
from flask_login import login_required, current_user
from . import db
from .models import Formdata, Formpred, Pred
import logging



# secret key
#app.config['SECRET_KEY'] = 'A2444EES'

class loginForm(FlaskForm):
  """ call year from index.html"""
  year = StringField('year', validators=[input_required()])
  age1 = StringField('age1')
  age2 = StringField('age2')

class loginForm1(FlaskForm):
  """ call year from index.html"""
  year1 = StringField('year1', validators=[input_required()])
  age1 = StringField('age1')

app = Blueprint('main', __name__)

# Création de route index (page principale)
@app.route('/')
def index():
    
    return render_template('index.html')



@app.route('/data', methods = ['GET', 'POST'])
def data():
  """ call index.html in template """
# treatment of dataframe and query
  names=['code_departement', 'nom_departement', 'code_region', 'nom_region']
  df = pd.read_csv('departements-france.csv',
                            header=None, skiprows=[0], names=names)
  list_code_departement = df.code_departement.tolist()
  list_nom_departement = df.nom_departement.tolist()

  list_code_departement1 = []
  list_code_departement2 = [971,972,973,974,976]

  for i in range(1, len(list_code_departement)-5):
      i = i*10
      list_code_departement1.append(i)
      
  list_code_departement = list_code_departement1 + list_code_departement2
  list_code_departement.insert(29, 201)
  list_code_departement.insert(30, 202)
  list_code_departement.remove(200)

  

  form = loginForm()
 

# condition validation constraint 
  if form.validate_on_submit():
    return 
  else:
    return render_template('data.html', list_code_departement=list_code_departement, 
                            list_nom_departement=list_nom_departement, form=form,  name=current_user.name)


@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
  """ call dashbord.html in tamplate """
# request method for post
  request.method == 'POST'

# call variable to tamplate index.html
  year = request.form.get('year')
  departement = request.form.get('departement')

  unhurt = request.form.get('unhurt') != None
  dead = request.form.get('dead') != None

  hospitalize = request.form.get('hospitalize') != None
  hurt_light =request.form.get('hurt_light') != None

  age1 = request.form.get('age1')
  age2 = request.form.get('age2')

  men = request.form.get('men')!= None
  women = request.form.get('women')!= None
  
  user_ = current_user.get_id()
  data = Formdata( year = year, departement=departement, unhurt=unhurt, dead=dead, hospitalize=hospitalize,
                  hurt_light=hurt_light, age1=age1,age2=age2, men=men, women=women, user_id =user_)

  db.session.add(data)
  db.session.commit()      

  plot1 = create_plot(year, departement ,1, 1, age1, age2, "INDEMNS", 'rgba(230, 36, 36, 0.5)')
  plot2 = create_plot(year, departement,1, 2, age1, age2, "TUÉS", 'rgba(4, 0, 247, 0.5)')
  plot3 = create_plot(year, departement, 1,  3, age1, age2, "BLESSÉS HOSPITALISÉS" , 'rgba(54, 214, 71, 0.5)')
  plot4 = create_plot(year, departement,1, 4 , age1, age2, "BLESSÉS LEGERÉS",'rgba(0, 0, 0, 0.5)')
  
  plot5 = create_plot(year, departement ,2, 1, age1, age2, "INDEMNES", 'rgba(230, 36, 36, 0.5)')
  plot6 = create_plot(year, departement,2, 2, age1, age2, "TUÉES" ,'rgba(4, 0, 247, 0.5)')
  plot7 = create_plot(year, departement, 2,  3, age1, age2, "BLESSÉES HOSPITALISÉES", 'rgba(54, 214, 71, 0.5)')
  plot8 = create_plot(year, departement,2, 4 , age1, age2, "BLESSÉES LEGERÉES", 'rgba(0, 0, 0, 0.5)')
  
  plot9 = create_plot1(year)
  plot10 = create_plot2(year)
  
  # return the tamplate
  return render_template('graph.html', plot1= plot1, plot2 = plot2, plot3 = plot3, plot4 = plot4,
    plot5 = plot5, plot6 = plot6, plot7 = plot7, plot8 = plot8,plot9=plot9,plot10 = plot10, unhurt = unhurt
    , dead = dead, hospitalize= hospitalize,hurt_light= hurt_light, age1= age1, age2= age2, men = men, women= women,
    year=year, name=current_user.name)
  
@app.route('/prediction', methods = ['GET', 'POST'])
def pred():
  names=['code_departement', 'nom_departement', 'code_region', 'nom_region']
  df = pd.read_csv('departements-france.csv',
                            header=None, skiprows=[0], names=names)
  list_code_departement = df.code_departement.tolist()
  list_nom_departement = df.nom_departement.tolist()

  list_code_departement1 = []
  list_code_departement2 = [971,972,973,974,976]

  for i in range(1, len(list_code_departement)-5):
      i = i*10
      list_code_departement1.append(i)
      
  list_code_departement = list_code_departement1 + list_code_departement2
  list_code_departement.insert(29, 201)
  list_code_departement.insert(30, 202)
  list_code_departement.remove(200)

  form1 = loginForm1()
# condition validation constraint 
  if form1.validate_on_submit():
    return
  else :
    return render_template('prediction.html', list_code_departement=list_code_departement 
      , list_nom_departement=list_nom_departement, form1=form1, name= current_user.name)

@app.route('/result', methods = ['GET', 'POST'])
def result():
    request.method == 'POST'
    year1 = request.form.get('year1')
    departement1 = request.form.get('departement1')
    age1 = request.form.get('age1')
    gender1 = request.form.get('gender')
    
    location1 = request.form.get('location')
    intersection1 = request.form.get('intersection')
    light1 = request.form.get('light')
    user_ = current_user.get_id()
    
    pred = prediction(year1, gender1, age1, location1, intersection1, light1, departement1)
    
    data1 = Formpred( year = year1, departement=departement1, age = age1, gender=gender1, location =location1,
                      intersection=intersection1, light=light1, user_id = user_)
    
    db.session.add(data1)

    db.session.flush()
    formpred_id = data1.id
    data2 = Pred(pred=pred, user_id= user_, formpred_id = formpred_id)  
  
    db.session.add(data2)
    db.session.commit()  

    # create logger  
    if pred == 0:
      logging.basicConfig(filename='erreur.log',level=logging.DEBUG,\
        format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
      logging.warning('Warning Error utilisateur %s: %s', user_ , 'Erreur prediction')

    return render_template('result.html', year1 = year1, departement1 = departement1
            , age = age1, gender = gender1, location1 = location1
            , intersection= intersection1, light1 = light1, pred = pred, name=current_user.name)