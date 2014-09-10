#-*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from Market.models import Claim
from Market.serializers import ClaimSerializer, OrderSerializer
from Market.service import service
from Market.service.service import Service
from Market.forms import ClaimForm, OrderForm, TraderForm, UserForm
from django.utils.translation import ugettext as _
from django.utils.translation import pgettext, ungettext

##-------------------------------------------------
##
##  Vues associées aux templates
##
##  Les vues possèdent le même nom que les templates associées
##
##-------------------------------------------------

def home(request):
    new_claims = Service.getAllClaim()
    featured_claim = new_claims[0]
    hot_claims = Service.getAllClaim()
    help_titles = Service.getHelpTitleAsDict('home')
    help_descriptions = Service.getHelpDescriptionAsDict('home')
    return render(request, 'market/home.html', locals())


@permission_required('user.is_staff', login_url='login')
def dashboard_admin(request):
    return render(request, 'market/dashboard_admin.html')


@login_required(login_url='login')
def dashboard_user(request):
    performance_data = Service.getDataChartPerformance(request.user.trader)
    return render(request, 'market/dashboard_user.html', locals())


def leaderboard(request):
    trader_leaderboard = Service.getLeaderboard()
    return render(request, 'market/leaderboard.html', locals())


@login_required(login_url='login')
def order_create(request, claim_id):
    claim = Service.getClaimById(claim_id)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            Service.createOrder(order, claim, request.user.trader)
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'market/order_create.html', locals())


@login_required(login_url='login')
def portfolio(request):
    holdings = Service.getAllHolding(request.user.trader)
    help_titles = Service.getHelpTitleAsDict('home')
    help_descriptions = Service.getHelpDescriptionAsDict('home')
    waiting_orders = Service.getAllOrder(request.user.trader)
    return render(request, 'market/portfolio.html', locals())


def claim_info(request, id):
    claim = Service.getClaimById(id)
    return render(request, 'market/claim_info.html', locals())


def claims(request):
    claims = Service.getAllClaim()
    return render(request, 'market/claims.html', locals())


def rewards(request):
    return render(request, 'market/rewards.html')


@login_required(login_url='login')
def transaction_historic(request):
    return render(request, 'market/transaction_historic.html')


def signup(request):
    if request.method == 'POST':
        traderform = TraderForm(request.POST)
        userform = UserForm(request.POST)
        if traderform.is_valid() and userform.is_valid():
            trader = traderform.save(commit=False)
            user = userform.save(commit=False)
            Service.createTrader(trader, user)
            return render(request, 'market/home.html')
    else:
        traderform = TraderForm()
        userform = UserForm()
    return render(request, 'market/signup.html', locals())


@login_required(login_url='login')
def claim_create(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            Service.createClaim(claim)
            return redirect('home')
    else:
        form = ClaimForm()
    return render(request, 'market/claim_create.html', locals())


def historic(request):
    return render(request, 'market/historic.html', locals())

    ##-------------------------------------------------
    ##
    ##  Partie Web Services
    ##
    ##-------------------------------------------------


class ClaimList(APIView):
    """

        Classe REST Service ClaimDetail

        Contient les méthodes correspondantes aux méthodes HTTP

        URL : /claim

    """

    def get(self, request, format=None):
        claims = Service.getAllClaim()
        serializer = ClaimSerializer(claims, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClaimSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimDetail(APIView):
    """
        REST Service ClaimDetail

        Contient les méthodes correspondantes aux méthodes HTTP

        URL : /claim/id

    """

    def get(self, request, pk, format=None):
        Claim = Service.getClaimById(pk)
        serializer = ClaimSerializer(Claim)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Claim = Service.getClaimById(pk)
        serializer = ClaimSerializer(Claim, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        claim = Service.getClaimById(pk)
        Service.deleteClaim(claim)
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    """
        REST Service OrderDetail

        Contient les méthodes correspondantes aux méthodes HTTP

        URL : /order

    """

    def get(self, request, format=None):
        Orders = Service.getAllOrder()
        serializer = OrderSerializer(Orders, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    """
        REST Service OrderDetail

        Contient les méthodes correspondantes aux méthodes HTTP

        URL : /order/id

    """

    def get(self, request, pk, format=None):
        Order = Service.getOrderById(pk)
        serializer = OrderSerializer(Order)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Order = Service.getOrderById(pk)
        serializer = OrderSerializer(Order, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Order = Service.getOrderById(pk)
        Service.deleteOrder(Order)
        return Response(status=status.HTTP_204_NO_CONTENT)












