from Remilia.utils.cli.prompts import Choice


class ChoiceBuilder:
    @staticmethod
    def fromdata(name:str,data) -> Choice:
        return Choice(name,data)