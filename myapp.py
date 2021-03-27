import pymysql
conn = pymysql.connect(
        host= 'project.cx3gwzviwakr.us-east-1.rds.amazonaws.com', #endpoint link
        port = 3306,
        user = 'ashish',
        password = '12345678',
        db = 'project' )
from flask import Flask, render_template, request, jsonify,session
import requests
import json
import csv

app = Flask(__name__)

covid_url_template = 'https://covid-api.mmediagroup.fr/v1/cases?country=United Kingdom'

@app.route('/cases', methods=['POST','GET'])
def getdeck():
    response = requests.get(covid_url_template)
    cur=conn.cursor()
    if response.ok:
        parsed = response.json()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>",parsed)

        cur.execute("""INSERT INTO project.covid (country, confirmed, recovered, deaths, updated_on) VALUES ('{}', {}, {}, {}, '{}')""".format(parsed['All']['country'], parsed['All']['confirmed'], parsed['All']['recovered'], parsed['All']['deaths'], parsed['Anguilla']['updated']))
        conn.commit()
        return jsonify(parsed)
    else:
        return jsonify(response.reason)

@app.route('/casedetails', methods=['GET'])
def deck():
    cur=conn.cursor()
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    cur.execute("""SELECT * from project.covid""")
    details=cur.fetchall()
    print(details[:])
    if len(details):
        return jsonify({'data':len(details)},details[:]), 200
    return jsonify({'error':'No data present'}), 404

@app.route('/casedetails/<updated>', methods=['GET'])
def one_deck(updated):
    cur=conn.cursor()
    cur.execute("""SELECT * FROM project.deckdata where updated_on = '{}' """.format(updated))
    details=cur.fetchall()
    if len(details):
        return jsonify({'data':details[0]}), 200
    return jsonify({'message':'Dstails of this timestamp does not exist'}), 404

@app.route('/casedetails/update/<country>/<confirmed>/<recovered>/<deaths>/<updated>', methods=['PUT','GET'])
def update_characteristics(country, confirmed, recovered, deaths, updated):
    cur=conn.cursor()
    cur.execute("""SELECT * FROM project.covid WHERE updated_on='{}' """.format(updated))
    details=cur.fetchall()
    if not len(details):
        return jsonify({'error':'No such timestamp exists'})
    rows_update = cur.execute("""UPDATE project.covid set country='{}', confirmed={}, recovered={}, deaths={} WHERE updated_on='{}'""".format(country, confirmed, recovered, deaths, updated))
    conn.commit()
    return jsonify({'country':country, 'confirmed':confirmed, 'recovered':recovered, 'deaths':deaths, 'updated':updated}), 200

@app.route('/casedetails/delete/<updated>', methods=['DELETE','GET'])
def delete_deck(updated):
    cur=conn.cursor()
    cur.execute("""SELECT * FROM project.covid WHERE updated_on='{}'""".format(updated))
    details=cur.fetchall()
    if len(details):
        deletedRows=cur.execute("""DELETE from project.covid WHERE updated_on='{}'""".format(updated))
        conn.commit()
        return jsonify({'ID':id, 'Message':'Deleted'}), 200
    return jsonify({"message":"The timestamp doesn't exist"}), 404

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5050, ssl_context=('cert.pem', 'key.pem'))
