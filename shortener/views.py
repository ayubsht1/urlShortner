import qrcode
from io import BytesIO
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from .models import ShortURL
from .forms import ShortURLForm
from .utils import generate_short_key
from django.http import JsonResponse
from django.db.models import F

class DashboardView(LoginRequiredMixin, ListView):
    model = ShortURL
    template_name = 'shortener/dashboard.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)
    
class CreateShortURLView(LoginRequiredMixin, CreateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = 'shortener/create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        custom_key = form.cleaned_data.get('custom_key')
        form.instance.user = self.request.user

        if custom_key:
            if ShortURL.objects.filter(short_key=custom_key).exists():
                form.add_error('custom_key', 'Key already exists')
                return self.form_invalid(form)
            form.instance.short_key = custom_key
        else:
            form.instance.short_key = generate_short_key()

        return super().form_valid(form)
    

class UpdateShortURLView(LoginRequiredMixin, UpdateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = 'shortener/edit.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        # Only allow owner to edit
        return ShortURL.objects.filter(user=self.request.user)

    def form_valid(self, form):
        custom_key = form.cleaned_data.get('custom_key')

        if custom_key:
            exists = ShortURL.objects.filter(short_key=custom_key).exclude(pk=self.object.pk)
            if exists.exists():
                form.add_error('custom_key', 'This key already exists')
                return self.form_invalid(form)

            self.object.short_key = custom_key

        return super().form_valid(form)
    
class QRCodeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        short_url = get_object_or_404(
            ShortURL,
            pk=pk,
            user=request.user
        )

        short_link = request.build_absolute_uri(
            f"/r/{short_url.short_key}/"
        )

        qr = qrcode.make(short_link)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(
            buffer.getvalue(),
            content_type="image/png"
        )
    
class QRPreviewView(LoginRequiredMixin, DetailView):
    model = ShortURL
    template_name = 'shortener/qr.html'

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)
    
class RedirectURLView(View):
    def get(self, request, key):
        short = get_object_or_404(ShortURL, short_key=key)

        if short.is_expired():
            raise Http404("Link expired")

        short.clicks += 1
        short.save()

        return redirect(short.original_url)
    
class DeleteShortURLView(LoginRequiredMixin, DeleteView):
    model = ShortURL
    template_name = 'shortener/confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return ShortURL.objects.filter(user=self.request.user)