from flask import Flask, request, abort, jsonify, redirect, request
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)

mydb_connector = mysql.connector



@app.route('/add-document', methods=['POST'])
def add_document():
    try:
        # get request data
        body = request.get_json()
        document_type = body.get('document_type')
        reciept = body.get('reciept')
        reciept_date = body.get('reciept_date',)
        status = body.get('status')
        user = body.get('user')
        content = body.get('content')
        
        #create db connection
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()

        #insert into document table
        document_insert_sql = f"insert into document (document_type,reciept,reciept_date,status) \
        values (%s,%s,%s,%s);"
        document_insert_val=(document_type,reciept,reciept_date,status)
        cur.execute(document_insert_sql,document_insert_val)
        mydb.commit()
        # output = cur.fetchall()
        document_id = cur.lastrowid

        #insert into draft table
        draft_insert_sql = f"insert into draft (content,user,document_id) \
        values (%s,%s,%s);"
        draft_insert_val=(content,user,document_id)
        cur.execute(draft_insert_sql,draft_insert_val)
        mydb.commit()
        draft_id = cur.lastrowid


        cur.close()
        # print(sql)
        return jsonify({
            'success': True,
            'document_id': document_id,
            'draft_id':draft_id

        }), 200
    except:
        abort(400)


if __name__ == '__main__':
    app.run()