from Text_Classifier import Text_Classsifier
import pandas as pd
import header
import logging
from datetime import datetime

class AnalysisEngine():
    
    
    
    
    def performTraining(self , trainingFilePath , textFields , labelColName , modelFilePath  , mask=[] , taskName=""):
        trainingStartTime = datetime.now()
        logging.info( str(trainingStartTime) + " ############## START TRAINING :: " + taskName + " #################################################")
        clf = Text_Classsifier()
        clf.loadTrainingData(trainingFilePath, textFields , labelColName , mask)
        
        # For task 1, make the proportion of risky vs non risky moderate enough to strengthen the model.
        if( (taskName == "Risk Classifier") & header.isRemoveSkewness):
            ratio=header.riskClassifierRatioRemoveSkewness
            df=pd.DataFrame()
            df['text']=clf.text
            df['label']=clf.label
            riskyDf=df[df['label']==1]
            count=int((df[df['label']==1]['label'].size)*ratio)
            nonRiskyDf=df[df['label']==0][:count]
            clf.text = riskyDf['text'].tolist()+nonRiskyDf['text'].tolist()
            clf.label = riskyDf['label'].tolist()+nonRiskyDf['label'].tolist()
        
        
        
        clf.train()
        clf.dumpModelFile(modelFilePath)
        trainingSpeed =  len(clf.text) / (datetime.now() - trainingStartTime).total_seconds() 
        logging.info( str(datetime.now()) + " TRAINING SPEED :: " + str(trainingSpeed)  + " articles per second." )
        logging.info( str(datetime.now()) + " ############## END TRAINING :: " + taskName + " #################################################")
        
    def initiateClassification(self  , textFields , modelFilePath , predictColName , testDataFilePath="" , df=pd.DataFrame() , mask=[] , taskName=""):
        predictStartTime = datetime.now()
        logging.info( str(predictStartTime) + " ############## START PREDICT PHASE :: " + taskName + " #################################################")
        predict_clf = Text_Classsifier()
        predict_clf.loadModel(modelFilePath)
        
        
        if not testDataFilePath == "" :
            test_data , df = predict_clf.loadTestDataFromFile(testDataFilePath, textFields, mask)
        else:
            test_data  = predict_clf.loadTestDataFromDataFrame(df, textFields , mask)
        
        
        predict = predict_clf.classify(test_data)
        
        if not mask:
            
            df[predictColName] = predict
            
        else:
            df.ix[ df[mask[0]]==mask[1], predictColName] = predict
            
       
        predictSpeed = len(predict) / (datetime.now() - predictStartTime).total_seconds()
        
        logging.info( str(datetime.now()) + " PREDICT SPEED :: " + str(predictSpeed)  + " articles/second." )
        logging.info( str(datetime.now()) + " ############## END PREDICT :: " + taskName + " #################################################")
        return df
    

    def performTrainingForAllTasks(self ):
        
        
        # Train phase
        # Task 1 RiskClassifier 
        self.performTraining(header.trainingFilePath, header.textFieldRiskClassifier, header.labelColNameRiskClassifier, header.riskClassifierModelFilePath , taskName="Risk Classifier")
        
        # Task 2   TopicClassifier
        #training file Consolidated_final.xlsx,
         
        self.performTraining(header.trainingFilePath, header.textFieldTopicClassifier, header.labelColNameTopicClassifier, header.topicClassifierModelFilePath , taskName="Topic Classifier")
        
        # Task 3 SubTopicClassifier 1
        # TODO Fetch unique values of sub topic and then create models for it.
         
        mask = [header.labelColNameTopicClassifier , 1]
        self.performTraining(header.trainingFilePath, header.textFieldTopicClassifier, header.labelColNameSubTopicClassifier, header.subTopicOneClassifierModelFilePath, mask , taskName="Sub Topic Classifier 1")
         
         
        # Task 4 SubTopicClassifier 2
         
        mask = [header.labelColNameTopicClassifier , 2]
        self.performTraining(header.trainingFilePath, header.textFieldTopicClassifier, header.labelColNameSubTopicClassifier, header.subTopicTwoClassifierModelFilePath, mask, taskName="Sub Topic Classifier 2")
         
         
        # Task 5 SubTopicClassifier 3
         
        mask = [header.labelColNameTopicClassifier , 3]
        self.performTraining(header.trainingFilePath, header.textFieldTopicClassifier, header.labelColNameSubTopicClassifier, header.subTopicThreeClassifierModelFilePath, mask , taskName="Sub Topic Classifier 3")
         
        
        # Task 5 SubTopicClassifier 4
        
        mask = [header.labelColNameTopicClassifier , 4]
        self.performTraining(header.trainingFilePath, header.textFieldTopicClassifier, header.labelColNameSubTopicClassifier, header.subTopicFourClassifierModelFilePath, mask , taskName="Sub Topic Classifier 4")
        
        
        
    def analyze(self):
        
        
        
        # TODO test if same df can be reused for multiple tasks of the predict phase
        # TODO Fetch text Fields and output file path from configuration file
        
        # Task 1 RiskClassifier
        dataFrame = self.initiateClassification( textFields=[ 'ArticleTitle' , 'Summary' ] , modelFilePath=header.riskClassifierModelFilePath , predictColName="riskClassifierPredict" , testDataFilePath=header.outputFilePath , taskName="Risk Classifier")
        
        #DEBUG Just to make the flow continue till end.
		
        dataFrame['riskClassifierPredict']=1
        
        # Task 2   TopicClassifier
        dataFrame = self.initiateClassification( textFields=['ArticleStory'], modelFilePath=header.topicClassifierModelFilePath, predictColName="topicClassifierPredict", df=dataFrame, mask=["riskClassifierPredict" , 1] , taskName="Topic Classifier")
         
             
         
        # Task 3 SubTopicClassifier 1
        dataFrame = self.initiateClassification( textFields=['ArticleStory'], modelFilePath=header.subTopicOneClassifierModelFilePath, predictColName="subTopicClassifierPredict", df=dataFrame, mask=["topicClassifierPredict" , 1] , taskName="Sub Topic Classifier 1 ")
      
        # Task 4 SubTopicClassifier 2
        dataFrame = self.initiateClassification( textFields=['ArticleStory'], modelFilePath=header.subTopicTwoClassifierModelFilePath, predictColName="subTopicClassifierPredict", df= dataFrame, mask=["topicClassifierPredict" , 2], taskName="Sub Topic Classifier 2")
         
         
        # Task 5 SubTopicClassifier 2
        dataFrame = self.initiateClassification( textFields=['ArticleStory'], modelFilePath=header.subTopicThreeClassifierModelFilePath, predictColName="subTopicClassifierPredict", df=dataFrame, mask=["topicClassifierPredict" , 3], taskName="Sub Topic Classifier 3")
         
         
        # Task 6 SubTopicClassifier 2
        dataFrame = self.initiateClassification( textFields=['ArticleStory'], modelFilePath=header.subTopicFourClassifierModelFilePath, predictColName="subTopicClassifierPredict", df=dataFrame, mask=["topicClassifierPredict" , 4], taskName="Sub Topic Classifier 4")
         
        dataFrame.to_csv("C:\Users\Jyoti.Gupta\Documents\crawler\AnalysisEngineOutput.csv" , header=True, encoding='latin-1')
  

if __name__ == '__main__':
    pass






