import http.server
import socketserver
import os
import shutil
from datetime import datetime, timedelta
import threading
import time
import socket

class AOIImageServer:
    def __init__(self, port=8080, images_dir ="aoi_images"):
        self.port = port
        self.images_dir = images_dir
        self.base_url = f"http://{self.get_local_ip()}:{port}"

        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
            print( f"Created Images directory: {images_dir}")
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"

    def cleanup_old_images (self, max_age_hours = 120):
        cutoff_time = datetime.now() - timedelta(hours = max_age_hours)
        for filename in os.listdir (self.images_dir):
            file_path = os.path.join( self.images_dir, filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff_time : 
                    os.remove(file_path)
                    print(f" Cleaned up old image: {filename}")
    
    def start_cleanup_thread (self):
        threading.Thread (target = self.cleanup_loop, daemon=True).start()
        print("Started automatic cleanup thread (every hour)")
    def cleanup_loop(self):
        while True:
            time.sleep(3600)
            self.cleanup_old_images()

    def upload_image(self, isn_path):
        print("origen", isn_path)
        print("Origin exists?", os.path.exists(isn_path))

        try: 
            if not os.path.exists(isn_path):
                return None
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = os.path.basename(isn_path)
            name_without_ext, ext = os.path.splitext(original_name)
            unique_name = f"{timestamp}_{name_without_ext}{ext}"
            destination = os.path.join(self.server_path, unique_name)
            print("Destination", destination)
            shutil.copy2(isn_path, destination)
            public_url = f"{self.base_url}/{unique_name}"
            print(f"Image uploaded {public_url}")
            return public_url
        except Exception as e:
            print(f"Failed to upload image: {e}")
            return None

    def start_server(self):
        try:
            os.chdir(self.images_dir)    
            handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer (("", self.port), handler)
            print( f" AOI Image Server Running")
            print(f"Server URL: {self.base_url}")
            self.server_path = os.path.abspath('.')
            print(f"serving from: {self.server_path}")
            self.start_cleanup_thread()
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n Server stopped by user")
            httpd.shutdown()
        except Exception as e:
            print(f"Server error: {e}")
    
 