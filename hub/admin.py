from django.contrib import admin
from .models import CashFlowModel, Document, Run

admin.site.register(CashFlowModel)
admin.site.register(Document)
admin.site.register(Run)
