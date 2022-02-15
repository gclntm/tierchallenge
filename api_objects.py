import boto3
from flask import Flask
from flask import jsonify
from flask import render_template 

# session = boto3.Session( 
#          aws_access_key_id='<your_access_key_id>', 
#          aws_secret_access_key='<your_secret_access_key>')

client = boto3.client('s3')

app = Flask(__name__)

@app.route('/v1/listobjects_json', methods=['GET'])
def listobjects():
    response = client.list_objects_v2(Bucket='tierchallenge')

    objects = []
    for obj in response['Contents']:
        #print(obj['Key'])
        objects.append(obj['Key'])
    return jsonify(objects)


@app.route('/v1/listobjects_html', methods=['GET'])
def listobjects_html():
    response = client.list_objects_v2(Bucket='tierchallenge')

    objects = []
    for obj in response['Contents']:
        #print(obj['Key'])
        objects.append(obj['Key'])
    return render_template('template.html',objects=objects)
