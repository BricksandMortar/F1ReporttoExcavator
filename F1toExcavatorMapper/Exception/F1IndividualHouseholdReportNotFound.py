from F1toExcavatorMapper.Exception import MappingFileNotFound


class F1IndividualHouseholdReportNotFound(MappingFileNotFound):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
