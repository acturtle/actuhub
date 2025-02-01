from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from queue import Queue
from threading import Thread

from .forms import CashFlowModelForm, DocumentForm, RunForm
from .models import CashFlowModel, Document, Run
from .utils import process_run

RUN_QUEUE = Queue()


def process_run_queue():
    while True:
        run = RUN_QUEUE.get()
        process_run(run)
        RUN_QUEUE.task_done()


worker_thread = Thread(target=process_run_queue, daemon=True)
worker_thread.start()


class ModelListView(ListView):
    model = CashFlowModel
    template_name = 'model_list.html'
    context_object_name = 'models'
    ordering = ['-id']


class ModelCreateView(CreateView):
    model = CashFlowModel
    form_class = CashFlowModelForm
    template_name = 'model_add.html'
    success_url = reverse_lazy('model_list')


class ModelDetailView(DetailView):
    model = CashFlowModel
    template_name = 'model_detail.html'
    context_object_name = 'model'


class ModelUpdateView(UpdateView):
    model = CashFlowModel
    form_class = CashFlowModelForm
    template_name = 'model_edit.html'
    success_url = reverse_lazy('model_list')


class ModelDeleteView(DeleteView):
    model = CashFlowModel
    template_name = 'model_delete.html'
    success_url = reverse_lazy('model_list')


class RunListView(ListView):
    model = Run
    template_name = 'run_list.html'
    context_object_name = 'runs'
    ordering = ['-id']


class RunCreateView(CreateView):
    model = Run
    form_class = RunForm
    template_name = 'run_add.html'
    success_url = reverse_lazy('run_list')

    def form_valid(self, form):
        run = form.save()
        RUN_QUEUE.put(run)
        return redirect(self.success_url)


class RunDetailView(DetailView):
    model = Run
    template_name = 'run_detail.html'
    context_object_name = 'run'


class RunDeleteView(DeleteView):
    model = Run
    template_name = 'run_delete.html'
    success_url = reverse_lazy('run_list')


class DocumentListView(ListView):
    model = Document
    template_name = 'document_list.html'
    context_object_name = 'documents'


class DocumentCreateView(CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'document_add.html'
    success_url = reverse_lazy('document_list')


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document_detail.html'
    context_object_name = 'document'


class DocumentUpdateView(UpdateView):
    model = Document
    template_name = 'document_edit.html'
    fields = ['name', 'file', 'cash_flow_models']
    success_url = reverse_lazy('document_list')


class DocumentDeleteView(DeleteView):
    model = Document
    template_name = 'document_delete.html'
    success_url = reverse_lazy('document_list')


@csrf_exempt
def get_runs_status(request):
    runs = Run.objects.all().values('id', 'status', 'cash_flow_model__name', 'cash_flow_model__id', 'version')
    return JsonResponse({'runs': list(runs)})
