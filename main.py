from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from bson import ObjectId
import json

app=FastAPI()
ds={}
def details(collectionName):
    username = data['user']
    password = data['pass']
    clusterId= data['clusterId']
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password)
    uri=f"mongodb+srv://{encoded_username}:{encoded_password}@{clusterId}.mongodb.net/"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['student']
    collection = db[collectionName]
    return collection

data=None
count=99
def loadData():
    global data
    global count
    with open('config.json','r')as file:
        data=json.load(file)
    collection=details("rollInfo")
    cursor = collection.find({})
    mx=99
    for doc in cursor:
        ds[doc['roll']]=doc['obj']
        if mx<doc['roll']:mx=doc['roll']
    count=mx+1


loadData()







def addStudent(student):
    collection=details("studentInfo")
    result = collection.insert_one(student)
    return str(result.inserted_id)

@app.post("/students",status_code=201)
def create_student(student: dict):
    global count
    result = addStudent(student)
    ds[count]=result
    roll_no=count
    rollCollection=details("rollInfo")
    rollCollection.insert_one({'roll':roll_no,'obj':result})
    count=count+1
    return {'id' : roll_no}

@app.get("/students",status_code=200)
def get_data(rollNo: int = 0,country: str="",age: int=-1):
    collection=details("studentInfo")
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
    global count
    collection=details("studentInfo")
    result = collection.delete_many({})

    collection=details("rollInfo")
    collection.delete_many({})
    count = 100
    return {"message": f"Deleted {result.deleted_count} documents"}

@app.delete("/students/{student_id}", status_code = 200)
def delete_data(student_id : int):
    collection=details("studentInfo")
    roll_no = ds[student_id]
    result = collection.delete_one({"_id":ObjectId(roll_no)})
    collection=details("rollInfo")
    collection.delete_one({"roll":student_id})
    return {"message": f"Deleted {result.deleted_count} documents"}

@app.patch("/students/{student_id}",status_code=204)
def update_data( student_id : int ,updated_data : dict):
    collection=details("studentInfo")
    obj_id=ds[student_id]
    collection.update_one({"_id": ObjectId(obj_id)}, {"$set": updated_data['updated_data']})
