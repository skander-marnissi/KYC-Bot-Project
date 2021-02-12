# KYC-Bot-Project

Know You Customer Bot developed with Sklearn, Tesseract OCR, face_regonition that allows ID verification automatically on python 3.6.

## Installation

Open cmd and type the following commands: 

```bash
git clone https://github.com/SkanderMarnissi/KYC-Bot-Project/
```
Then  

```bash
cd KYC-Bot-Project
pip install -r requirements.txt
```
Don't forget to install Google tesseract to your project.

## How it works?

The program takes three images as input : One for the Front of the ID card the second for Back of the ID card and
the therd for the selfie .

## Usage 

In order to obtain good result methods from the file KYC_BOT_Script.py should be executed in order :

**1> Check if the front id picture provided is a real one with the front id model verification.**

**2> Check if the back id picture provided is a real one with the back id model verification.**

**3> Check if the TWO picture of the ID(Front and Back) are correct with the two factor verification method.**

**4> Compare faces (on Front of the ID and The selfie) with the compare faces method.**

**5> Test the whole process(1,2,3,4) with the kyc web service method.**

## Type 'python' in your terminal: 

```python

#Import the specified script
from KYC_BOT_Script import ImageRecognizer

#Test it with new object created and intialized with input images(example)
test_obj = ImageRecognizer("images\\front_id_test.png","images\\back_id_test.png","images\\selfie_test.png")

# 1.Check if the provided picture is a front id picture
test_obj.ml_front_id_check()

# 2.Check if the provided picture is a back id picture
test_obj.ml_back_id_check()

# 3.Check if image is an Id
test_obj.two_factor_verification()

# 4.compare if face in id card and selfie are the same (tolerance is set to 0.48)
test_obj.compare_faces()

# 5.Check all the steps (1,2,3,4) 
test_obj.kyc_web_service()

```

## To use server 

In order to test your server you should run the KYC_BOT_Server.py file in terminal like this 

```bash

python KYC_BOT_Server.py

```

## Server usage

You must send a JSON file like this format to your server(you can use postman):

    ```json
    {
        "selfie":"( B-64 encoded selfie picture )",

        "selfie_name":"selfie_name_file_name.(jpg|png)",

        "front_cin":"( B-64 encoded front of Id picture )",

        "front_cin_name":"front_cin_file_name.(jpg|png)",

        "back_cin":"( B-64 encoded back of Id picture )",

        "back_cin_name":"back_cin_file_name.(jpg|png)"
    }

    ```
It will automatically start the KYC_BOT_Script module and send a JSON response to the client containing:

    ```json
    {
        "Id_number":"(Id number)",

        "date_emission":"(Emission date of Id)",

        "ML_front_ID_trust_rate":"(Accuracy of the front id verification model)",

        "ML_back_ID_trust_rate":"(Accuracy of the back id verification model)",

        "faces_trust_rate":"(distance between the two faces(id face and selfie face)"

    }

    ```
*SKANDER MARNISSI COPYRIGHT © 2018 - ALL RIGHTS RESERVED*