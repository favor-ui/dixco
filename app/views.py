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
                        'account_number':r['Account Number'],
                        'account_type':r['Account Type'],
                        'transaction_val':r['Transaction Value'],
                        'transaction_ref':r['Transaction Reference'],
                        'token':r['Token']
                        })
        
        return jsonify({'result' : output})
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})


@app.route('/disco_transaction/search', methods = ['GET'])
# @jwt_required
def get_one_disco_tran(transaction_type, token):
    """To get one item from the database.its a Get request and We use the databasename.find_one"""
    try:
        transactions = mongo.db.transactions_
    
        r = transactions.find_one({'transaction_type': transaction_type})

        if r:
            output = []
            output.append({
                        'account_number':r['Account Number'],
                        'account_type':r['Accout Type'],
                        'transaction_val':r['Transaction Value'],
                        'transaction_ref':r['Transaction Reference'],
                        'token':r['Token]'
                        ]})
        else:
            r = transactions.find_one({'token': token})

            output = []

            output.append({
                        'account_number':r['Account Number'],
                        'account_type':r['Accout Type'],
                        'transaction_val':r['Transaction Value'],
                        'transaction_ref':r['Transaction Reference'],
                        'token':r['Token]'
                        ]})
                            
        return jsonify({'result' : output})
    
    except Exception:
        return jsonify({"Message":"Something went wrong Please check"})


@app.route('/disco_attendees', methods = ['POST'])
# @jwt_required
def register():
    """To add an item to the database. its a post request and we use databasename.insert()"""
    try:
        transactions = mongo.db.transactions_
        account_number = request.json['Account Number']
        if not account_number:
            return jsonify({"Error":"Field can not be blank", "status":0})
        account_type = request.json['Accout Type']
        if not account_type:
            return jsonify({"Error":"Field can not be blank", "status":0})
        transaction_val = request.json['Transaction Value']
        if not transaction_val:
            return jsonify({"Error":"Field can not be blank", "status":0})
        transaction_ref = request.json['Transaction Reference']
        if not transaction_ref:
            return jsonify({"Error":"Field can not be blank", "status":0})
        token = request.json['Token']
        if not token:
            return jsonify({"Error":"Field can not be blank", "status":0})


        r = [{'account_name':'Account Name',
                        'account_number':'Account Number',
                        'account_type':'Accout Type',
                        'transaction_val':'Transaction Value',
                        'transaction_ref':'Transaction Reference',
                        'token':'Token'}]
        
        reg_id = transactions.insert_many({r})
                        
        r = transactions.find_one({'_id':reg_id})
            
        output = ({
                    'account_number':r['Account Number'],
                    'account_type':r['Accout Type'],
                    'transaction_val':r['Transaction Value'],
                    'transaction_ref':r['Transaction Reference'],
                    'token':r['Token'] 
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






