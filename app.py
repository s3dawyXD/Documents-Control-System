from flask import Flask, request, abort, jsonify, redirect, request
from flask_cors import CORS
import mysql.connector


app = Flask(__name__)
CORS(app)

mydb_connector = mysql.connector


def json_data(cursor):
    result_list = cursor.fetchall()
    fields_list = cursor.description
    if len(result_list) > 0:
        column_list = []
        for i in fields_list:
            column_list.append(i[0])
        jsonData_list = []
        for row in result_list:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            jsonData_list.append(data_dict)
        return jsonData_list
    else:
        return []


@app.route('/document', methods=['POST'])
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

        # create db connection
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                       password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()

        # insert into document table
        document_insert_sql = f"insert into document (document_type,reciept,reciept_date,status) \
        values (%s,%s,%s,%s);"
        document_insert_val = (document_type, reciept, reciept_date, status)
        cur.execute(document_insert_sql, document_insert_val)
        mydb.commit()
        document_id = cur.lastrowid

        # insert into draft table
        draft_insert_sql = f"insert into draft (content,user,document_id) \
        values (%s,%s,%s);"
        draft_insert_val = (content, user, document_id)
        cur.execute(draft_insert_sql, draft_insert_val)
        mydb.commit()
        draft_id = cur.lastrowid

        cur.close()
        return jsonify({
            'success': True,
            'document_id': document_id,
            'draft_id': draft_id

        }), 200
    except:
        abort(400)
    finally:
        mydb.close()


@app.route('/document', methods=['GET'])
def get_document():
    try:
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                       password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()
        document_get_sql = "select document.*,draft.draft_id,draft.content,draft.user from document \
        left join draft on document.document_id = draft.document_id order by draft.document_id,draft.draft_id;"
        cur.execute(document_get_sql)

        output = json_data(cur)

        cur.close()
        return jsonify({
            'success': True,
            'data': output
        }), 200
    except:
        abort(400)
    finally:
        mydb.close()


@app.route('/circulate', methods=['POST'])
def send_document():
    try:
        body = request.get_json()
        draft_id = body.get("draft_id")
        sender = body.get("from")
        recever = body.get("to")
        if draft_id == None or sender == None or recever == None:
            abort(400)
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                       password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()

        copy_insert_sql = f"insert into copies(`from`,`to`,draft_id) \
            values(%s,%s,%s);"
        copy_insert_val = (sender,recever,draft_id)
        cur.execute(copy_insert_sql, copy_insert_val)
        mydb.commit()
        copy_id = cur.lastrowid
        cur.close()
        return jsonify({
            'success': True,
            'copy_id': copy_id
        }), 200
    except:
        abort(400)
    

@app.route('/draft', methods=['POST'])
def edit_document():
    try:
        body = request.get_json()
        document_id = body.get("document_id")
        content = body.get("content")
        user = body.get("user")
        if document_id == None :
            abort(400)
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                       password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()

        draft_insert_sql = f"insert into draft (content,user,document_id) \
        values (%s,%s,%s);"
        draft_insert_val = (content, user, document_id)
        cur.execute(draft_insert_sql, draft_insert_val)
        mydb.commit()
        draft_id = cur.lastrowid

        cur.close()
        return jsonify({
            'success': True,
            'draft_id': draft_id
        }), 200
    except:
        abort(400)
    finally:
        mydb.close()

@app.route('/circulate', methods=['GET'])
def get_copies():
    try:
        mydb = mysql.connector.connect(host="127.0.0.1", user="root",
                                       password="123", port=3306, database="documents_control_system")
        cur = mydb.cursor()
        document_get_sql = "select document.*,draft.draft_id,draft.content,draft.user , \
        copies.copy_id,copies.from,copies.to from document \
        left join draft on document.document_id = draft.document_id inner join \
        copies on draft.draft_id = copies.draft_id\
        order by draft.document_id,draft.draft_id;"
        cur.execute(document_get_sql)

        output = json_data(cur)

        cur.close()
        return jsonify({
            'success': True,
            'data': output
        }), 200
    except:
        abort(400)
    finally:
        mydb.close()



if __name__ == '__main__':
    app.run(debug=True)
