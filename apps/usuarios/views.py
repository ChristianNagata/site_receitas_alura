from django.http import request
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, AnonymousUser
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """Cadastra uma nova pessoa no sistema."""

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O campo "nome" não pode ficar em branco!')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(
                request, 'O campo "email" não pode ficar em branco!')
            return redirect('cadastro')

        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')

        if email_existe(email):
            messages.error(request, 'Este email já está sendo utilizado!')
            return redirect('cadastro')

        if username_existe(nome):
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')

        user = User.objects.create_user(
            username=nome, email=email, password=senha)
        user.save()

        messages.success(request, 'Usuário cadastrado com sucesso!')

        return redirect('login')

    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza a entrada de uma pessoa no sistema."""

    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        user = User.objects.get(email=email)

        email_existe = User.objects.filter(email=email).exists()

        if senha == '' or email == '':
            messages.error(
                request, 'Ambos os campos devem ser preenchidos!')
            return redirect('login')

        if email_existe:
            nome = User.objects.filter(email=email).values_list(
                'username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('dashboard')
        else:
            messages.error(
                request, 'O usuário não existe!')
            return redirect('login')

    return render(request, 'usuarios/login.html')


def logout(request):
    """Realiza a saída de uma pessoa no sistema."""

    auth.logout(request)
    return redirect('index')


def dashboard(request):
    """Mostra as receitas do usuário caso ele esteja cadastrado, caso não, mostra a página inicial."""

    if request.user.is_authenticated:
        id = request.user.id
        receita = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receita
        }

        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    return senha != senha2


def email_existe(email):
    return User.objects.filter(email=email).exists()


def username_existe(nome):
    return User.objects.filter(username=nome).exists()
