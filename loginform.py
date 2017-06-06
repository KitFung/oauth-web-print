from wtforms import form, fields, validators
from user import User


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
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
