import API
import time
from Algorithm import *
from Floodfill import FloodFill
from HandRule import LeftHandRule, RightHandRule
from DFS import DepthFirstSearch  

# Function to give the goal green colour to make it different and distinct from the rest locations of the maze
def set_goal():
    API.setText(CENTER, CENTER, "Goal")
    API.setColor(CENTER, CENTER, "G")
    API.setColor(CENTER - 1, CENTER, "G")
    API.setColor(CENTER - 1, CENTER - 1, "G")
    API.setColor(CENTER, CENTER - 1, "G")

def main():
    API.log("Running...")
    API.setColor(0, 0, "G") # Colour the starting point in green 
    API.setText(0, 0, "start") # Define the starting point by "start"

    set_goal() # Call the function to colour the goal
    
    floodfill = FloodFill() # Create an instance of the floodfill algorithm
    leftHandRule = LeftHandRule() # Create an instance of the Left Hand Rule algorithm
    rightHandRule = RightHandRule() # Create an instance of the Right Hand Rule algorithm
    dfs = DepthFirstSearch()  # Create an instance of the DFS algorithm

    #Execute FloodFill algorithm
    #floodfill.execute()
    #time.sleep(3)  

    #Execute LeftHandRule algorithm
    #leftHandRule.execute()
    #time.sleep(3)

    #Execute RightHandRule algorithm
    #rightHandRule.execute()  # Removed unnecessary reinitialization
    #time.sleep(3)

    #Execute DepthFirstSearch algorithm
    dfs.execute()  
    time.sleep(3)


if __name__ == "__main__":
    main()
