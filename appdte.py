#!/usr/bin/python
#-*- coding: utf-8 -*-
from dte import *
from timbre import *
from signdte import *
from enviodte import *
from authSII import *
from upload import *
import json

                		
f  = open("DTEPRUEBA.json","r")
contenido = f.read()
f.close
print contenido


info = json.loads(contenido)
infoemisor = info['emisor']
rutemisor = infoemisor['rutemisor'] 
rutenvia = infoemisor['rutenvia']

infoiddoc = info['iddoc']

objDTE = dte()
#creo el archivo el archivo xml
documento = objDTE.creaDTE(contenido)

#añado la seccion de timbre
objtimbre = timbre()

#añado la seccion de firma del dte y firmo el documento
objfirma = signDTE()
documento = objtimbre.creaTimbre(documento)
documento = objfirma.signDTE(documento)

#creo el sobre electronico del documento electrónico
objEnvioDTE = envioDTE()
enviodte = objEnvioDTE.make_envio(documento,infoemisor,infoiddoc)

#preparo la secuencia de autentificacion
objauthSII = authSII()
objSeed = objauthSII.getSeed()
valortoken = objauthSII.getToken(objSeed)

#con el token obtenido inicio la secuencia de carga del documento e inicio el upload al SII
objupLoad =  uploadSII()
respuesta = objupLoad.uploadDTE(valortoken,rutemisor,rutenvia,"enviodtefirmado") 

#imprimo cadena xml que me devuelve un track id
print respuesta
