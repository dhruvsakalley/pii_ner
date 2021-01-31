import re

class RulesEngine():
    '''
    This class implements rule based NER, by pinning the text content in order to improve recognition.
    While it support pinning known labels, there is also support to pin text with unknown labels.
    '''

    def __init__(self):
        # pattern from https://emailregex.com/ General Email Regex (RFC 5322 Official Standard) converted to python
        self._email_pattern = re.compile(
            r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
            , re.IGNORECASE)

        # SSN pattern
        self._ssn_pattern = re.compile(r'''
            (\d{3}      # first 3 digits (e.g. '800')
            \D?         # optional separator is any number of non-digits
            \d{2}       # trunk is 2 digits (e.g. '55')
            \D?         # optional separator
            \d{4})      # rest of number is 4 digits (e.g. '1212')
        ''', re.VERBOSE)

        # 12, 13, 14, 15, 16, 19 digit credit cards
        self._creditcard_pattern = re.compile(r'''
            (
            \d{19}      # all 12 digits
            |           # OR
            \d{16}      # all 16 digits
            |           # OR
            \d{15}      # all 15 digits
            |           # OR
            \d{14}      # all 14 digits
            |           # OR
            \d{13}      # all 14 digits
            |           # OR
            \d{12}      # all 19 digits
            )
        ''', re.VERBOSE)

        # phones will also catch cc, so a phone check will be dependent on cc check
        self._phone_pattern = re.compile(r"([+,(]?(\d{3}|\d{1})?[-,(]?\d{3}\D?\D?\d{3}\D?\d{4}([ ]*(?:#|x\.?|ext\.?|extension)[ ]*(\d{5}|\d{4}|\d{3})?(?!\d{1}.*)|(?!\d{1}.*)))")

        # pin patterns
        self.pin_map = {
            "Email": (lambda subtext: f"eee {subtext} mmm"),
            "SSN": (lambda subtext: f"sss {subtext} nnn"),
            "Phone_number": (lambda subtext: f"ppp {subtext} hhh"),
            "CreditCardNumber": (lambda subtext: f"ccc {subtext} ccc"),
        }

    def pin_email(self, text):
        z = self._email_pattern.search(text)
        if z:
            return self._email_pattern.sub(self.pin_map["Email"](z.group()), text)
        else:
            return text

    def pin_ssn(self, text):
        z = self._ssn_pattern.search(text)
        if z:
            return self._ssn_pattern.sub(self.pin_map["SSN"](z.group()), text)
        else:
            return text

    def pin_phone(self, text):
        cc = self._creditcard_pattern.search(text)
        if cc:
            return text
        z = self._phone_pattern.search(text)
        if z:
            return self._phone_pattern.sub(self.pin_map["Phone_number"](z.group()), text)
        else:
            return text

    def pin_cc(self, text):
        z = self._creditcard_pattern.search(text)
        if z:
            return self._creditcard_pattern.sub(self.pin_map["CreditCardNumber"](z.group()), text)
        else:
            return text

    def pin_text(self, text):
        '''
        Mark a text input for known patterns (important: multually exclusive patterns)
        '''
        text_ = self.pin_email(text)
        if text_ == text:
            text_ = self.pin_phone(text)
            if text_ == text:
                text_ = self.pin_cc(text)
                if text_ == text:
                    text_ = self.pin_ssn(text)
        return text_


def unit_test():
    eng = RulesEngine()
    texts = [
        # email
        ("Town minute culture throughout business. Under stay occur hot. friley@zavala-griffith.com","email"),
        ("Radio respond perhaps western loss blood. Turn list economy itself executive indeed with. Final so environmental relationship jrodriguez@mccarthy-lawson.biz or arrive idea church. Fast exactly raise city push live benefit else.","email"),
        ("Approach article scene though respond white song. Pick PM even white still. Keep north martinvalerie@cruz-collins.com reflect away property standard.","email"),
        ("Cell town lowens@hotmail.com administration arm. Say range watch our shoulder as.","email"),
        # phone
        ("2536307050 Year not special must run since. Stuff their better of public good.","ph"),
        ("Add three Democrat deep 712-204-4405x2487 bill appear. Or box traditional majority. Analysis fly teacher court like president.","ph"),
        ("Feel thank whether threat spring third position. Away magazine whatever source answer ability. (477)402-2657 Election shoulder like student peace.","ph"),
        ("She late away 996-294-4022 line recent employee. Several past personal.","ph"),
        ("Nearly but foreign. Much value (789)017-0422 beat second poor feeling work. Then picture them water window.","ph"),
        ("Character film 001-753-147-3410 whole above operation player cause.","ph"),
        ("Drop yet bad +1-329-455-6695x335 each whose. Machine board size special care hear.","ph"),
        # ssn
        ("Question as should sign face. Memory 337-66-8906 approach month back.","ssn"),
        ("Sound improve parent dream 377 98 7558 send language. Hundred better down understand treatment able. Partner kid want feel action yeah.","ssn"),
        ("We trial win. Indeed hotel 211 72 2423 dream. Poor friend go east above.","ssn"),
        ("Series painting development simply 693 88 4776 good. Hour cultural so only group.","ssn"),
        ("Gun billion skin. Find success force state 211 72 2423 within.","ssn"),
        ("Wear language word kitchen might figure miss join. Large hear security year during reach watch. 211 72 2423","ssn"),
        ("Organization 877-42-6395 rich indicate medical everyone industry. Under word director value. Candidate help anything weight specific.","ssn"),
        ("Job security fall bad good relationship. List area away federal necessary. 587-05-0700 Wind all stage time animal.","ssn"),
        # credit card
        ("Director thousand manager give 4674473076627534 board white. Result how more southern. Fact guess to.","cc"),
        ("Report author increase a 4730553981548548163 receive watch. Book rather imagine. Decision hit result able store future development source.","cc"),
        ("Positive cause I arrive night site wind. Throughout mind over 2383084986841820 he collection hit. Fall challenge action through.","cc"),
        ("Store effort campaign girl worker technology. Fact reach somebody sense. Run run tonight soldier. World trade 676293890015 play account up single.","cc"),
        ("Coach he west magazine against beat. By 344984586232209 sometimes series time whole election prove. Series protect program may peace answer.","cc"),
        ("Speech national especially available own black alone. After friend religious 3563330148426475 unit movement not pretty all.","cc"),
    ]

    for t,c in texts:
        print("\n",t,"---")
        fmap = {
            "email":eng.pin_email,
            "ph":eng.pin_phone,
            "ssn":eng.pin_ssn,
            "cc":eng.pin_cc
        }
        print(t)
        print("+++" )
        print(fmap[c](t))
        print("\n")

if __name__ == "__main__":
    unit_test()