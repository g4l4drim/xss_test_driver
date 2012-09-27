# -*- coding: utf-8 -*-
import hashlib
import json
import re
import urllib2
import base64

#Removed cookie payload due to security sandboxing of webkit / chrome etc...
#document.cookie='%(vnum)s-%(cnum)s-%(encnum)s=pass;%(domain)s;path=/';
payload="""window.location="/%(vnum)s/%(cnum)s/%(encnum)s/pass";
xhr=new XMLHttpRequest();
xhr.open("GET", "%(base)stest/%(vnum)s/%(cnum)s/%(encnum)s/xhrpass",false);
document.write("<"+"img src=%(base)stest/%(vnum)s/%(cnum)s/%(encnum)s/imgpass"+">"+"pass"+"<"+"/img"+">");"""

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }
def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def hashstr(string):
    md5=hashlib.md5()
    md5.update(string)
    return md5.hexdigest()
#todo: refactor test vector / xss vector generation and ressources management (ie:external files included)
def build_vector(vector,vector_payload,context,context_id=0,encoding_id=0,baseurl=""):
    """output the vector for the session with the given payload"""
    #if self.verbose:
        #print("building vector n°"+str(vector_n))
    vector_params={'payload':vector_payload,
                   'jscript':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.js",
                   'eval_payload':eval_payload(vector_payload),
                   'scriptlet':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.html",
                   'css':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.css",
                   'jpg':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.jpg",
                   'htc':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.htc",
                   'xbl':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.xbl",
                   'svg':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.svg",
                   'svg2':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.svg2",
                   'svg3':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.svg3",
                   'svg4':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.svg4",
                   'xxe':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.xxe",
                   'dtd':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.dtd",
                   'evt':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.evt",
                   'vml':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.vml",
                   'sct':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.sct",
                   'event':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.php",
                   'xdr':baseurl+"/"+context+"/inc/"+str(vector.id)+"/"+str(context_id)+"/"+str(encoding_id)+"/payload.xdr",
                   'base64':b64_payload(vector_payload),
                   'b64':b64_payload(vector_payload),
                   'b64uri':b64_uri_payload(vector_payload)
                   }
    #TODO: xhtml encoded output : http://html5sec.org/#18
    #TODO: Add swf payload include
    return str(vector.vector) % vector_params

def eval_payload(payload):
    """output an eval() function containing the encoded payload"""
    str_eval="eval(String.fromCharCode("
    for c in payload:
        str_eval+="%(c)d," % {'c':ord(c),}
    str_eval += "32))"
    return str_eval

def b64_uri_payload(payload):
    b64uri=b64_payload(payload).replace("=","%%3D")
    return b64uri

def b64_payload(payload):
    """base 64 encoded payload"""
    #TODO : code the function !!!
    # b64encode(string) -> Fonction pour encoder en b64
    b64=base64.encodestring("<script>"+payload+"</script>")
    return b64

def xss_payload():
    """output a alert() popup payload displaying XSS"""
    return """alert('xss')"""

def test_payload(vnum,cnum,encnum,baseurl="",domain=""):
    """output the javascript payload for a given test case instance
        the given payload will generata a request to the validation url
        Returns string"""
    #context : is it a test context or a manual showcase eg:alert("xss")
    payload_params={
                    'vnum':vnum,
                    'cnum':cnum,
                    'encnum':encnum,
                    'base':baseurl,
                    'domain':domain
                    }
    return payload % payload_params

def shazzer_to_vectors(url):
    req=urllib2.Request(url)
    opener = urllib2.build_opener()
    f = opener.open(req)
    export=json.load(f)
    vectors=[]
    for svect in export:
        vectorstr=svect["vector"]
        p=re.compile("%([0-9A-Fa-f][0-9A-Fa-f])")
        vectorstr=p.sub("\\x\g<1>",vectorstr)
        p=re.compile("alert\(.*\)")
        vectorstr=p.sub("%(eval_payload)s",vectorstr)
        p=re.compile("log\(.*\)")
        vectorstr=p.sub("%(eval_payload)s",vectorstr)
        p=re.compile("customLog\(.*\)")
        vectorstr=p.sub("%(eval_payload)s",vectorstr)
        vectorstr=vectorstr.replace("%","%%")
        datatypes={"num":"num","chr":"chr","hex2":"hex2","hex4":"hex4","hex6":"hex6",
                   "uni":"uni","urlenc":"urlenc","raw1":"raw1","raw2":"raw2","raw3":"raw3",
                   "datacsspropertynames":"text",
                   "datadhtmlprops":"text",
                   "dataevents":"text","datahtmlattributes":"text","datahtmlelements":"text",
                   "dataints":"text","datajscsspropertynames":"text","datajsproperties":"text",
                   "dataprotocols":"text"}
        for ts in datatypes:
            vectorstr=vectorstr.replace("*"+ts+"*","%("+datatypes[ts]+")s")
        vectorstr=vectorstr % svect
        vectors.append(vectorstr)
    #removing duplicates :
    vectors=list(set(vectors))
    return vectors

def shazzer_vector_desc(shazzer_vector_id):
    req=urllib2.Request("http://shazzer.co.uk/json?action=vectorList")
    opener = urllib2.build_opener()
    f = opener.open(req)
    export=json.load(f)
    def f(x): return x["id"]==shazzer_vector_id
    shazzer_vector=filter(f,export)
    return shazzer_vector[0]

def shazzer_link(shazzer_vector):
    string_id=shazzer_vector["description"]
    string_id=string_id.replace(" ","-")
    return string_id
    





