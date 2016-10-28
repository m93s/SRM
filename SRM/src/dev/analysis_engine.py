from text_classifier import Text_Classsifier
import pandas as pd
import header
import logging
from datetime import datetime
import os

class Analysis_Engine():
    
    
    def __init__(self,header):
        self.header = header
        return
    
    def performTraining(self , trainingFilePath , textFields ,
            labelColName , modelFilePath  , mask=[] , taskName=""
        ):
        """
        Trains a classifier, given the training data details are provided

        :param trainingFilePath:
        :param textFields:
        :param labelColName:
        :param modelFilePath:
        :param mask:
        :param taskName:
        :return:
        """
        training_start_time = datetime.now()
        logging.info(str(training_start_time) + "START TRAINING :: " + taskName
        )

        clf = Text_Classsifier()
        clf.loadTrainingData(trainingFilePath, textFields,
        labelColName, mask
        )
        
        # For task 1, make the proportion of risky vs non risky moderate
        # enough to strengthen the model.
        if( (taskName == "Risk Classifier") & self.header.isRemoveSkewness):
            ratio=self.header.riskClassifierRatioRemoveSkewness
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

        trainingSpeed =  len(clf.text) / (
            datetime.now() - training_start_time).total_seconds()

        logging.info( str(datetime.now())
            + " TRAINING SPEED :: " + str(trainingSpeed)

            + " articles per second." )

        logging.info( str(datetime.now()) + " END TRAINING :: " + taskName )
        
    def initiateClassification(self  , textFields , modelFilePath ,
            predictColName , testDataFilePath="" , df=pd.DataFrame(),
            mask=[] , taskName=""):
        predictStartTime = datetime.now()
        logging.info( str(predictStartTime)
            + "START PREDICTION :: " + taskName )

        predict_clf = Text_Classsifier()
        predict_clf.loadModel(modelFilePath)
        
        
        if not testDataFilePath == "" :
            test_data , df = predict_clf.loadTestDataFromFile(testDataFilePath,
                                                              textFields, mask)
        else:
            test_data  = predict_clf.loadTestDataFromDataFrame(df,
                                                            textFields , mask)
        
        
        predict = predict_clf.classify(test_data)
        
        if not mask:
            
            df[predictColName] = predict
            
        else:
            df.ix[ df[mask[0]]==mask[1], predictColName] = predict
            
       
        predictSpeed = len(predict) / (datetime.now()
                                       - predictStartTime).total_seconds()
        
        logging.info( str(datetime.now()) + " PREDICT SPEED :: "
                      + str(predictSpeed)  + " articles/second." )

        logging.info( str(datetime.now()) + " END PREDICTION :: " + taskName )
        return df
    

    def performTrainingForAllTasks(self ):
        
        
        # Train phase
        # Task 1 RiskClassifier 
        self.performTraining(self.header.training_file,
                             self.header.text_field_risk_classifier,
                             self.header.label_col_name_risk_classifier,
                             self.header.risk_classifier_model_file ,
                             taskName="Risk Classifier")
        
        # Task 2   TopicClassifier
        #training file Consolidated_final.xlsx,
         
        self.performTraining(self.header.training_file,
                             self.header.text_field_topic_classifier,
                             self.header.label_col_name_topic_classifier,
                             self.header.topic_classifier_model_file ,
                             taskName="Topic Classifier")

        
        
    def analyze(self):
        
        # Task 1 RiskClassifier
        dataFrame = self.initiateClassification(
                    textFields=[ 'ArticleTitle', 'Summary'],
                    modelFilePath=self.header.riskClassifierModelFilePath,
                    predictColName="riskClassifierPredict",
                    testDataFilePath=self.header.outputFilePath,
                    taskName="Risk Classifier")
        
        #DEBUG Just to make the flow continue till end.
        dataFrame['riskClassifierPredict'] = 1
        
        # Task 2   TopicClassifier
        dataFrame = self.initiateClassification(
                        textFields=['ArticleStory'],
                        modelFilePath=self.header.topicClassifierModelFilePath,
                        predictColName="topicClassifierPredict",
                        df=dataFrame,
                        mask=["riskClassifierPredict", 1],
                        taskName="Topic Classifier")
         
             
         
        path = os.path.join(self.header.output_dir, self.header.outputFilePath)
        dataFrame.to_csv(path,
                         header=True,
                         encoding='latin-1')
  






