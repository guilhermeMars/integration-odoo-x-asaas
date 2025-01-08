from flask import Flask, request, jsonify
import requests
import xmlrpc.client

app = Flask(__name__)

ODOO_URL = "https://ebramev-corporativo.odoo.com/"
ODOO_DB = "ebramev-corporativo"
ODOO_USERNAME = "marketing3@ebramev.com.br"
ODOO_PASSWORD = "4f2f61da00b82bf50bc98ecb89ce8df2cd9a67a8"

# Autenticação no Odoo
def odoo_authenticate():
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL))
    uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
    return uid

# Criação de uma cobrança no Odoo
def create_invoice_in_odoo(data):
    user_id = odoo_authenticate()
    models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(ODOO_URL))

    created_id = models.execute_kw(ODOO_DB, user_id, ODOO_PASSWORD, 'x_receitas', 'create', [{
        'x_name': data.get("customer"),
    }])

    return created_id

@app.route('/asaas/webhook', methods=['POST'])
def asaas_webhook():
    data = request.json
    if data and data.get("event") == "PAYMENT_CREATED":
        response = create_invoice_in_odoo(data)
        return jsonify(response)
    return jsonify({"status": "ignored"}), 200

if __name__ == '__main__':
    app.run(port=5000)