from django import forms


class AvatarForm(forms.Form):
    name = forms.CharField(label="名称", max_length=128)
    attack = forms.CharField(label="攻", max_length=128)
    defense = forms.CharField(label="守", max_length=128)
    speed = forms.CharField(label="速", max_length=128)
    comment = forms.CharField(label="备注", max_length=128)


