from django.shortcuts import render, redirect
from django.views.generic import View
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from web_learn.utils import normalize, product_vectorizer, product_matriz, recomender, system_recomend
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
            prod_series = pd.Series(document_in_text)
            prod_matriz = product_vectorizer.transform(prod_series)
            producto = cosine_similarity(prod_matriz, product_matriz, True)
            producto_serie = pd.Series(producto[0])
            system_recomend['product_name'] = producto_serie
            product_final = system_recomend.sort_values('product_name', ascending=False)
            for r in product_final.index:
                if product_final["product_name"][r]>=0.1:
                    ProductRecomender.objects.create(
                        producto=instance,
                        position=product_final["product_name"][r],
                    )
            return redirect('respuesta', id=instance.id)
        else:
            return redirect('index')
    

class ResultView(View):
    
    def get(self, request, id):
        instance = Producto.objects.get(id = id)
        matches = ProductRecomender.objects.filter(producto = instance,).all()
        #recomender_product = matches

        return render(request, "respuesta.html", {"matches": matches})