from flask import *
import os
app = Flask(__name__)

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
data = os.path.abspath(os.path.dirname(__file__)) + "/kunal-862dc-45065b50ed56.json"
cred = credentials.Certificate(data)
firebase_admin.initialize_app(cred)
fb = firestore.client()



@app.route('/',methods=["POST","GET"])
def landing():
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


    return(render_template("landingpage.html",regular_cookies_dict=rcd,regular_cookies_length=rcdl))
@app.route('/products',methods=["POST","GET"])
def products():
    cookies_class = fb.collection('Cookies Class')
    cookies_class_stream = cookies_class.stream()
    cookies_types = []
    for k in cookies_class_stream:
        cookies_types = k.to_dict()['type']
    cookies_types.insert(0, 'All Products')
    print(cookies_types)
    all_products = {}
    for ct in cookies_types:
        l = fb.collection(ct)
        all_list = l.stream()
        all_products[ct] = {}
        for doc in all_list:
            all_products[ct][str(doc.id)] = []
            all_products[ct][str(doc.id)].append(u'{}'.format(doc.to_dict()['Image']))
            all_products[ct][str(doc.id)].append(u'{}'.format(doc.to_dict()['Name']))
            all_products[ct][str(doc.id)].append(u'{}'.format(doc.to_dict()['Weight']))
    print(all_products)
    return (render_template("products.html",all_products_dict=all_products,product_types=cookies_types,product_types_length=len(cookies_types)))
@app.route('/contactUs',methods=["POST","GET"])
def contactUs():
    return (render_template('contactUs.html'))
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
