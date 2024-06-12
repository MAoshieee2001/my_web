import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from core.pos.forms import CompanyForm
from core.pos.mixins import ValidatePermissionRequiredMixin
from core.pos.models import Company


class CompanyUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Company  # Hacemos referencia a nuestro modelo
    form_class = CompanyForm  # Hacemos referencia a nuestro formClass
    template_name = 'company/create.html'  # Hacemos referencia a nuestro template name
    permission_required = 'change_company'  # Le damos los permisos que va a solicitar
    success_url = reverse_lazy('dashboard')  # Url redirectt que permite enviar si sse cumplio correctamente

    def get_object(self, queryset=None):  # El metodo get object permite devolver el objecto en si, referente asu key, sin embargo, lo estamos modificando
        company = Company.objects.first()
        return company if company else Company()

    def dispatch(self, request, *args, **kwargs):  # Permite redirecionar dependiendo la peticion que le estemos mandao
        self.object = self.get_object()
        return super(CompanyUpdateView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs): # Peticion POST, podemos hacemos el tema de la actualizacion
        data = {}
        try:
            action = request.POST['action']
            if action == 'update':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado ninguna opción.'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):  # Mandamos un diccionario con toda la información, que va a cargar nuestra pagina
        context = super(CompanyUpdateView, self).get_context_data(**kwargs)  # Como estamos sobreescribiendo nuestro context, es importante tenerlo
        context['title'] = 'Editar mi compañia'  # Mandalos un titulo
        context['entity'] = 'Compañia'  # Mandamoss el nombre de la entidad
        context['action'] = 'update'  # Mandamos la acción
        context['list_url'] = self.success_url  # Mandamos la lista url
        return context
