"""
Contains classes etc that might help in processing the text whicl will be
used for training and classification purposes
"""

class Pre_Processor(object):
    """
    A base class that conatins methodfs for pre processing.

    The constructor needs a "root" dir whose all files will be pre processes


    """

    def __init__(self, root, file_ids,
                 stop_words_removal = False,
                named_entity_removal = False,
                hypernom_substitution = False,
                 output_location):
        """
        :param root: the root ditecttory the needs to be pre processed
        """

        if stop_words_removal:
            self.remove_stop_words()

        if named_entity_removal:
            self.remove_named_entities()

        if hypernom_substitution:
            self.substitute_hypernom()
        return None

    def start(self):
        return None

    def remove_stop_words(self):
        return None

    def remove_named_entities(self):
        return None

    def substitute_hypernom(self):
        return None
