# app.py - Faylka oo Dhammaystiran oo leh CRUD operations
from flask import Flask, jsonify, request, session, render_template, redirect, url_for, make_response
from flask_cors import CORS
import json
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default-secret-key-for-development')
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

PRODUCTS_FILE = 'products.json'

def read_products():
    """Function to read products from the JSON file."""
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_products(products):
    """Function to write products to the JSON file."""
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as file:
        json.dump(products, file, indent=2, ensure_ascii=False)

# ================== ROUTES-KA BIXINAYA BOGAGGA HTML ==================
@app.route('/')
def index_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/manage')
def manage_page():
    if 'logged_in' in session and session['logged_in']:
        # Waxaan abuuraynaa response object si aan ugu darno headers
        response = make_response(render_template('manage.html'))
        # Kuwan ayaa u sheegaya browser-ka inuusan keydin boggan
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return redirect(url_for('login_page'))

@app.route('/admin')
def admin_page():
    if 'logged_in' in session and session['logged_in']:
        # Sidoo kale halkan ku samee
        response = make_response(render_template('admin.html'))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    return redirect(url_for('login_page'))

# ================== ROUTES-KA API-GA EE AUTHENTICATION ==================
@app.route('/api/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Ka soo akhri magaca iyo password-ka environment variables
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['logged_in'] = True
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Magaca ama password-ku waa qalad"})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/check-auth')
def check_auth():
    if 'logged_in' in session and session['logged_in']:
        return jsonify({"authenticated": True})
    return jsonify({"authenticated": False})

# ================== ROUTES-KA API-GA EE BADEECOOYINKA (PRODUCTS) ==================

@app.route('/api/products')
def get_products():
    products = read_products()
    include_featured = request.args.get('include_featured', 'false').lower() == 'true'
    if not include_featured:
        products = [p for p in products if not p.get("isFeatured")]
    
    limit = request.args.get('limit', type=int)
    if limit:
        sorted_products = sorted(products, key=lambda p: p.get('id', 0), reverse=True)
        return jsonify(sorted_products[:limit])
    else:
        return jsonify(products)

# ROUTE CUSUB: Helitaanka hal badeeco (GET single product)
@app.route('/api/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products = read_products()
    product = next((p for p in products if p.get('id') == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Badeecada lama helin"}), 404

# ROUTE CUSUB: Ku darista badeeco cusub (ADD new product)
@app.route('/api/add-products', methods=['POST'])
def add_product():
    if not session.get('logged_in'):
        return jsonify({"error": "Login ayaa loo baahan yahay"}), 401
    
    data = request.get_json()
    products = read_products()
    
    new_id = max([p.get('id', 0) for p in products]) + 1 if products else 1
    data['id'] = new_id
    
    products.append(data)
    write_products(products)
    return jsonify({"success": True, "message": "Badeecada si guul leh ayaa loo diiwaan geliyay."})

# ROUTE CUSUB: Wax ka beddelka badeeco (UPDATE a product)
@app.route('/api/update-product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    if not session.get('logged_in'):
        return jsonify({"error": "Login ayaa loo baahan yahay"}), 401

    data = request.get_json()
    products = read_products()
    product_found = False
    for i, product in enumerate(products):
        if product.get('id') == product_id:
            products[i] = data
            products[i]['id'] = product_id # Hubi in ID-ga uusan isbeddelin
            product_found = True
            break
    
    if product_found:
        write_products(products)
        return jsonify({"success": True, "message": "Badeecada si guul leh ayaa loo cusbooneysiiyay."})
    return jsonify({"error": "Badeecada lama helin"}), 404

# ROUTE CUSUB: Tirtiridda badeeco (DELETE a product)
@app.route('/api/delete-product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    if not session.get('logged_in'):
        return jsonify({"error": "Login ayaa loo baahan yahay"}), 401
        
    products = read_products()
    original_length = len(products)
    products = [p for p in products if p.get('id') != product_id]
    
    if len(products) < original_length:
        write_products(products)
        return jsonify({"success": True, "message": "Badeecada si guul leh ayaa loo tirtiray."})
    return jsonify({"error": "Badeecada lama helin"}), 404

# ================== KICINTA SERVER-KA ==================
if __name__ == '__main__':
    app.run() # Iska daa sidan, Gunicorn ayaa la wareegi doona