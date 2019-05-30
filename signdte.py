

class signDTE:

	def signDTE(self,contenido):	
		sig = """<Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
		<SignedInfo>
		<CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
		<SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
		<Reference URI="#DOC33">
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



		#f = open("dte.xml", "r")
		#contenido = f.read()
		#f.close()
		contenido = contenido.replace('</Documento>','</Documento>'+'\n'+sig)
		f = open("dte.xml", "w")
		f.write(contenido)
		f.close()
		
		import os
		os.system("xmlsec1 --sign --pwd 'amulen1956' --privkey-pem key.pem,cert.pem --id-attr:ID Documento dte.xml > dtefirmado.xml")

		f = open("dtefirmado.xml", "r")
		contenido = f.read()
		f.close()
		return contenido
