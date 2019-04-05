from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps
import os
import csv
import pandas as pd
import sys, getopt, pprint

app = Flask(__name__)
cf_port = os.getenv("PORT")

#MONGODB_HOST = '127.0.0.1'
#MONGODB_PORT = 27017
DBS_NAME = 'U2VrgicbP4a2Td7B'
COLLECTION_NAME = 'projects'
FIELDS = {'school_state': True, 'resource_type': True, 'poverty_level': True, 'date_posted': True, 'total_donations': True, '_id': False}

# START - subprogram insert data to DB
#insert data from file.csv to MongoDB

client = MongoClient("mongodb://G3lbKo__UExZrtBo:l1H2egzQff_BEbG1@10.11.241.39:47481/U2VrgicbP4a2Td7B") #host uri
db = client.U2VrgicbP4a2Td7B     #Select the database

csvfile = open('donors.csv', 'r')
reader = csv.DictReader( csvfile )
db.projects.drop()
header= [ "_projectid","_teacher_acctid","_schoolid","school_ncesid","school_latitude","school_longitude","school_city","school_state","school_zip","school_metro","school_district","school_county","school_charter","school_magnet","school_year_round","school_nlns","school_kipp","school_charter_ready_promise","teacher_prefix","teacher_teach_for_america","teacher_ny_teaching_fellow","primary_focus_subject","primary_focus_area","secondary_focus_subject","secondary_focus_area","resource_type","poverty_level","grade_level","vendor_shipping_charges","sales_tax","payment_processing_charges","fulfillment_labor_materials","total_price_excluding_optional_support","total_price_including_optional_support","students_reached","total_donations","num_donors","eligible_double_your_impact_match","eligible_almost_home_match","funding_status","date_posted","date_completed","date_thank_you_packet_mailed","date_expiration" ]

for each in reader:
    row={}
    for field in header:
        row[field]=each[field]

    db.projects.insert(row)
# END - subprogram insert data to DB

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/donorschoose/projects")
def donorschoose_projects():
    connection = MongoClient("mongodb://G3lbKo__UExZrtBo:l1H2egzQff_BEbG1@10.11.241.39:47481/U2VrgicbP4a2Td7B")
    collection = connection[DBS_NAME][COLLECTION_NAME]
    projects = collection.find(projection=FIELDS, limit=10000)
    #projects = collection.find(projection=FIELDS)
    json_projects = []
    for project in projects:
        json_projects.append(project)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

if __name__ == '__main__':
   if cf_port is None:
       app.run(host='0.0.0.0', port=5000, debug=True)
   else:
       app.run(host='0.0.0.0', port=int(cf_port), debug=True) 
    
