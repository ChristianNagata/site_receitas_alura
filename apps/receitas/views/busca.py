from receitas.models import Receita
from django.shortcuts import render, redirect


def busca(request):
    lista_receitas = Receita.objects.order_by(
        '-data_receita').filter(publicada=True)

    if 'search' in request.GET:
        nome_a_buscar = request.GET['search']
        lista_receitas = lista_receitas.filter(
            nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas': lista_receitas
    }

    return render(request, 'receitas/buscar.html', dados)
