#!/usr/bin/python
#-*- coding: UTF-8 -*-

from xml.dom.minidom import *

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64


class timbre:
	
	def creaTimbre(self,contenido):
		xmlTree = parseString(contenido)

		#get all departments
		nrolinea = 0
		item1 = ""
		for node1 in xmlTree.getElementsByTagName("DscItem") :
		    for node2 in node1.childNodes:
			if(node2.nodeType == Node.TEXT_NODE) :
			    if(nrolinea==0):
			       item1 = node2.data  	
			    nrolinea = nrolinea + 1 	


		documento = xmlTree.getElementsByTagName("Documento")[0]
		ted = xmlTree.createElement("TED")


		ted.setAttribute("version", "1.0")
		dd = xmlTree.createElement("DD")
		re = xmlTree.createElement("RE")

		rutemisor = ""
		for element in xmlTree.getElementsByTagName("RUTEmisor"):
		   rutemisor =  element.firstChild.nodeValue

		text = xmlTree.createTextNode(rutemisor)
		re.appendChild(text)
		dd.appendChild(re)



		tipodte = ""
		for element in xmlTree.getElementsByTagName("TipoDTE"):
		   tipodte =  element.firstChild.nodeValue

		td = xmlTree.createElement("TD")
		text = xmlTree.createTextNode(tipodte)
		td.appendChild(text)
		dd.appendChild(td)

		folio = ""
		for element in xmlTree.getElementsByTagName("Folio"):
		   folio =  element.firstChild.nodeValue

		f = xmlTree.createElement("F")
		text = xmlTree.createTextNode(folio)
		f.appendChild(text)
		dd.appendChild(f)

		"""<TED version="1.0">
		   <DD>
		    <RE>76040308-3</RE>
		    <TD>33</TD>
		    <F>669</F>
		    <FE>2019-05-16</FE>
		    <RR>77813960-K</RR>
		    <RSR>AMULEN CONSULTORES LTDA</RSR>
		    <MNT>543668</MNT>
		    <IT1>CAJON AFECTO</IT1>
		"""

		fchemis = ""
		for element in xmlTree.getElementsByTagName("FchEmis"):
		   fchemis =  element.firstChild.nodeValue

		text = xmlTree.createTextNode(fchemis)


		fe = xmlTree.createElement("FE")
		fe.appendChild(text)

		dd.appendChild(fe)


		rutrecep = ""
		for element in xmlTree.getElementsByTagName("RUTRecep"):
		   rutrecep =  element.firstChild.nodeValue

		text = xmlTree.createTextNode(rutrecep)
		rr = xmlTree.createElement("RR")
		rr.appendChild(text)
		dd.appendChild(rr)


		rznsocrecep  = ""
		for element in xmlTree.getElementsByTagName("RznSocRecep"):
		   rznsocrecep =  element.firstChild.nodeValue

		text = xmlTree.createTextNode(rznsocrecep)
		rsr = xmlTree.createElement("RSR")
		rsr.appendChild(text)
		dd.appendChild(rsr)



		mntotal  = ""
		for element in xmlTree.getElementsByTagName("MntTotal"):
		   mntotal =  element.firstChild.nodeValue
		text = xmlTree.createTextNode(mntotal)

		mnt = xmlTree.createElement("MNT")
		mnt.appendChild(text)
		dd.appendChild(mnt)

		it1 = xmlTree.createElement("IT1")
		text = xmlTree.createTextNode(item1)
		it1.appendChild(text)
		dd.appendChild(it1)


		#procedo a cargar el nodo caf
		caf = xml.dom.minidom.parse('/home/esteban/appdte/caf/F76040308T33.xml')
		nodecaf = caf.getElementsByTagName("CAF")[0]
		dd.appendChild(nodecaf)


		tsted = xmlTree.createElement("TSTED")

		import time
		fecha = time.strftime("%Y-%m-%d")
		hora = time.strftime("%X")
		text = xmlTree.createTextNode(fecha+"T"+hora)
		tsted.appendChild(text)
		dd.appendChild(tsted)

		ted.appendChild(dd)

		auxdd = dd.toxml()
		auxdd = auxdd.replace("\n","")
		#obtengo la clave rsa del caf y la guardo en unA variable
		clave = ""
		rsask = caf.getElementsByTagName("RSASK")

		for node1 in rsask:
		    for node2 in node1.childNodes:
			if(node2.nodeType == Node.TEXT_NODE) :
			   clave = node2.data		


		key = RSA.importKey(clave)
		message = auxdd.encode('iso-8859-1')

		h = SHA.new(message)
		p = PKCS1_v1_5.new(key)
		signature = p.sign(h)

		firma = base64.b64encode(signature)

		frmt = xmlTree.createElement("FRMT")
		frmt.setAttribute("algoritmo", "SHA1withRSA")
		text = xmlTree.createTextNode(firma)
		frmt.appendChild(text)
		ted.appendChild(frmt)
		documento.appendChild(ted)

		tmstfirma = xmlTree.createElement("TmstFirma")
		text = xmlTree.createTextNode(fecha+"T"+hora)
		tmstfirma.appendChild(text)
		documento.appendChild(tmstfirma)

		#guardo el xml del documento
		#archivo = open("dte.xml", "w")
		#  xmlTree.writexml(archivo)
		#archivo.close()
		contenido = xmlTree.toxml()
		return contenido
