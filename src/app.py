# Librerias para conexion
from flask import Flask, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import requests

# URL DEL WEB HOOK
webhook_url = "https://webhook.site/14693700-0cce4ef4-9961-e927cf90c008"

app = Flask(__name__)

# URI database mongo by dave *ESTA URL ESTARA DISPONIBLE 2 DIAS*
app.config['MONGO_URI']='mongodb+srv://dave:123ok@cluster0-yxxsk.mongodb.net/todoLegal'

mongo = PyMongo(app)

# CREAR NUEVO
@app.route('/vcambio',methods=['POST'])
def create_vcambio():
    print(request.json)
    fecha = request.json['fecha']
    open_ = request.json['open']
    high = request.json['high']
    low = request.json['low']
    close = request.json['close']
    adjClose = request.json['adjclose']
    tipo = request.json['tipo']
    
    id_saved = mongo.db.vcambio.insert({"fecha":fecha,"open":open_,"high":high,"low":low,"close":close,"adjClose":adjClose,"tipo":tipo})
    return {'message':'Guardado: '+str(id_saved)}

# OBTENER VALORES DE CAMBIO
@app.route('/vcambio', methods=['GET'])
def get_vcambios():
    vcambios = mongo.db.vcambio.find()
    response = json_util.dumps(vcambios)
     response_w = requests.post(webhook_url, data=response,headers={'Content-Type': 'application/json'})
    return Response(response, mimetype="application/json")

# OBTENER POR ID
@app.route('/vcambio/<id>', methods=['GET'])
def get_vcambioId(id):
    vcambio = mongo.db.vcambio.find_one({'_id': ObjectId(id) })
    response = json_util.dumps(vcambio)
    response_w = requests.post(webhook_url, data=response,headers={'Content-Type': 'application/json'})
    return Response(response, mimetype="application/json")

# OBTENER POR QUERY
@app.route('/vcambio_q/<q>', methods=['GET'])
def get_vcambio_q(q):
    vcambio = mongo.db.vcambio.aggregate([
    {
        "$search": {
        "text": {
            "query": q,
            "path": ["low","tipo","high","close","open","fecha","adjClose"]
                }
        }
    }
    ])
    response = json_util.dumps(vcambio)
    response_w = requests.post(webhook_url, data=response,headers={'Content-Type': 'application/json'})
    return Response(response, mimetype="application/json")



if __name__ == "__main__":
    app.run(debug=True)