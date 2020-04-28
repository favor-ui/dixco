from flask import jsonify, request, abort
from app import app, mongo, cur_time_and_date



@app.route('/')
def home():
    try:
        return jsonify(
            {
                "Message":"Welcome",
                "status":1
                }
                )
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})


@app.route('/disco_transaction', methods = ['GET'])
# @jwt_required
def get_all_transactions():
    """To get one item from the database.its a Get request and We use the databasename.find_one"""
    try:
        transactions = mongo.db.transactions_
        
        output = []

        for r in transactions.find():
            output.append({
                        'Account Number':r['account_number'],
                        'Account Type':r['account_type'],
                        'Transaction Value':r['transaction_value'],
                        'Transaction Ref':r['transaction_ref'],
                        'Token':r['token'
                        ]})
        
        return jsonify({'result' : output})
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})


@app.route('/disco_transaction/search', methods = ['GET'])
# @jwt_required
def get_one_disco_tran():
    """To get one item from the database.its a Get request and We use the databasename.find_one"""
    try:
        transactions = mongo.db.transactions_
        request_data = request.get_json()
        name1 = request_data['name']
        name2 = "_".join(name1.split())
        name = name2.lower()
    
        r = transactions.find_one({'transaction_value': name})

        if r:
            output = []
            output.append({
                        'Account Number':r['account_number'],
                        'Account Type':r['account_type'],
                        'Transaction Value':r['transaction_value'],
                        'Transaction Ref':r['transaction_ref'],
                        'Token':r['token']
                        })
        else:
            r = transactions.find_one({'token': name})

            output = []

            output.append({
                    'Account Number':r['account_number'],
                    'Account Type':r['account_type'],
                    'Transaction Value':r['transaction_value'],
                    'Transaction Ref':r['transaction_ref'],
                    'Token':r['token']
                        })
                            
        return jsonify({'result' : output})
    
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})


@app.route('/disco_transaction', methods = ['POST'])
# @jwt_required
def register():
    """To add an item to the database. its a post request and we use databasename.insert()"""
    try:
        transactions = mongo.db.transactions_
        
        account_number1 = request.json['account_number']
        account_number= int(account_number1)
        if not account_number:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        account_type1 = request.json['account_type']
        account_type = str(account_type1)
        if not account_type:
            return jsonify({"Error":"Field can not be blank", "status":0})
       
        transaction_val1 = request.json['transaction_value']
        transaction_val = int(transaction_val1)
        if not transaction_val:
            return jsonify({"Error":"Field can not be blank", "status":0})
       
        transaction_ref1 = request.json['transaction_ref']
        transaction_ref = str(transaction_ref)
        if not transaction_ref:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        token1 = request.json['token']
        token = str(token1)
        if not token:
            return jsonify({"Error":"Field can not be blank", "status":0})
        
        reg_id = transactions.insert_one({'Account Number':'account_number',
                                    'Account Type':'account_type',
                                    'Transaction Value':'transaction_value',
                                    'Transaction Ref':'transaction_ref',
                                    'Token':'token'})


        r = transactions.find_one({'_id':reg_id})
            
        output = ({
                    'Account Number':'account_number',
                    'Account Type':'account_type',
                    'Transaction Value':'transaction_value',
                    'Transaction Ref':'transaction_ref',
                    'Token':'token' 
                    })
        
        return jsonify({'result' : output})
   
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})
   



@app.errorhandler(400)
def bad_request__error(exception):
    return jsonify(
        {
            "Message": "Sorry you entered wrong values kindly check and resend!"
        },
        {
            "status":400
        }
    )


@app.errorhandler(401)
def internal_error(error):
    return jsonify(
        {
            "Message": "Acess denied ! please register and login to generate API KEY"
        },
        {
            "status": 401
        }
    )



@app.errorhandler(404)
def not_found_error(error):
    return jsonify(
        {
            "Message":"Sorry the page your are looking for is not here kindly go back"
        },
        {
            "status": 404
        }
    )





@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Sorry the requested method is not allowed kindly check and resend !"
        },
        {
            "status": 405
        }
    )

@app.errorhandler(500)
def method_not_allowed(error):
    return jsonify(
        {
            "Message": "Bad request please check your input and resend !"
        },
        {
            "status": 500
        }
    )





