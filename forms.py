from flask_wtf import FlaskForm
from jsondb import Jsondb
from wtforms.fields import StringField, SubmitField
from wtforms.widgets import TextArea

#Make a form with flask WTF
class Forms():
    def buildEditForm():
        jsondb = Jsondb()
        data = jsondb.get_data()
        class EditNotice(FlaskForm):
            brokenlabel = StringField('Broken Label', default=data["brokenlabel"])
            brokenhtml = StringField('Broken HTML', default=data["brokenhtml"], widget=TextArea())
            joinlabel = StringField('Join Label', default=data["joinlabel"])
            joinhtml = StringField('Join HTML', default=data["joinhtml"], widget=TextArea())
            listenlabel = StringField('Listen Label', default=data["listenlabel"])
            listenhtml = StringField('Listen HTML', default=data["listenhtml"], widget=TextArea())
            extralabel = StringField('Extra Label', default=data["extralabel"])
            extrahtml = StringField('Extra HTML', default=data["extrahtml"], widget=TextArea())
            welfarelabel = StringField('Welfare Label', default=data["welfarelabel"])
            welfarehtml = StringField('Welfare HTML', default=data["welfarehtml"], widget=TextArea())
            bannerlabel = StringField('Banner Label', default=data["bannerlabel"])
            meetinglabel = StringField('Meeting Label', default=data["meetinglabel"])
            meetinghtml = StringField('Meeting HTML', default=data["meetinghtml"], widget=TextArea())
            committeehtml = StringField('Committee HTML', default=data["committeehtml"], widget=TextArea())
            showlabel = StringField('Show Label', default=data["showlabel"])
            submit = SubmitField('Edit Noticeboard')
        return EditNotice()