import os  
import json

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Storage:

    @staticmethod
    #method to load JSON data from a file, create file if it does not exist
    def load(file):
        
        path = Storage._resolve(file)
        os.makedirs(os.path.dirname(path), exist_ok=True) 
        # Check if the file exists 
        if not os.path.exists(file) or os.path.getsize(path) == 0: 
        # Create the file if it doesn't exist 
            with open(file, "w") as f:  
                json.dump([], f) 
        # Open file in read mode
        with open(path, "r") as f:  
            return json.load(f)  
        
    @staticmethod
    def save(file, data):
        #Save JSON data to a file
        path =Storage._resolve(file)
        os.makedirs(os.path.dirname(path),exist_ok=True)
        with open(file, "w") as f:  
            json.dump(data, f, indent=4) 