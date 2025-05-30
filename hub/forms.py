from django import forms
from .models import CashFlowModel, Document, Machine, Run


class CashFlowModelForm(forms.ModelForm):
    class Meta:
        model = CashFlowModel
        fields = '__all__'


class RunForm(forms.ModelForm):
    class Meta:
        model = Run
        fields = ['cash_flow_model', 'version']


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'
