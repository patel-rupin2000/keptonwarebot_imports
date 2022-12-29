from flask import *
import os
app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# cred = credentials.Certificate("kunal-862dc-45065b50ed56.json")
data = os.path.abspath(os.path.dirname(__file__)) + "/kunal-862dc-45065b50ed56.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)
fb = firestore.client()
rc = fb.collection('Regular Cookies')
regular_cookies = rc.stream()
rcd = {}
rcdl = 0
for doc in regular_cookies:
    rcd[str(doc.id)] = []
    print(doc.id)
    rcd[str(doc.id)].append(u'{}'.format(doc.to_dict()['Image']))
    rcd[str(doc.id)].append(u'{}'.format(doc.to_dict()['Name']))
    rcd[str(doc.id)].append(u'{}'.format(doc.to_dict()['Weight']))
    rcdl += 1

print(rcd)
@app.route('/',methods=["POST","GET"])
def hello_world():


    return(render_template("landingpage.html",regular_cookies_dict=rcd,regular_cookies_length=rcdl))


if __name__ == '__main__':
    app.run()
