from wtforms import fields, validators
from user import User

# Added for PrintingForm
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

import cups


class PrintingForm(FlaskForm):
    pagerange = fields.TextField()
    side = fields.RadioField('Label', choices=[('A','one-sided'),('B','two-sided')])
    numberup = fields.SelectField('Label', choices = [(1, 1), (2, 2), (4, 4), (8, 8), (16, 16)])

    conn = cups.Connection()
    printers = conn.getPrinters()
    printername = []
    for printer in printers:
        printername.append((printer, printer))

    printer = fields.SelectField('Printer', choices = printername)

#    inputfile = FileField(validators=[FileRequired()])

    # check if the pagerange syntax is valid
    def valid_pagerange(self, data):
        

        # True if empty
        if "".join(data.split()) == "":
            return True

        # False if contains other strings
        #if any((c in set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_+=;:?/.><\'\"|[]\{\}\\')) for c in data):
        #    return False
        rangelist = data.split(",")
        for substr in rangelist:
            if '-' in substr:
                ran = substr.split("-")
                if not len(ran) == 2:
                    return False

                try:
                    int(ran[0])
                    int(ran[1])
                except:
                    return False

                if int(ran[0]) > int(ran[1]) or int(ran[0]) < 1:
                    return False

            else:
                try:
                    int(substr)
                except:
                    return False
                if int(substr) < 1:
                    return False

        return True

    def validate(self):

        if not self.valid_pagerange("".join(self.pagerange.data.encode('ascii', 'ignore').split()) ) == True:
            return False

        return True
    


# Define login and registration forms (for flask-login)
class LoginForm(FlaskForm):
    username = fields.TextField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate(self):
        user = self.get_user()

        if user is None:
            return False
            #raise validators.ValidationError('Invalid user')

        if user.password != self.password.data:
            return False
            #raise validators.ValidationError('Invalid password')

        return True

    def get_user(self):
        return User.get(self.username.data)
