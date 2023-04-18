Graphical User Interface



The graphical user interface is simple with a canvas with a white background and clear and submit buttons. It displays the Result of the expression, Predicted Gesture and confidence score. 



Users can interact with it using Keypad or Touch. 



Online Recognition 



Component A - Store the points.



On each mouse drag the points for each stroke are stored using the draw function at line(). All the points are stored in the points array. 



Component B - N$ recogniser 



The collected points are passed to the Recognise function in the N$ recogniser after initialising it with the set of points collected. 

On clicking the submit button The Recognise function combines the separate strokes and then Resamples, Rotates, Scales and translates 

the points by calling the unistroke class at line() in recognizerV2.py file.  

The recognised gesture is calculated by finding best angle between the user input and the template gestures which is followed by picking up 

The gesture which has the minimum distance from the user gesture. These computation are done by using the function in the recognizedV2Utils.py 

file.  



Component C - Output the result 



The result is displayed on the GUI which shows the recognised gesture and the confidence score for each gesture that the user draws





Equation calculation 



Component A - Storing the points 

For this operation the points are stored in a sequential manner. For example if the user inputs (3 + 2) x 5, then initially the individual stroke will be stored 

as ( , 3 , - , | , 2 , ) , \ , / , 5. 



Component B - Segmentation 



The segmentation is present in the segment.py file which is responsible for making sense out of the single strokes. It uses the function 

IsOverlapping on lie 23 in the segment.py file to check if any two single strokes are overlapping or not. 

Here for example the plus sign (+) and the multiplication sign (x) have overlapping strokes. It combines them to be considered as a single gesture with multiple strokes. This is done by calculating the Euclidian distance between every point stroke 1 and every point in stroke 2. If the the distance between any 

Pair points (one in stroke 1 and the other in stroke2 ) is less than or equal to the threshold value, which is set to 10, then the strokes are considered 

Overlapping and combined. 



After this step the points are fed into the N $ recogniser by calling the startRecognition function at line 81 in segment.py file. 



The result of the recognition is a list of the recognised gestures. 

So for (3+2) x 5 we get a list as [‘(’ , ’3’,  ’+’ , ‘2’ , ‘)’ , ‘x’ , ‘5’  ]. 



Component C - Calculation of expression



The resultant list is then passed to the calculation function at line() in the board.py file. This function stores all the members of the list in a 

String format and uses the evaluation function “eval( )” to evaluate the string. It respects the PEDMAS rules and calculates the result accordingly. 





Component D - Displaying the Result

The calculated result is displayed on the GUI and is updated whenever the user clears the board and tries a new expression. 



 



Offline Recognition 



Component A - Read in Dataset. 

    The xml files were stored locally from the N$ website. The xmlparser.py file reads the gesture points 

    for each gesture for each speed for each user. 





Component 2 - Connect to Recognizer 

The offline_recognizer.py from Project 1 was adapted to accommodate the recognition of multi-stroke points.



To achieve this, the following steps were implemented:



The xml data was imported into a python dictionary.
The N dollar recogniser was used to then recognise the gestures. 




Component 3 - Loop over Dataset



The data is split into training and testing templates using the getSplitData(Line 88) function and the recognizer is loaded with the training set for each user, example, and gesture. The inputs are tested using testing data against the training examples in the same order, and the N-best list is calculated.

The calculation of the N-best list is performed in the recognizerV2.py (Line 91) file.







Component 4 - Output Results 



All the following results are logged into the logfile.csv file using the writeToCsv function Line (124). In the offline_recognizer.py



'User','Gesture Type','RandomIteration','#ofTrainingExamples',

'TotalSizeOfTrainingSet','Training Set Contents','Candidate',

'RecoResult','Correct or Incorrect','RecoResultScore',

'RecoResultBestMatch','RecoResultNBestSorted'







Collecting Data





Component A - Write Gesture Files



The gesture files are written by creating a submit button, which, when clicked by the user, triggers the 

"createXMLUserLogs" function (line 227, Line 275) in board.py.

This function first stores the data in json format and then converts it into the required XML format (line 293 - 336, board.py).







Component B - Prompt for specific samples



   We display prompts  by showing labels (line 78,board.py) showing what is to be drawn next.

    When the user starts, he/she is prompted to draw gestures by displaying "Please draw a <gesture name>". 



    There is a clear canvas button which clears the canvas if the the participant makes a mistake. He/she can

    then draw the gesture again. 



    A submit button is included (line 196, board.py) which when clicked records the points of the current gesture and prompts the user 

    to draw the next gesture. 



    A thankyou messege is shown when the user is done with the study. 



Component C - Recruit 6 people 



   For this part of the project, six people were recruited. They were informed about the study, the time it would take, the specifics, and the risks and were required to sign a consent form. Each user took approximately 15-20 minutes to complete the task.



Component D - Submit the full Dataset. 



    The XML files are stored in the xml_collected_logs folder. Each user has their own folder containing XML files for all 17 gestures and 10 different samples of each gesture. In total, each user has 170 gestures, and there are a total of 1020 gestures for all six users.







Exploring Data