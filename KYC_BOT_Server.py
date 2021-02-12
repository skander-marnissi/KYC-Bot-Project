from flask import Flask, request, render_template, send_from_directory,jsonify
import os
import base64
from KYC_BOT_Script import ImageRecognizer
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#Test route 
@app.route("/")
def main() :
	return "Your server is Running , WOoooHooooo ! "

#Script route
@app.route("/receive",methods=['POST','GET'])
def receive():
	
    #Retrieving Data from Json request
    
        data = request.get_json()
        selfie_name = data['selfie_name']
        selfie = data['selfie']
        front_cin_name = data['front_cin_name']
        front_cin = data['front_cin']
        back_cin = data['back_cin']
        back_cin_name = data['back_cin_name']

        #Utf-8 encode
        a = front_cin.encode('utf-8')
        b = selfie.encode('utf-8')
        c = back_cin.encode('utf-8')
        
        #Testing
        print("______________________________________________________________________________")
        print("Testing received json Data : ",selfie_name)
        print("Testing received json Data : ",front_cin_name)
        print("Testing received json Data : ",back_cin_name)
        
        
        #Decode the Base64 encoded Front_ID picture
        with open("images/"+front_cin_name, "wb") as h:
            h.write(base64.decodebytes(a))

        #Decode the Base64 encoded Selfie picture
        with open("images/"+selfie_name, "wb") as h :
            h.write(base64.decodebytes(b))     

        #Decode the Base64 encoded Back_ID picture
        with open("images/"+back_cin_name, "wb") as h :
            h.write(base64.decodebytes(c))          

        
                            #Starting the verifications
 ######################################################################################

        obj = ImageRecognizer("images/"+front_cin_name,"images/"+back_cin_name,"images/"+selfie_name)

        response=json.loads(obj.kyc_web_service())

        print(response)

        return jsonify(response)
               
######################################################################################

# Server Config(optionnal parameters :host = 'your ip address',threaded=True)
if __name__ == "__main__":
    app.run(debug = True)	




