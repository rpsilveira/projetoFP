from django.shortcuts import render, HttpResponseRedirect
from django.db.models import Q 
from caixas.models import Caixas

def index(request):
    return render(request, 'index.html')

def caixaListar(request):
    caixas = Caixas.objects.all()[0:10]

    return render(request, 'caixas/listaCaixas.html', {'caixas': caixas})


def caixaAdicionar(request):
    return render(request, 'caixas/formCaixas.html')

def caixaSalvar(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '0')

        try:
            caixa = Caixas.objects.get(pk=codigo)
        except:
            caixa = Caixas()

        caixa.pessoa_id = request.POST.get('pessoa_id', '')
        caixa.tipo = request.POST.get('tipo', '')
        caixa.descricao = request.POST.get('descricao', '')
        caixa.valor = request.POST.get('valor', '')
        caixa.pagseguro = request.POST.get('pagseguro', '')
        caixa.data = request.POST.get('data', '00/00/0000')

        caixa.save()
    return HttpResponseRedirect('/caixas/')

def caixaPesquisar(request):
    if request.method == 'POST':
        textoBusca = request.POST.get('textoBusca', 'TUDO')

        try:
            if textoBusca == 'TUDO':
                caixas = Caixas.objects.all()
            else: 
                caixas = Caixas.objects.filter(
                    (Q(tipo__contains=textoBusca) |  
                    Q(descricao__contains=textoBusca) | 
                    Q(valor__contains=textoBusca) | 
                    Q(pagseguro__contains=textoBusca) | 
                    Q(data__contains=textoBusca))).order_by('-descricao')
        except:
            caixas = []

        return render(request, 'caixas/listaCaixas.html', {'caixas': caixas, 'textoBusca': textoBusca})

def caixaEditar(request, pk=0):
    try:
        caixa = Caixas.objects.get(pk=pk)
    except:
        return HttpResponseRedirect('/caixas/')

    return render(request, 'caixas/formCaixas.html', {'caixa': caixa})

def caixaExcluir(request, pk=0):
    try:
        caixa = Caixas.objects.get(pk=pk)
        caixa.delete()
        return HttpResponseRedirect('/caixas/')
    except:
        return HttpResponseRedirect('/caixas/')
