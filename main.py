# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi import Response
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from urllib.parse import quote_plus
# from bson.objectid import ObjectId


# app=FastAPI()

# ds={}
# rollNo=100

# def addStudent(student):
#     username = "tanishqrawat8"
#     password = "Tanu@091710"

#     global rollNo
#     encoded_username = quote_plus(username)
#     encoded_password = quote_plus(password)


#     uri=f"mongodb+srv://{encoded_username}:{encoded_password}@tanishq.5tbek3n.mongodb.net/"


#     client = MongoClient(uri, server_api=ServerApi('1'))

#     db = client['student']

#     collection = db['studentInfo']
#     result = collection.insert_one(student)
#     obj_id =str(result.inserted_id)
#     ds[rollNo]=obj_id
#     ans={'id':rollNo}
#     rollNo+=1
#     return ans



# # Define a route with a POST method to save student data
# # @app.post("/students/",status_code=201)
# # def create_student(student: dict):
# #     print(student)
# #     print(type(student))
# #     result = addStudent(student)
# #     return {'id':result}




# @app.get("/students", status_code=200)
# def get_student_list():
#     return []



from fastapi import FastAPI

app = FastAPI()

# POST method route for creating a new student
@app.post("/students", status_code=201)
def create_student():
    # Add logic here to create a new student
    return {"message": "Student created successfully"}

# GET method route for retrieving a list of students
@app.get("/students", status_code=200)
def get_student_list():
    # Add logic here to retrieve a list of students
    return {"message": "List of students retrieved successfully"}

# PUT method route for updating a student
@app.put("/students", status_code=200)
def update_student():
    # Add logic here to update a student
    return {"message": "Student updated successfully"}
