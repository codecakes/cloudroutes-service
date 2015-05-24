######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# Reaction - Forms Class
######################################################################

from wtforms import Form
from wtforms import TextField, PasswordField, SelectField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, Length, Required, URL
from wtforms.validators import IPAddress, NumberRange, EqualTo
from ..base import BaseReactForm

class ReactForm(BaseReactForm):
    ''' Class that creates a Reaction form for the dashboard '''

    apikey = TextField("API Key", validators=[DataRequired(message='API Key is a required field')])
    appname = TextField("Application Name", validators=[DataRequired(message='Application Name is a required field')])
    call_on = SelectField("Call On", choices=[('false', 'False Monitors'), ('true', 'True Monitors')], validators=[DataRequired(message='Call On is a required field')])

    dyno_type = TextField("Dyno Type", validators=[DataRequired(message='Dyno Type is a required field')])
    min_size = SelectField("Minimum Size", choices=[( '1', '1X'), ( '2', '2X'), ( '3', 'PX')], validators=[DataRequired(message='Minimum Size is a required field')])


if __name__ == '__main__':
    pass
