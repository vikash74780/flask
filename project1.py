from flask import Flask
import jwt
from flask import request
import json
import csv
import time

app=Flask(__name__)
@app.route('/register',methods=['POST'])
def register():
    email=request.json['email']
    password=request.json['password']
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)
    flag = False

    for row in csv_reader:
        if row['email'] == email:
            if row['password'] == password:
                flag = True
                break
    if(flag):
        return json.dumps({'message':'Already register'})
    else:
        return json.dumps({"message":"user register"})

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    flag = False
    for row in csv_reader:
        if row['email'] == email:
            if row['password'] == password:
                flag = True
                break

    if flag:
        payload={'email':email,"password":password,'message':'Login successful','expire': time.time()+3600}
        key='secret'
        encode_jwt=jwt.encode(payload,key)
        return {'auth_token':encode_jwt.decode(),'message': 'Login successful'}
    else:
        return {'message':'email or password incorrect'}

@app.route('/modify/<user_id>',methods=['PATCH'])
def modify(user_id):
    auth_token = request.json['auth_token']
    email = request.json['email']
    password = request.json['password']
    key = 'secret'
    data = jwt.decode(auth_token, key)
    if data['expire'] >= time.time() and data['email']==email:
        f_hand = open('data/users.csv', 'r')
        csv_reader = csv.DictReader(f_hand)
        details=[]
        for i in csv_reader:
            details.append(i)
        f_hand.close()
        flag = False
        for row in details:
            if row['id'] == user_id:
                    flag = True
                    break

        if flag:
            f_hand=open('data/users.csv','w')
            headers=details[0].keys()
            csv_writer=csv.DictWriter(f_hand,fieldnames=headers,lineterminator='\n')
            csv_writer.writeheader()
            for row in details:
                if(row['id']==user_id):
                    row['password']=password
                csv_writer.writerow(row)
            f_hand.close()
            return json.dumps({'data':data,'message': 'user modified'})
        else:
            return json.dumps({'mesage':'NOT MODIFY'})


@app.route('/delete/<user_id>',methods=['DELETE'])
def delete(user_id):
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)
    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    f_hand=open('data/users.csv','w')
    headers=details[0].keys()
    csv_writer=csv.DictWriter(f_hand,fieldnames=headers,lineterminator="\n")
    csv_writer.writeheader()
    for row in details:
        if row['id'] != user_id:
            csv_writer.writerow(row)
        else:
            continue
    f_hand.close()
    return json.dumps({'message':'deleted'})

@app.route('/show',methods=['GET'])
def show():    
    f_hand=open('data/user.csv','r')
    csv_reader=csv.DictReader(f_hand)
    details=list(csv_reader)
    f_hand.close()
    return json.dumps({'users':details})

#***********************************************

@app.route('/movie/create/<user_id>',methods=['POST'])
def create(user_id):
    email=request.json['email']
    password=request.json['password']
    movie_id= request.json['id']
    movie_name=request.json['movie_name']
    year=request.json['year']
    duration= request.json['duration']

    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    flag = False
    for row in details:
        if row['email'] == email:
            if row['password'] == password:
                flag = True
                break

    if flag:
        payload={'email':email,'message':'login'}
        key='secret'
        encode_jwt=jwt.encode(payload,key)

        for line in details:
            if(line['id']==user_id):

                hand = open('data/movies.csv', 'r')
                csv_reader = csv.DictReader(hand)
                details=[]
                for i in csv_reader:
                    details.append(i)
                #headers=details[0].keys()
                hand.close
                hand=open('data/movies.csv','a')
                headers=details[0].keys()
                csv_writer=csv.DictWriter(hand,fieldnames=headers,lineterminator="\n")
                #csv_writer.writeheader()
                csv_writer.writerow({'id':movie_id,'movie_name':movie_name,'year':year,'duration':duration,'user_id':user_id}) 
                hand.close()
                break
        
        return json.dumps({'auth_token':encode_jwt.decode(),'message': 'movies created'})
    else:
        return {'message': 'email or password incorrect'}      


