import requests
import json
import datetime
import cv2
import time

def messageStructure(line, machine, ISN, img_url, webhook_url, isn):
    fecha = datetime.datetime.now()

    card = {

    
       "type":"message",
       "attachments":[
          {
             "contentType":"application/vnd.microsoft.card.adaptive",
             "contentUrl":None,
             "content":{
                "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",   
                "version": "1.5",
                "body": [
                    {
                        "type": "Image",
                        "altText": "Image of abnormal glue",
                        "size": "Medium",
                        "style": "RoundedCorners",
                        "url": img_url,
                        "targetWidth": "Wide"
                    },
                   
                    {
                        "type": "TextBlock",
                        "wrap": True,
                        "size": "Large",
                        "weight": "Bolder",
                        "color": "Default",
                        "text": "GLUE INSPECTION AI ALERT " #CHANGE FOR YOUR OWN TITLE
                    },
                    {
                        "type": "TextBlock",#THIS IS THE FIRST TEXT BLOCK
                        "text": f"Abnormal glue detected on {fecha}",
                        "wrap": True,
                        "spacing": "None",
                        "fontType": "Default",
                        "size": "Small",
                        "weight": "Default",
                        "isSubtle": True,
                        "color": "Default"
                    },
                    {
                        "type": "TextBlock",
                        "text": f"Line: {line}, Machine: {machine}",
                        "wrap": True
                    },
                    {
                        "type": "TextBlock",
                        "text": f"ISN: {ISN}",
                        "wrap": True
                    },
                    {
                        "type": "TextBlock",
                        "text": f"Path to folder: {isn}",
                        "wrap": True
                    },
                    {
                        "type": "ActionSet",
                        "targetWidth": "atLeast:Narrow",
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "Open Link",
                                "url": img_url #HERE IS WHERE WE ADD THE LINK OF OUR PICTURE IN THE WEBSERVER TO SHOW 
                            }
                        ],
                        "spacing": "Medium"
                    }
                ]
             }  
        }
          
    ]
 }
    
    print("Testing webhook…")
    print(f"URL: {webhook_url}")

    retries=5
    attempts = 0
    while attempts < retries:
        try:
            response = requests.post(
            webhook_url,
            json=card,
            timeout=20,
            headers={'contentType': 'application/json'}
        )

            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code in [200, 202]:
                attempts=5
                print(" Test message sent successfully!")
                print(" Check your Teams channel now")
            else:
                print(f" Attempt {attempts} failed")
                attempts=+1
                

        except Exception as e:
            print(f" Error: {e}")
            #input("Press Enter to continue…")
        if attempts < retries :
            print("retrying in 2 seconds...")
            time.sleep(2)
        else:
            print("All attempts retried")


