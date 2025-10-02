import os
import json
import time
import datetime
import requests
from webserver import AOIImageServer
import threading 
from Team_Sender import messageStructure



with open("parameterss.json", "r") as file:
    config = json.load(file)

start_time = datetime.datetime.now()
main_path = config["ng_path"]
receiver = config["receiver"]
valid_models = config["models"]
processed_log = config ["enviados_log"]
check_interval = config["check_interval"]
teams_webhook = config["teams_webhook_url"]

PORT= 8080
LOCAL_SERVER_DIR = "aoi_imges"
server = AOIImageServer(port=PORT, images_dir=LOCAL_SERVER_DIR)
threading.Thread (target = server.start_server, daemon=True).start()
print(f"Server started in {server.base_url}")

if os.path.exists(processed_log):
    with open(processed_log, "r") as f:
        processed_folders = set(line.strip() for line in f if line.strip())
else:
     processed_folders = set()


def get_subfolders(main_path):
    try:
        return [os.path.join(main_path, d) for d in os.listdir(main_path) if os.path.isdir(os.path.join(main_path, d))]
    except Exception as e:
        print(f"Error accessing {main_path}: {e}")
        return[]
    
def search_fail():
    for model in get_subfolders(main_path):
        fecha = datetime.datetime.now()
        model_name = os.path.basename(model)

        line = model_name[:3]
        machine = model_name[3:]

        print(f"Checking model: {model_name}, Line: {line}, Machine: {machine}")

        for year in get_subfolders(model):
            for month in get_subfolders(year):
                for day in get_subfolders(month):
                    for isn in get_subfolders(day):
                        ISN_fixed = isn.split("\\")

                        ISN_final = ISN_fixed[-1].strip()
                        print(ISN_final)
                        
                        if isn in processed_folders:
                            continue
                        try:
                            creation_time = datetime.datetime.fromtimestamp(os.path.getctime(isn))
                        except Exception as e:
                            print(f"Creation time cannot be read for {ISN_final}: {e}")
                            continue

                        if creation_time > start_time:
                            time.sleep(5)
                            print(f"New ISN with defect found {ISN_final}, uploading to webserver")
                            img_path = isn+"\\"+ISN_final+".jpg"
                            
                            #print("imagen path", img_path)
                            try:
                                
                                if os.listdir(isn): 
                                    url = server.upload_image(img_path)
                                    print("Esta es la URL", url)
                              
                            except Exception as e:
                                print(f"error obteniendo la URL {e}")
                            try:
                            
                                teams_message = messageStructure(line, machine, ISN_final, url, teams_webhook, isn)
                            except Exception as e:
                                print(F"Error sending teams notification: {e}")

                            with open (processed_log, "a") as f:
                                f.write(isn+ "\n")
                                processed_folders.add(isn)
                                print(f"✅ {fecha} - Processed: {ISN_final}")



if __name__ == "__main__":
    print("AOI Folder monitoring started...")
    while True:
        try: 
            search_fail()
            time.sleep(check_interval)
        except KeyboardInterrupt:
            print("Monitoring interrupted by user")
        except Exception as e:
            print(f"Error {e}")
            time.sleep(check_interval)


