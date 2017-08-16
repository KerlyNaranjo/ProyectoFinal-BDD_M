# Curso BigData & Data Analytics by Handytec
# Fecha: Marzo-2016
# Descripcion: Programa que cosecha tweets desde la API de twitter usando tweepy

import couchdb #Libreria de CouchDB (requiere ser instalada primero)
from tweepy import Stream #tweepy es la libreria que trae tweets desde la API de Twitter (requiere ser instalada primero)
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json #Libreria para manejar archivos JSON


###Credenciales de la cuenta de Twitter########################
#Poner aqui las credenciales de su cuenta privada, caso contrario la API bloqueara esta cuenta de ejemplo
ckey = "w721sk5kmzyH7ZZfiSUfPjUDI"
csecret = "1UL5sNwITAXoSyKZh9izpAL19ALJUaPRWbkETlrBh8Q2jYWoEd"
atoken = "872556070471913473-Ffn3ytzbC8XTMXVESijhID1XUqGVNvh"
asecret = "jGvsPepDF00rbHi8gaPrQHMoTLkZJgkV7rbFyNgrgElDc"
#####################################

class listener(StreamListener):
    
    def on_data(self, data):
        dictTweet = json.loads(data)
        try:
            dictTweet["_id"] = str(dictTweet['id'])
            #Antes de guardar el documento puedes realizar parseo, limpieza y cierto analisis o filtrado de datos previo
            #a guardar en documento en la base de datos
            doc = db.save(dictTweet) #Aqui se guarda el tweet en la base de couchDB
            print ("Guardado " + "=> " + dictTweet["_id"])
        except:
            print ("Documento ya existe")
            pass
        return True
    
    def on_error(self, status):
        print (status)
        
auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())


#Setear la URL del servidor de couchDB
server = couchdb.Server('http://localhost:5984/')
try:
    #Si no existe la Base de datos la crea
    db = server.create('ecuador')
except:
    #Caso contrario solo conectarse a la base existente
    db = server['ecuador']
    
#Aqui se define el bounding box con los limites geograficos donde recolectar los tweets
twitterStream.filter(locations=[-79.4883,-4.622,-78.6269,-3.6652]) #Loja
twitterStream.filter(locations=[-78.4336,0.0623,-77.5722,0.6518]) #Ibarra
twitterStream.filter(locations=[-79.5652,-3.3087,-78.7038,-2.72]) #Cuenca
