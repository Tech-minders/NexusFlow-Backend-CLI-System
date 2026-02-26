import os  
import json


class Storage:

    @staticmethod
    #method to load JSON data from a file, create file if it does not exist
    def load(file):
        
        # Create 'data' folder if it doesn't exist
        os.makedirs("data", exist_ok=True) 
        # Check if the file exists 
        if not os.path.exists(file): 
        # Create the file if it doesn't exist 
            with open(file, "w") as f:  
                json.dump([], f) 
        # Open file in read mode
        with open(file, "r") as f:  
            return json.load(f)  
        
    @staticmethod
    def save(file, data):
        #Save JSON data to a file
        with open(file, "w") as f:  
            json.dump(data, f, indent=4) 