import logging 
import logging.handlers
from fileinput import filename


class Header():

    #Defaults
    settings_file="../resources/Settings.config"

    #Directories
    home_dir=""
    log_dir=""
    output_dir=""
    resource_dir=""


    #Crawler_Inputs
    crawler_switch=""
    site_info_file = ""
    keyword_file= ""
    site_timestamp_pickle_file = ""
    crawler_output=""
    key_word_filering_switch=""


    #Logging_Inputs
    log_file = ""
    level_name = ""

    #Classifier_Inputs
    classifier_switch=""
    training_file = ""
    label_col_name_risk_classifier = ""
    text_field_risk_classifier = ""
    risk_classifier_model_file=""
    text_field_topic_classifier=""
    label_col_name_topic_classifier=""
    topic_classifier_model_file=""
    label_col_name_sub_topic_classifier=""
    is_param_tune=False
    is_remove_skewness=False
    risk_classifier_ratio_remove_skewness=1
    classifier_output=""

















