'''
Goal
----
You will be entering an HTTP maze. Your goal is to get out of it!

API
---
ENDPOINT = "https://settlement-challenging-photographer-sandy.trycloudflare.com"
The maze will be represented as an API with one GET endpoint.
To enter the maze, head over to https://settlement-challenging-photographer-sandy.trycloudflare.com
To go to a specific step in the maze, GET /<STEP_ID>
The final step of the maze will return a "CONGRATS" message.

Instructions
------------
Print the STEP_ID of the final step

'''
import requests

class RampMaze:

    def __init__(self):

        self.visited = set()

    
    def make_request(self, url: str) -> dict:

        url = url.lower()

        data = requests.get(url, timeout=5)
        print(data.json())
        return data.json()
    
    def get_next_step(self, step_id: str) -> dict:

        self.URL = self.URL.lower()

        new_url = self.URL + "/" + step_id 

        return new_url
    
    def is_end_maze(self, message: str) -> bool:

        if message == "CONGRATS":
            print("SUCCESS WE HAVE ENDED MAZE") 
            return True
        return False 
    

    

    


       

if __name__ == "__main__":

    engine = RampMaze()

    engine.make_request()
    engine.get_next_step('XCMGOOAFHX')

        






