#Authors - Harsh Athavale & Abdul Samadh Azath

Part 2 - Online Recognition
***************************

Component A - Store the points:
-------------------------------
We monitor all the mouse button press, drag and release events on the canvas. This is done on line 176 in board.py in the setMouseBindings() function.
The draw event is used to store the points(unistroke) list defined at line 24 in board.py. This points array stores all the unistrokes.
Each unistroke is recorded and added to allPoints list defined at line 30 in board.py when the mouse button is released and points(unistroke) list
is cleared. When the submit button is clicked the allPoints list which is the set of all unistrokes recorded in the current session is sent for recognition. 

Component B - Store Template
----------------------------
We store the template for online recognition in online_template.py. We use 10 samples for each gesture as a template. 

Component C1 - N$ recogniser
---------------------------- 
The collected points are passed to the Recognise function in the NDollarRecognizer class in recognizerV2.py after initialising it with the set of
template points. 
On clicking the submit button The Recognise function combines the separate strokes and then Resamples, Rotates, Scales and translates 
the points by calling the unistroke class at line 20 in recognizerV2.py file. We will be using bounded rotation invariance.
The recognised gesture is calculated by finding best angle between the user input and the template gestures which is followed by picking up 
The gesture which has the minimum distance from the user gesture. These computation are done by using the Recognize function in the NDollarRecognizer
class in the recognizedV2Utils.py file.

Component C2 - Equation Calculation
-----------------------------------
Storing the result:
For this operation the points are stored in a sequential manner. For example if the user inputs (3 + 2) x 5, then initially the individual stroke
will be stored as ( , 3 , | , - , 2 , ) , \ , / , 5.

Segmentation:
The segmentation code is present in the segment.py file which is responsible for making sense out of the single strokes. It uses the function 
IsOverlapping on line 23 in the segment.py file to check if any two single strokes are overlapping or not. 
Here for example the plus sign (+) and the multiplication sign (x) have overlapping strokes. It combines them to be considered as a single gesture with multiple strokes. This is done by calculating the Euclidian distance between every point stroke 1 and every point in stroke 2. If the the distance between any 
Pair points (one in stroke 1 and the other in stroke2 ) is less than or equal to the threshold value, which is set to 10, then the strokes are considered 
Overlapping and combined. 

Component D - Output the result
-------------------------------
The result is displayed on the GUI which shows the recognised gesture and the confidence score for each gesture that the user draws using the setPredictionLabels() function defined in line 131 in board.py. 



Part 3 - Offline Recognition
**************************** 

Component A - Read in Dataset.
------------------------------
The xml files were stored locally from the N$ website for the MMG datset in the mmg folder. The xmlparser.py file reads the gesture points for each gesture for medum speed for each user. 


Component B - Connect to Recognizer
-----------------------------------
The offline_recognizer.py from Project 1 was adapted to accommodate the recognition of multi-stroke points.
To achieve this, the following steps were implemented:
The xml data was imported into a python dictionary in the class Parser in xmlparser.py.
For each user we generate training_set and testing_set using getSplitData(Line 88) in offline_recognizer.py
For each user we create a NDollarRecognizer object with the training data as the template. This can be seen at line 56 in
offline_recognizer.py. 


Component C - Loop over Dataset
--------------------------------
The data is split into training and testing templates using the getSplitData(Line 88) function and the recognizer is loaded with the training set for each user, example, and gesture. The inputs are tested using testing data against the training examples in the same order, and the N-best list is calculated.
The calculation of the N-best list is performed in the recognizerV2.py (Line 91) file.

Note: The N-Best list will only contain those gestures which are within the AngleSimilarityThreshold as used on line 75 in recognizerV2.py. 

Component D - Output Results
-----------------------------
All the following results are logged into the logfile.csv file using the writeToCsv function Line (124). In the offline_recognizer.py

'User','Gesture Type','RandomIteration','#ofTrainingExamples',

'TotalSizeOfTrainingSet','Training Set Contents','Candidate',

'RecoResult','Correct or Incorrect','RecoResultScore',

'RecoResultBestMatch','RecoResultNBestSorted'


Part 4: Collecting Data
***********************


Component A - Write Gesture Files
---------------------------------
The gesture files are written by creating a submit button, which, when clicked by the user, triggers the 
"createXMLUserLogs" function (line 227, Line 275) in board.py.
This function first stores the data in json format and then converts it into the required XML format (line 293 - 336, board.py).

Component B - Prompt for specific samples
-----------------------------------------
We display prompts  by showing labels (line 78,board.py) showing what is to be drawn next.
When the user starts, he/she is prompted to draw gestures by displaying "Please draw a <gesture name>". 
There is a clear canvas button which clears the canvas if the the participant makes a mistake. He/she can then draw the gesture again. 
A submit button is included (line 196, board.py) which when clicked records the points of the current gesture and prompts the user
to draw the next gesture. 
A thankyou messege is shown when the user is done with the study. 



Component C - Recruit 6 people
------------------------------
For this part of the project, six people were recruited. They were informed about the study, the time it would take, the specifics, and
the risks and were required to sign a consent form. Each user took approximately 15-20 minutes to complete the task.


Component D - Submit the full Dataset
-------------------------------------
The XML files are stored in the xml_collected_logs folder. Each user has their own folder containing XML files for all 17 gestures and 10 different samples of each gesture. In total, each user has 170 gestures, and there are a total of 1020 gestures for all six users.


Part 5: Exploring Data
**********************

Component A - Run an offline recognition test
---------------------------------------------
We used the data we collected in part 4(stored in xml_collected_logs) and ran the offline
recognition we built in part 3.


Component 2 - Output the result
-------------------------------
We ran the offline_recognizer.py module for the data we collected from main.py(line 8) and created the log file named
logfile-10iter-6user.csv. We used 10 iterations and training examples ranging from 1 to 9 per user.
The selection of training set and testing gesture is completely randomized.

The same experiment was conducted on the mmg dataset and the offline recognition is stored in logfile-20-user-10-iter.csv.
    

Component 3 - Analyze dataset using GHoST
-----------------------------------------
We needed to modify the xml which we collected from the user(xml_collected_logs) to make it
compatible with the GHoST tool. We had to tweak the attribute names using modifyXML.py and stored
the edited xml files in xml_modified_logs. Then we used GHoST
tool to generate heatmap, confusion matrix and feature data on xml_edited_logs.


Component 4 - Extract user articulation insights
------------------------------------------------
1. There is a big variation in the size of the X. The second  stroke of the X changes drastically with the users.
2. The size of 0 differs a lot among all the users. 
3. The minus, slash, and caret were the symbols with the least variation owing to their simple straight line structure.
4. All numbers had a generally very low variation except 8 which was the most complicated structure to draw due to its frequent curves, which
indicates that drawing straightline gestures is easier than curved ones.


Artifacts
----------

Data collected from 6 users - HCIRA2/xml_collected_logs
Offline Recognition file for data collected from 6 users - HCIRA2/logfile-6-user-10-iter.csv
Offline Recognition file for MMG Dataset - HCIRA2/logfile-20-user-10-iter.csv
GHoST Feature Data - HCIRA2/ghost_analysis/feature_data.csv
GHoST Heatmap - HCIRA2/ghost_analysis/heatmap.bmp
Concent Forms - HCIRA2/consent_forms