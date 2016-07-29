from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])


class NetworkForm(Form):
    nick = StringField('Nickname', [validators.Length(min=4, max=25)])
    hostname = StringField('Hostname', [validators.DataRequired()])
    port = StringField('Port', [validators.DataRequired()])
    network = StringField('Network Name', [validators.DataRequired()])
    realname = StringField('Real Name')


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
