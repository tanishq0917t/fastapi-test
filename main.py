from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from bson import ObjectId
import json

app=FastAPI()
data=None
def loadData():
    global data
    with open('config.json','r')as file:
        data=json.load(file)

loadData()
count=100
ds={}

def details():
    username = data['user']
    password = data['pass']
    clusterId= data['clusterId']
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)
    uri=f"mongodb+srv://{encoded_username}:{encoded_password}@{clusterId}.mongodb.net/"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['student']
    collection = db['studentInfo']
    return collection

def addStudent(student):
    collection=details()
    result = collection.insert_one(student)
    return str(result.inserted_id)

@app.post("/students",status_code=201)
def create_student(student: dict):
    global count
    result = addStudent(student)
    ds[count]=result
    roll_no=count
    count=count+1
    return {'id' : roll_no}

@app.get("/students",status_code=200)
def get_data(rollNo: int = 0,country: str="",age: int=-1):
    collection=details()
    if rollNo==0:
        if len(country)==0 and age==-1:
            cursor = collection.find({})
            all_data=[]
            for doc in cursor:
                all_data.append({"name":doc['name'],"age":doc["age"]})
            return all_data
        if len(country)>0 and age==-1:
            cursor = collection.find({"address.country":country})
            all_data=[{'name':doc['name'],'age':doc['age']} for doc in cursor]
            return all_data
        if len(country)==0 and age!=-1:
            cursor = collection.find({"age":{"$gte":age}})
            all_data=[{'name':doc['name'],'age':doc['age']} for doc in cursor]
            return all_data
        if len(country)>0 and age!=-1:
            cursor = collection.find({"age":{"$gte":age},"address.country":country})
            all_data=[{'name':doc['name'],'age':doc['age']} for doc in cursor]
            return all_data
    else:
        cursor = collection.find({"_id":ObjectId(ds[rollNo])})
        print(cursor)
        for doc in cursor:
            return {'name':doc['name'],'age':doc['age'],'address':doc['address']}

@app.delete("/students", status_code = 200)
def delete_data():
    collection=details()
    result = collection.delete_many({})
    return {"message": f"Deleted {result.deleted_count} documents"}

@app.delete("/students/{student_id}", status_code = 200)
def delete_data(student_id : int):
    collection=details()
    roll_no = ds[student_id]
    result = collection.delete_one({"_id":ObjectId(roll_no)})
    return {"message": f"Deleted {result.deleted_count} documents"}

@app.patch("/students/{student_id}",status_code=204)
def update_data( student_id : int ,updated_data : dict):
    collection=details()
    obj_id=ds[student_id]
    collection.update_one({"_id": ObjectId(obj_id)}, {"$set": updated_data['updated_data']})
