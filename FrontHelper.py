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

# print(FrontHelper.dictionaryToInfostring({"1":2, "2": "NULL", "3": None}))