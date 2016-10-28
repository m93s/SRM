from crawler import Crawler
import header
import ConfigParser
import os.path
import logging 
import sys
from analysis_engine import Analysis_Engine





class Controller():

    settings = ConfigParser.ConfigParser()
    header = header.Header()

    def start(self):
        self.read_inputs()
        self.set_logger()

        if self.header.crawler_switch==1:
            self.run_crawler()
        if self.header.classifier_switch==1:
            self.run_classification_engine()

        return None

    def set_logger(self):

        if not os.path.isdir(self.header.log_dir):
            logging.warning("""LOG_DIR_PATH not set properly.
                            logs are redirected to log.txt placed at:"""
                            + self.header.home_dir)
            log_dir_path = self.header.home_dir



        LEVELS = {'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'warning': logging.WARNING,
                      'error': logging.ERROR,
                      'critical': logging.CRITICAL}

        try:

            level = LEVELS.get(self.header.level_name , logging.NOTSET)
            path = os.path.join(self.header.log_dir,self.header.log_file)

            logging.basicConfig(filename=path , level=level)

            if level == logging.NOTSET:
                logging.warning("""Logging level not set properly.
                                "Allowed levels are : critical , error ,
                                "warning , info , debug """)

        except Exception as e:
            print e.message
            return None

    def read_inputs(self):
        self.settings.read(self.header.settings_file)
        try:
            #Directories
            section = 'DIRECTORIES'
            self.header.home_dir = self.settings.get(section,
                                                'HOME_DIR')
            self.header.output_dir= self.settings.get(section,
                                             'OUTPUT_DIR')
            self.header.log_dir= self.settings.get(section,
                                                 'LOG_DIR')
            self.header.resource_dir= self.settings.get(section,
                                              'RESOURCE_DIR')


            #Crawler_Inputs
            section = 'CRAWLER_INPUTS'
            self.header.crawler_switch=self.settings.get(section,
                                                    'CRAWLER_SWITCH')
            self.header.crawler_switch=int(self.header.crawler_switch)

            self.header.site_info_file = self.settings.get(section,
                                                        'SITE_INFO_FILE')
            self.header.keyword_file = self.settings.get(section,
                                                       'KEYWORD_FILE')

            self.header.site_timestamp_pickle_file = self.settings.get(section,
                                                       'SITE_PICKLE_DUMP_FILE')

            self.header.crawler_output = self.settings.get(section,
                                                    'CRAWLER_OUTPUT')
            self.header.key_word_filering_switch=self.settings(
                section, 'KEY_WORD_FILTERING_SWITCH'
            )
            self.header.key_word_filering_switch=int(
                self.header.key_word_filering_switch
            )

            #Logging_Inputs
            section = 'LOGGING_INPUTS'
            self.header.log_file=self.settings.get(
                section,'LOG_FILE'
            )
            self.header.level_name = self.settings.get(
                section,'LEVEL_NAME'
            )



            #Classifier_Inputs
            section = 'CLASSIFIER_INPUTS'

            self.header.training_file = self.settings.get(
                                                    section,
                                                    'TRAINING_FILE_PATH')

            self.header.classifier_switch=self.settings.get(section,
                                                       'CLASSIFIER_SWITCH')
            self.header.classifier_switch=int(self.header.classifier_switch)

            self.header.label_col_name_risk_classifier = self.settings.get(
                                            section,
                                            'LABEL_COL_NAME_RISK_CLASSIFIER')

            self.header.text_field_risk_classifier = self.settings.get(
                                            section,
                                            'TEXT_FIELDS_RISK_CLASSIFIER')\
                                            .split(',')


            self.header.risk_classifier_model_file = self.settings.get(
                                        section,
                                        'RISK_CLASSIFIER_MODEL_FILE')

            self.header.text_field_topic_classifier = self.settings.get(
                                                section,
                                                'TEXT_FIELDS_TOPIC_CLASSIFIER'
                                                ).split(',')

            self.header.label_col_name_topic_classifier = self.settings.get(
                                            section,
                                            'LABEL_COL_NAME_TOPIC_CLASSIFIER')

            self.header.topic_classifier_model_file = self.settings.get(
                                            section,
                                            'TOPIC_CLASSIFIER_MODEL_FILE')

            self.header.label_col_name_sub_topic_classifier = self.settings.get(
                                        section,
                                        'LABEL_COL_NAME_SUB_TOPIC_CLASSIFIER' )

            self.header.risk_classifier_ratio_remove_skewness = float(
                                                        self.settings.get(
                                    section,
                                    'RISK_CLASSIFIER_RATIO_REMOVE_SKEWNESS' ))

            self.header.classifier_output=self.settings.get(section,
                                                       'CLASSIFIER_OUTPUT')

            if "true" in (self.settings.get(section ,'IS_REMOVE_SKEWNESS')).lower():
                self.header.isRemoveSkewness = True

        except Exception as e:
            print e.message


        return None





    def run_classification_engine(self):
        analyzer = Analysis_Engine(self.header)
        analyzer.performTrainingForAllTasks()
        analyzer.analyze()
        return None

    def run_crawler(self):
        crawler = Crawler(self.header)
        return None


if __name__ == '__main__':
    Controller().start()
