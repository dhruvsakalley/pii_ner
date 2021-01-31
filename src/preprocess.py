import pandas as pd
from difflib import SequenceMatcher
import re
import rules

class CoNLLConverter():
    '''
    This class is used for shaping the given data and tokenizing it into CoNLL format.
    The objective is to make it compatible with flair input format.
    '''
    def __init__(self):
        self.engine = rules.RulesEngine()

    def matcher(self, string: str, pattern):
        '''
        Return the start and end index of any pattern present in the text.
        '''
        match_list = []
        pattern = pattern.strip()
        seqMatch = SequenceMatcher(None, string, pattern, autojunk=False)
        match = seqMatch.find_longest_match(0, len(string), 0, len(pattern))

        if (match.size == len(pattern)):
            start = match.a
            end = match.a + match.size
            match_tup = (start, end)
            match_list.append(match_tup)

        return match_list

    def mark_sentence(self, s: str, match_list: list, negative=False):
        '''
        Marks all the entities in the sentence as per the BIO scheme.
        '''
        word_dict = {}
        for word in s.split():
            word_dict[word] = 'O'

        # Skip the None class label
        if not negative:
            for start, end, e_type in match_list:
                temp_str = s[start:end]
                tmp_list = temp_str.split()
                if len(tmp_list) > 1:
                    word_dict[tmp_list[0]] = 'B-' + e_type
                    for w in tmp_list[1:]:
                        word_dict[w] = 'I-' + e_type
                else:
                    word_dict[temp_str] = 'B-' + e_type
        return word_dict


    def bio_tagger(self, text, label, entity):
        '''
        Tag a single sentence into BIO scheme per the provided label and entity
        '''
        tagged_data = []
        entity = str(entity).strip().replace('@',' @ ')

        # These are the rule bases entities that have been pinned already, which requires special markup
        if entity and label and label in ["Email", "SSN", "Phone_number", "CreditCardNumber"]:
            # entity = self.engine.pin_map[label](entity)
            text = self.engine.pin_text(text).replace('@',' @ ')

        if label == "None":
            #negative samples
            d = self.mark_sentence(text, None, negative=True)
            for i in d.keys():
                tagged_data.append(i + ' ' + d[i] +'\n')
            tagged_data.append('\n')
        else:

            match_list = []
            a = self.matcher(text, entity)
            match_list = [(a[0][0], a[0][1], label)]
            d = self.mark_sentence(text, match_list)
            for i in d.keys():
                tagged_data.append(i + ' ' + d[i] +'\n')
            tagged_data.append('\n')

        return tagged_data