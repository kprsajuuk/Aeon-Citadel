from django import forms


class ActionForm(forms.Form):
    act_name = forms.CharField(label="行动名", max_length=128)
    act_detail = forms.CharField(label="行动详情", max_length=128)


class EventForm(forms.Form):
    message = forms.CharField(label="描述", max_length=128)
