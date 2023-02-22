'''
This python file provides exception handling code for data pipeline 
'''
import sys

def error_message_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info()

    filename = exc_tb.tb_frame.f_code.co_filename

    error_message = 'Error occured python script name [{0}] line number [{1}] error message [{2}]'.format(
        filename, exc_tb.tb_lineno, str(error))
    return error_message

# Used  this function to load the error if error occurs 
class SensorException(Exception):
    def __init__(self, error_message, error_detail:sys):
        '''
        :param error message: error message in string format
        '''
        # super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail= error_detail)
# Init function cannot return anything hence this __str__ function is used to return error msg
    def __str__(self):
        return self.error_message