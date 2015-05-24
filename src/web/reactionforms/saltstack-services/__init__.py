######################################################################
# Cloud Routes Web Application
# -------------------------------------------------------------------
# SaltStack Services Reaction - Forms Class
######################################################################

from wtforms import TextField, SelectField
from wtforms.validators import DataRequired, URL
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates a Saltstack Reaction form for the dashboard '''

    function_choices = [
        ("reload", "Reload"),
        ("restart", "Restart"),
        ("start", "Start"),
        ("stop", "Stop")
    ]

    matcher_choices = [
        ("glob", "Hostname Glob"),
        ("pcre", "Hostname PCRE"),
        ("list", "List"),
        ("grain", "Grains"),
        ("grain_pcre", "Grains PCRE"),
        ("pillar", "Pillar"),
        ("nodegroup", "NodeGroup"),
        ("ipcidr", "IP Address/CIDR"),
        ("compound", "Compound")
    ]

    url = TextField(
        "URL",
        validators=[URL(message='URL must be in an appropriate format')])
    secretkey = TextField(
        "Secret Key",
        validators=[DataRequired(message='Secret Key is a required field')])
    function = SelectField(
        "Function", choices=function_choices,
        validators=[DataRequired(message='Function is a required field')])
    tgt = TextField(
        "Target",
        validators=[DataRequired(message='Target is a required field')])
    matcher = SelectField(
        "Matcher",
        choices=matcher_choices,
        validators=[DataRequired(message='Matcher is a required field')])
    args = TextField(
        "Service",
        validators=[DataRequired(message='Service is a required field')])
    call_on = SelectField(
        "Call On",
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call On is a required field')])

if __name__ == '__main__':
    pass
