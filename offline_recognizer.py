#Authors - Harsh Athavale & Abdul Samadh Azath

from xmlparser import Parser
from recognizerV2 import NDollarRecognizer
from copy import deepcopy
from random import randint, shuffle
from json import dumps
import csv
from constants import GESTURE_LIST

class OfflineRecognizer(): #Offline recognizer code
    def __init__(self): # this initilizes the data structures
        self.parser = Parser()
        # self.recognizer = NDollarRecognizer(True)
        # Load offline data
        self.offlineData = self.parser.getOfflineData()
        # print(dumps(self.offlineData))
        # Pre process offline data
        # self.preProcessOfflineData()
        # Recognize offline data
        self.recognizeOfflineData()
    
    def recognizeOfflineData(self): # this is the main loop 
        score = {} #dict to store the scores
        logcsv = [] # list to store theh logfile contents 
        total=0 # total iterations
        correct=0  # number of correct matches 
        iterations = 10 # number of iterations
        examples_start, examples_end = 1,9 # Start and End number of examples
        user_count = 0
        total_examples = (examples_end - examples_start + 1)*len(self.offlineData)
        example_count = 0
        for user in self.offlineData: # For each user
            user_count += 1
            score[user] = {}
            for example in range(examples_start,examples_end+1): # For each example from 1 to 9
                example_count += 1
                print('Processing Example {}/{} for {} completed {}%'.format(example, examples_end, user,int((example_count/total_examples)*100)))
                score[user][example] = {}
                for i in range(1,iterations+1): # For iterations from 1 to 10


                    # print(len(self.preProcessedData[user]['medium']))
                    # print(len(self.preProcessedData[user]['medium']['arrow']))
                    # print(len(self.preProcessedData[user]['medium']['arrow'][0]))
                    
                    # Get training and testing set
                    training_set, testing_set = self.getSplitData(self.offlineData[user], example, user)

                    items = list(training_set.items())
                    shuffle(items)
                    training_set = dict(items)
                    # print(training_set)
                    # print(len(training_set))
                    # print(len(testing_set))
                    recognizer = NDollarRecognizer(True,training_set) # loads the recognizer with training templates. 

                    for gesture_raw,points in testing_set.items(): # iterates through each gesture in the training set and predicts the gesture. 
                        gesture = gesture_raw.split('|')[0]
                        if gesture not in score[user][example]:
                            score[user][example][gesture] = 0

                        # print(points) 
                        # recognizedGesture_raw, recognitionScore, _,Nbest = recognizer.Recognize(points)
                        Result, NBest= recognizer.Recognize(points,with_Nbest=True)
                        recognizedGesture_raw, recognitionScore = Result.Name,Result.Score

                        recognizedGesture = recognizedGesture_raw.split('|')[0]
                        # print(recognizedGesture)

                        #data structure for storing logfile results. 
                        log = {}
                        log['User'] = user
                        log['Gesture Type'] = gesture
                        log['RandomIteration'] = i
                        log['#ofTrainingExamples'] = example
                        log['TotalSizeOfTrainingSet'] = len(training_set)
                        log['Training Set Contents'] = [key for key in training_set]
                        log['Candidate'] = gesture_raw
                        log['RecoResult'] = recognizedGesture
                        log['Correct or Incorrect'] = 1 if recognizedGesture == gesture else 0
                        log['RecoResultScore'] = round(recognitionScore,3)
                        log['RecoResultBestMatch'] = recognizedGesture_raw
                        log['RecoResultNBestSorted'] = self.getTopN(NBest,50)
                        
                        logcsv.append(log)
                        if recognizedGesture == gesture:
                            score[user][example][gesture] += 1
                            correct+=1
                        total+=1
        totalAverageAccuracy = (correct/total)*100  # average accuracy over  all recognitions  
        self.writeToFile(dumps(score), 'score.json')
        self.writeToCsv(logcsv,'logfile.csv', totalAverageAccuracy, score, iterations, examples_end-examples_start+1)
    

    def getSplitData(self, gestures, E, user): # this splits the data into training and testing.
        training_set = {}
        testing_set = {}
        for gesture,points in gestures.items(): # For each gesture pick E training examples and 1 testing example
            random_list = [i for i in range(0,10)]
            shuffle(random_list)
            training_examples = []
            for i in range(0,E):
                training_examples.append(random_list[i])
            for i in training_examples:
                training_set["{}|{}|E{}".format(gesture,user,i+1)] = points[str(i)]
            testing_example = random_list[E]
            # print("----------------------")
            # print(points)
            testing_set["{}|{}|E{}".format(gesture,user, testing_example+1)] = points[str(testing_example)]
        return training_set, testing_set
    
    def writeToFile(self, data, filename): # writes score to file. 
        file = open(filename, 'w')
        file.write(data)
        file.close()
    
    def getTopN(self, Nbest, N): # this chooses N or 50 , whichever is the least. 
        if len(Nbest) > N:
            return {value[0]:value[1] for i, value in enumerate(Nbest.items()) if i <= N}
        else:
            return Nbest
            
    def writeToCsv(self,dict_data,filename, totalAverageAccuracy, score, iterations, eRange): #Writes to logfile. 
        print("Processing complete! Writing to csv.")
        csv_columns = ['User','Gesture Type','RandomIteration','#ofTrainingExamples','TotalSizeOfTrainingSet','Training Set Contents','Candidate','RecoResult','Correct or Incorrect','RecoResultScore','RecoResultBestMatch','RecoResultNBestSorted']
        csv_file=filename
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in dict_data:
                    writer.writerow(data)
                writer.writerow({})
                writer.writerow({'User':'Total Average Accuracy', 'Gesture Type':totalAverageAccuracy})
                for user in score:
                    for example in score[user]:
                        gestureSum = 0
                        for gesture in score[user][example]:
                            gestureSum += score[user][example][gesture]
                        gestureAccuracy = ((gestureSum/(len(GESTURE_LIST)*iterations)))*100
                        writer.writerow({'User':'Accuracy for User:{} E:{}'.format(user,example),'Gesture Type':round(gestureAccuracy,1)})
        except IOError:
            print("I/O error")
