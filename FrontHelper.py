class FrontHelper:
    """[summary]
    """
    @staticmethod
    def othersToPrintableString(input) -> str:
        """[summary]

        Args:
            input ([type]): [description]

        Returns:
            str: [description]
        """
        if type(input) is str:
            return input
        elif input is None:
            return ""
        else:
            return str(input)
    
    @staticmethod
    def dictionaryToInfostring(toPack:dict) -> str:
        """This function transforms a dictionary of values into a packed string

        Args:
            toPack (dict): [description]

        Returns:
            str: [description]
        """
        output = ""
        for attribute in toPack.keys():
            output += str(attribute)
            output += ": "
            output += FrontHelper.othersToPrintableString(toPack.get(attribute, ""))
            output += "\n"
        if output[-1] == "\n":
            output = output[0:-1]
        return output

    @staticmethod
    def isValidString(input) -> bool:
        """return if a string is valid as user input

        Args:
            input ([type]): [description]

        Returns:
            bool: [description]
        """
        if input is None:
            return False
        elif type(input) is not str:
            return False
        else:
            return input.isalnum()
    
    @staticmethod
    def genderToString(gender):
        formattedGender = None
        if type(gender) is str:
            try:
                formattedGender = int(gender)
            except BaseException:
                return "Error"
        formattedGender = gender
        if formattedGender == 0:
            return "Male"
        elif formattedGender == 1:
            return "Female"
        elif formattedGender == 2:
            return "Others"
        else:
            return "Error"

    @staticmethod
    def StringToGender(genderText) -> int:
        if type(genderText) is not str:
            return 3
        genderText = genderText.lower()
        if genderText == "male":
            return 0
        elif genderText == "female":
            return 1
        elif genderText == "others":
            return 2
        else:
            return 3

    @staticmethod
    def StringToIsPublic(ispublicText) -> int:
        if type(ispublicText) is not str:
            return 0
        ispublicText = ispublicText.lower()
        if ispublicText == "public":
            return 1
        else:
            return 0

    @staticmethod
    def ispublicToString(ispublic) -> str:
        formattedIspublic = None
        if type(ispublic) is str:
            try:
                formattedIspublic = int(ispublic)
            except BaseException:
                return "Error"
        formattedIspublic = ispublic
        if formattedIspublic == 0:
            return "Private"
        elif formattedIspublic == 1:
            return "Public"
        else:
            return "Error"