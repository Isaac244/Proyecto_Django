from django.shortcuts import render, redirect
from django.views.generic import View

from web_learn.utils import  recomender
from web_learn.forms import DocumentForm
from web_learn.models import Producto, ProductRecomender

# Create your views here.
class IndexView(View):

    def get(self, request):
        form = DocumentForm()
        return render(request, "index.html", {"form": form})
    
    def post(self, request):
        form = DocumentForm(request.POST)
        if form.is_valid():
            instance = form.save()
            document_in_text = recomender(instance.prod)
            print(document_in_text)
            for r in document_in_text.index:
                #if product_final["product_name"][r]>=0.1:
                    ProductRecomender.objects.create(
                        producto=instance,
                        position=document_in_text[r],
                    )
            return redirect('respuesta', id=instance.id)
        else:
            return redirect('index')
    

class ResultView(View):
    
    def get(self, request, id):
        instance = Producto.objects.get(id = id)
        matches = ProductRecomender.objects.filter(producto = instance)#.all()

        return render(request, "respuesta.html", {"matches": matches})