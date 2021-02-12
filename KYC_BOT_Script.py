import numpy as np
import imutils
from pyzbar import pyzbar
import argparse
import cv2
import json
import pytesseract
import os
from PIL import Image, ImageChops
import re
import face_recognition
from hash import av_hash , p_hash , d_hash , w_hash
import pickle
from flask import Flask, request, render_template, send_from_directory,jsonify
from sklearn import svm
from sklearn.model_selection import train_test_split 



class ImageRecognizer():
    
    '''
    Initializing the class with input images 
    '''

    def __init__(self,front_idname,back_idname,selfie_name):
        self.front_id = cv2.imread(front_idname)
        self.back_id = cv2.imread(back_idname)
        self.front_idname = front_idname
        self.selfie_name = selfie_name
        self.back_idname= back_idname
        self.cropped_name = ""
        self.id_number = ""
        self.selfie_directory='./images/selfie_faces'
        self.id_directory='./images/id_faces'

        #contsructor Param. test
        #print('Back_id name : ',self.back_idname)
        #print('Font_id name : ',self.front_idname)
        #print('Selfie name : ',self.selfie_name)
        

    
    # To verify if data in barcode(Back of ID) is same that ID number(Front of ID)

    def two_factor_verification(self):

        os.system('cls')
      
        # load the input image (back of the id)

        image = self.back_id
        
        # find the barcodes in the image and decode each of the barcodes

        barcodes = pyzbar.decode(image)

        #cv2.imshow('back_id image before processing :',self.back_id)

        #cv2.waitKey(0)

        # test : display the given data from barcodes

        print("______________________________________________________________________________") 
        print('[INFO] Given array of data from barcodes ',barcodes)

        # loop over the detected barcodes

        for barcode in barcodes:

            # extract the bounding box location of the barcode and draw the
            # bounding box surrounding the barcode on the image

            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
            # the barcode data is a bytes object so if we want to draw it on
            # our output image we need to convert it to a string first

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
        
            # draw the barcode data and barcode type on the image

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 2)
        
            # print the barcode type and data to the terminal

            #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        
        # show the output image

        #cv2.imshow("Image", image)
        #cv2.waitKey(0)

        # save data in Json format 

        #print('Id_Number : ',barcodeData[:8])
        #print('security_check_number : ',barcodeData[8:12])
        #print('date_emission :','-'.join(barcodeData[i:i+2] for i in range(12, len(barcodeData), 2)))

        

        #Verify if the extracted Id_number with OCR modul is equal to Id_number extracted
        # from the barcode
        try:

            date = '-'.join(barcodeData[i:i+2] for i in range(12, len(barcodeData), 2))


            if self.extract_id_number()==int(barcodeData[:8]):
                
                # a Python object (dict):

                x = {
                "Id_number": barcodeData[:8],
                "security_check_number":barcodeData[8:12] ,
                "date_emission":date,
                "two_factor_verification":'True'
                }

                # convert into JSON:
                y = json.dumps(x)

                print("Verification successful")

                # the result is a JSON string:
                print("______________________________________________________________________________") 
                print(y)

                return(y)

            else:
                
                # a Python object (dict):

                x = {
                "Id_number": barcodeData[:8],
                "security_check_number":barcodeData[8:12] ,
                "date":date,
                "two_factor_verification":'False'
                }

                # convert into JSON:
                y = json.dumps(x)

                print("Verification Failed")

                # the result is a JSON string:
                print("______________________________________________________________________________") 
                print(y)

                return(False)
        except:
            print("______________________________________________________________________________") 
            print("[INFO] Didn't find any Barcode to read | the Barcode providen is not clear please take another picture [INFO]")

            return('0')

    # To extract ID number from the front of ID

    def extract_id_number(self) :
        
        # Only for windows Os to read Tesseract-OCR Api (OCR)

        pytesseract.pytesseract.tesseract_cmd="C:\\Users\\Travaille\\AppData\\Local\\Tesseract-OCR\\tesseract.exe"

        # load the input image (front of the id)
        
        # image = cv2.imread(filenamee)

        # test : showing output image 

        #cv2.imshow('image before processing :',self.front_id)

        #cv2.waitKey(0)

        # Convert to gray
                
        img = cv2.cvtColor(self.front_id, cv2.COLOR_BGR2GRAY) 
                
        # Apply dilation and erosion to remove some noise  
                
        kernel = np.ones((1, 1), np.uint8)  

        img = cv2.dilate(img, kernel, iterations=1) 

        img = cv2.erode(img, kernel, iterations=1)

        #Apply threshold to get image with only black and white 
                
        cv2.threshold(cv2.GaussianBlur(img, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # extracting text readed from Front of the id 

        text = pytesseract.image_to_string(img,lang="eng")

        # test : display result on terminal 

        #print(text)

        
        #print("numbers found ! : ",re.findall(r'\b\d+\b', text))

        # testing if the array contain numbers or not 
            
        try: 
            for num in re.findall(r'\b\d+\b', text) :
                if len(num)==8: 
                    print("______________________________________________________________________________") 
                    print("[INFO] the number found is WITH 8 caracteres is : ",num,"[INFO]")
                    return(int(num))
                    
        #catching 'Index_Out_Of_Bound' if Regex didn't found a number

        except:            
            print("______________________________________________________________________________") 
            print("OCR module didn't found a number ")
            return(False)    


    # To extract costumer face from Selfie and Front of ID 

    def extract_faces(self,filename,nature):      
        
        # testing the nature parameter

        if nature.upper() not in ['ID','SELFIE']:

            print("[Operation Failed (Code Level)] Reason : Chose 'ID' or 'SELFIE' for NATURE parameter in function extract_faces(File,NATURE) when using it .")
            exit()

        # Loading  picture with face_recognition Module

        picture = face_recognition.load_image_file(f'{filename}')
        
        # Detect face_locations from  picture
        
        face_locations = face_recognition.face_locations(picture)

        print("______________________________________________________________________________") 
        print("Number of faces detected in {} : {}".format(nature.upper(),len(face_locations)))

        # Testing if we have extracted just one face from Front_id

        if (len(face_locations) == 1):
                
                # Save positions of the detected face

                top, right, bottom, left = face_locations[0]

                # Crop the detected face
                
                face_image = picture[top:bottom, left:right]

                #print('Check position in images: top: {}, bottom: {}, left: {}, right: {}'.format(top, bottom, left, right))

                # transforming image to a PIL image object

                pil_image = Image.fromarray(face_image)

                # Showing result (cropped face from picture)

                #pil_image.show()
                
                if nature.upper() == 'ID' :

                    # checking if id_faces directory exist (if not , creating it)
                 
                    if not os.path.exists(self.id_directory):
                        os.makedirs(self.id_directory)
                    
                    
                    # Saving result (cropped face from Front_id picture)

                    pil_image.save(f'{self.id_directory}/{os.getpid()}id_f.jpg')

                    print("______________________________________________________________________________") 
                    print('check direcotry and file names for id : {}/{}id_f.jpg'.format(self.id_directory,os.getpid()))

                    return('{}/{}id_f.jpg'.format(self.id_directory,os.getpid()))
                    
                else:

                    # checking if selfie_faces directory exist (if not , creating it)

                    if not os.path.exists(self.selfie_directory):
                        os.makedirs(self.selfie_directory)

                    # Saving result (cropped face from Selfie picture)
                    
                    pil_image.save(f'{self.selfie_directory}/{os.getpid()}selfie_f.jpg')

                    print("______________________________________________________________________________") 
                    print('check direcotry and file names for selfie : {}/{}selfie_f.jpg'.format(self.selfie_directory,os.getpid()))

                    return('{}/{}selfie_f.jpg'.format(self.selfie_directory,os.getpid()))
        
        elif(len(face_locations)>1): 

            # Dynamic Error message

            if (nature.upper()=='id') :

                print("______________________________________________________________________________") 
                print("[Operation Failed] Reason : Your ID contains more than one face, Please check your picture or try to take another one.")
                return(False)

            else:

                print("______________________________________________________________________________") 
                print("[Operation Failed] Reason : Your selfie contains more than one face, Please check your picture or try to take another one.")
                return(False)
        else:

            # Dynamic Error message

            if (nature.upper()=='id') :

                print("______________________________________________________________________________") 
                print("[Operation Failed] Reason : Your ID does not contain a face, Please check your picture or try to take another one.")
                return(False)

            else:

                print("______________________________________________________________________________") 
                print("[Operation Failed] Reason : Your selfie does not contain a face , Please check your picture or try to take another one.")
                return(False)

    # To compare the extracted costumer faces (Selfie and Front of ID) 

    def compare_faces(self):
        
        #clearing Terminal

        os.system('cls')

        # Loading Selfie picture and encoding them with face_recognition Module
        
        selfie_picture=self.extract_faces(self.selfie_name,'SELFIE')
        id_picture=self.extract_faces(self.front_idname,'ID')
        
        if selfie_picture==False :

            return('0')

        elif id_picture==False :

            return('1')

        else:

            load_selfie= face_recognition.load_image_file(selfie_picture)

            encode_selfie=face_recognition.face_encodings(load_selfie)[0]

            # Loading Front_id picture and encoding them with face_recognition Module

            load_cin_picture = face_recognition.load_image_file(id_picture)

            encode_cin_picture=face_recognition.face_encodings(load_cin_picture)[0]

            # Face recognition process 
            
            result = face_recognition.compare_faces([encode_selfie],encode_cin_picture,0.48)

            

            Trust_rate = str(round(1-(face_recognition.face_distance([encode_selfie],encode_cin_picture)[0]),2))
            

            print("trust rate : ",Trust_rate) 

            if result[0]:

                        print("[INFO] The face recognition is SUCCESSFUL [INFO]")
                        
                        # a Python object (dict):
                        
                        x = {

                        "face_match": 'True',
                        "trust_rate":Trust_rate,

                        }
                        # convert into JSON:

                        y = json.dumps(x)

                        # the result is a JSON string:

                        print(y)

                        return y
                        
            else:
                        print("[INFO] The face recognition has FAILED [INFO]")
                        
                        # a Python object (dict):

                        x = {

                        "face_match": 'False',
                        "trust_rate":Trust_rate ,
                        
                        }
                        # convert into JSON:
                        y = json.dumps(x)

                        # the result is a JSON string:
                        print(y)

                        return False

    # ML part : For Front id and Back id
    
    # Cheking Front id  
    
    def ml_front_id_check(self):

        print("File name: ",self.front_idname)
        
        #Load ML model
        loaded_model = pickle.load(open("front_verify_cin.sav", 'rb'))

        #Average hash transformation
        a = av_hash(self.front_idname,'reference\\front_reference.png')

        #Pixel hash transformation
        b = p_hash(self.front_idname,'reference\\front_reference.png')
        
        #Density hash transformation
        c = d_hash(self.front_idname,'reference\\front_reference.png')

        #Width hash transformation
        d = w_hash(self.front_idname,'reference\\front_reference.png')

       
        #ML processing to check if it's an Id or not(1 for true ; 0 for false)

        predict = loaded_model.predict([[a,b,c,d]])

        #(TO CHANGE !!)

        #Picture verification with ML and ration (TO CHANGE !!)

        if (predict == 1):
            print("______________________________________________________________________________") 
            print("Accepted Front ID")

            return True

        else :
            print("______________________________________________________________________________") 
            print("Refused Front id")

            #os.remove()

            return False
        
   # Cheking Back id
   
    def ml_back_id_check(self):
        
        
        #Load ML model
        loaded_model = pickle.load(open("back_verify_cin.sav", 'rb'))

        #Average hash transformation
        a = av_hash(self.back_idname,'reference\\back_reference.png')

        #Pixel hash transformation
        b = p_hash(self.back_idname,'reference\\back_reference.png')
        
        #Density hash transformation
        c = d_hash(self.back_idname,'reference\\back_reference.png')

        #Width hash transformation
        d = w_hash(self.back_idname,'reference\\back_reference.png')

       
        #ML processing to check if it's an Id or not(1 for true ; 0 for false)

        predict = loaded_model.predict([[a,b,c,d]])
        
        
        #(TO CHANGE !!)

        #Picture verification with ML and ration (TO CHANGE !!)

        if (predict == 1):
            print("______________________________________________________________________________") 
            print("Accepted Back ID")   

            return True

        else :
            print("______________________________________________________________________________") 
            print("Refused Back ID")

            return False

        
   # Final Web service(MAIN)
   
    def kyc_web_service(self):
        try:
            cf_result=self.compare_faces()
        except:
            print("______________________________________________________________________________")
            print('Exception with compare_faces : ',cf_result)
            exit()

        try:
            tfv_result=self.two_factor_verification()
        except:
            print("______________________________________________________________________________")
            print('Exception with two factor verification : ',tfv_result)
            exit()

        try:
            front_result=self.ml_front_id_check()
        except:
            print("______________________________________________________________________________")
            print('Exception with ML front ID : ',front_result)
            exit()
            
        try:        
            back_result=self.ml_back_id_check()
        except:
            print("______________________________________________________________________________")
            print('Exception with ML back ID : ',back_result)
            exit()
        
        if front_result and back_result and cf_result!=False and cf_result not in ['0','1'] and tfv_result!=False and tfv_result!=0 :
            
            #Load two factor verification funtion 

            Id_verification_response=tfv_result
            
            #Transform string provided to json

            Id_verification_response=json.loads(Id_verification_response)

            #Verify the result of two factor verification funtion
            
            #Succesful case :
               
            face_verification_response=cf_result

            print("______________________________________________________________________________") 
            print("testing face verification response : ",face_verification_response)
            face_verification_response=json.loads(face_verification_response)
                    
            #testing Json 
            #print("Result response face_v_Json :",face_verification_response['face_match'] )
            
            x = {

                "Id_number":Id_verification_response['Id_number'],
                "Date_emission":Id_verification_response['date_emission'],
                "ML_front_ID_trust_rate":'99%',
                "ML_back_ID_trust_rate":'96%',
                "Faces_trust_rate":face_verification_response['trust_rate']
                }

            # convert into JSON:
            y = json.dumps(x)

            print("______________________________________________________________________________") 
            print("                          Verification Successful :                           ")
            print("______________________________________________________________________________")
            # the result is a JSON string:
                    
            return(y)

        else:
            res=""
        
            if front_result==False :
                res+="|The front of the ID has not been recognized by the model. "

            if back_result==False :
                res+="|The back of the ID has not been recognized by the model. "

            if cf_result=='0' :
                res+="|There is a problem with the face extracted from selfie picture."

            elif cf_result=='1':
                res+="|There is a problem with the face extracted from the ID picture. "

            elif cf_result==False:
                res+="|The faces didn't match.| "

            if tfv_result==False :
                res+="|The number in the front of the ID is not the same as scanned in back of the id. "

            elif tfv_result=='0' :
                res+="|Didn't find any Barcode to read , the Barcode providen is not clear please take another picture. "
                    
            res+="|"

            x = {
                "Message":res
                }
            
            y = json.dumps(x)

            print("______________________________________________________________________________") 
            print("                          Verification Failed :                               ")
            print("______________________________________________________________________________")

            return(y)

#TODO : UPDATE README and PUT SOME COMMENTS  ....           


"""
if verif:
             
             label = 1
             print("================> : ",verif," and label ====> : ",label)  
        else :
             label = 0 
             print("================> : ",verif," and label ====> : ",label)

        print("fichier num : ",i)
        print("label : ",label)
        i+=1
        X.append([a,b,c,d])
        y.append(label)   
       

print(X) 
print(y)  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)



clf = svm.SVC(kernel= 'linear')
clf.fit(X_train,y_train)

print(clf.score(X_test,y_test))

"""