@app.route('/movie/details/<user_id>',methods=['POST'])
def moviedetails(user_id):
    email=request.json['email']
    password=request.json['password']
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    
    flag = False
    for row in details:
        if row['email'] == email:
            if row['password'] == password:
                flag = True
                break
    if flag:
        payload={'email':email,'message':'login'}
        key='secret'
        encode_jwt=jwt.encode(payload,key)
        f_hand=open('data/movies.csv','r')
        csv_reader=csv.DictReader(f_hand)
        details=list(csv_reader)
        d=[]
        for i in details:
            if(i['user_id']==user_id):
                d.append(i)

        f_hand.close()
        return json.dumps({'auth_token':encode_jwt.decode(),'movies':d})
    else:
        return {'message':'email or password incorrect'}

@app.route('/movie/search/<movie_name>',methods=['POST'])
def search(movie_name):
    email=request.json['email']
    password=request.json['password']
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    
    flag = False
    for row in details:
        if row['email'] == email:
            if row['password'] == password:
                flag = True
                break   
    if flag:
        payload={'email':email,'message':'login'}
        key='secret'
        encode_jwt=jwt.encode(payload,key)
        f_hand=open('data/movies.csv','r')
        csv_reader=csv.DictReader(f_hand)
        moviedata=list(csv_reader)
        f_hand.close()
        for i in range(len(moviedata)):
            if(moviedata[i]['movie_name']==movie_name):
                return json.dumps({'auth_token':encode_jwt.decode(),'searched movie':moviedata[i]})
                break    
        return json.dumps({'message':'invalid movie name'})
    else:
        return {'message':'email or password invalid'}
    

@app.route('/movie/delete/<user_id>',methods=['DELETE'])
def delete_movie(user_id):
    email=request.json['email']
    password=request.json['password']
    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    for line in details:
        if(line['email']==email and line['password']==password and line['id']==user_id):
            payload={'email':email,'message':'login'}
            key='secret'
            encode_jwt=jwt.encode(payload,key)
            f_hand= open('data/movies.csv', 'r')
            csv_reader = csv.DictReader(f_hand)
            details=[]
            for i in csv_reader:
                details.append(i)
            f_hand.close()
            f_hand=open('data/movies.csv','w')
            headers=details[0].keys()
            csv_writer=csv.DictWriter(f_hand,fieldnames=headers,lineterminator='\n')
            csv_writer.writeheader()
            for row in details:
                if row['user_id'] !=user_id:
                    csv_writer.writerow(row)
                else:
                    continue
            f_hand.close()
            return json.dumps({'auth_token':encode_jwt.decode(),'message':'movie deleted'})
            break
        
    return json.dumps({'message':'email doesnt not exits'})


@app.route('/movie/modify/<movie_id>',methods=['PATCH'])
def movie_modify(movie_id):
    email = request.json['email']
    password = request.json['password']
    movie_name=request.json['movie_name']
    year=request.json['year']
    duration=request.json['duration']
    auth_token=request.json['auth_token']

    f_hand = open('data/users.csv', 'r')
    csv_reader = csv.DictReader(f_hand)

    details=[]
    for row in csv_reader:
        details.append(row)
    f_hand.close()
    key = 'secret'
    data = jwt.decode(auth_token, key)
    if data['expire'] >= time.time() and data['email']==email and data['password']==password:
        f_hand = open('data/movies.csv', 'r')
        csv_reader = csv.DictReader(f_hand)
        detail=[]
        for i in csv_reader:
            detail.append(i)
        f_hand.close()
        flag = False
        for row in detail:
            if row['id'] == movie_id:
                flag = True
                break
        if flag:
            f_hand=open('data/movies.csv','w')
            headers=detail[0].keys()
            csv_writer=csv.DictWriter(f_hand,fieldnames=headers,lineterminator='\n')
            csv_writer.writeheader()
            for row in detail:
                if(row['id']==movie_id):
                    row['movie_name']=movie_name
                    row['year']=year
                    row['duration']=duration
                csv_writer.writerow(row)
            f_hand.close()
            return json.dumps({'data':data,'message': 'movie modified'})
        else:
            return json.dumps({'mesage':'not modify'})
    return json.dumps({'message':'user doesnt not exits'})
