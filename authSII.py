import requests
from xml.dom.minidom import *
import os
		
class authSII:

	def getSeed(self):			
		url="https://palena.sii.cl/DTEWS/CrSeed.jws?WSDL"
		headers = {'content-type':  'text/xml; charset=utf-8',
			     'Access-Control-Allow-Credentials':'true',	
		 	    'SOAPAction':'getSeed'		
		}

		body = """ 
			     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
			       <soapenv:Header/>
			       <soapenv:Body>
			       <getSeed></getSeed>
			      </soapenv:Body>
			      </soapenv:Envelope> """

		response = requests.post(url,data=body,headers=headers,verify=False)
		contenido = response.content
		print contenido
		salida = contenido.replace("&lt;", "<").replace("&quot;","\"").replace("&gt;",">")
		
		original = "<?xml version="+"\""+"1.0"+"\"" + " encoding="+"\""+ "UTF-8" + "\""+"?>"
		reemplazo = ""
		       
		salida = salida.replace(original,reemplazo) 

		return salida

	def getToken(self,objseed):

		

		xmlTree = xml.dom.minidom.parseString(objseed)
		valorsemilla = ""
		for element in xmlTree.getElementsByTagName("SEMILLA"):
		    valor1 =  element.firstChild.nodeValue
		    valorsemilla = valor1.lstrip('+-0') 
		doc=Document()
		gettoken = doc.createElement("getToken")
		item = doc.createElement("item")
		semilla = doc.createElement("Semilla")
		text = doc.createTextNode(valorsemilla)

		semilla.appendChild(text)
		item.appendChild(semilla)
		gettoken.appendChild(item)

		doc.appendChild(gettoken)

		contenido = doc.toprettyxml(indent="  ")


		sig = """<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
		<SignedInfo>
		<CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
		<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
		<Reference URI="">
		<Transforms>
		<Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
		</Transforms>
		<DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
		<DigestValue/>
		</Reference>
		</SignedInfo>
		<SignatureValue/>
		<KeyInfo>
		<KeyValue/>
		<X509Data>
		<X509Certificate/>
		</X509Data>
		</KeyInfo>
		</Signature>"""


		contenido = contenido.replace('</getToken>',sig+'</getToken>')
		#guardo el xml del documento
		f = open("gettoken.xml", "w")
		f.write(contenido)
		f.close()


		os.system("xmlsec1 --sign --privkey-pem key.pem,cert.pem --pwd 'amulen1956' gettoken.xml > gettokensigned.xml")

		f = open("gettokensigned.xml", "r")
		contenido = f.read()
		f.close()

		contenidoa = contenido.replace('<?xml version="1.0"?>','')

		url="https://palena.sii.cl/DTEWS/GetTokenFromSeed.jws?WSDL"
		headers = {'content-type':  'text/xml; charset=utf-8',
			     'Access-Control-Allow-Credentials':'true',	
		 	    'SOAPAction':'getToken'		
		}




		body = """ 
			     <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
			       <soapenv:Header/>
			       <soapenv:Body>
			       <getToken>
				<pszXml>	
				 """

		body = body+"<![CDATA["+'\n'+contenidoa+"]]></pszXml></getToken></soapenv:Body></soapenv:Envelope>"	

		response = requests.post(url,data=body,headers=headers,verify=False)
		respuesta = response.content


		salida = respuesta.replace("&lt;", "<").replace("&quot;","\"").replace("&gt;",">");
		
		original = "<?xml version="+"\""+"1.0"+"\"" + " encoding="+"\""+ "UTF-8" + "\""+"?>"
		reemplazo = ""
		       
		salida = salida.replace(original,reemplazo); 
		
		xmlTree = xml.dom.minidom.parseString(salida)
		valortoken = ""
		for element in xmlTree.getElementsByTagName("TOKEN"):
		    valortoken =  element.firstChild.nodeValue

		return valortoken
