from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from Market.models import Claim, MarketOrder, Trader
from django.db import models


class ClaimForm(forms.ModelForm):
    """
        Formulaire de création d'une prédiction

        Utilisé par la vue "claim_create"
        Situé dans le template "claim_create.html"

    """
    ipo_date = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'datePicker', 'readonly': 'true'}))

    class Meta:
        model = Claim
        exclude = ('id', 'end_date', 'end_value', 'create_date', 'status', 'price')


class OrderForm(forms.ModelForm):
    """
        Formulaire de création d'une prédiction

        Utilisé par la vue "order_create"
        Situé dans le template "order_create.html"

    """
    date_expire = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'datePicker', 'readonly': 'true'}))

    class Meta:
        model = MarketOrder
        exclude = ('id', 'end_date', 'date_sent', 'trader', 'claim', 'filled')


class TraderForm(forms.ModelForm):
    """
        Formulaire de création d'un utilisateur

        Utilisé par la vue "signup"
        Situé dans le template "signup.html"

    """
    birthdate = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'datePicker', 'readonly': 'true'}))

    class Meta:
        model = Trader
        exclude = ('user', 'cash')


class UserForm(forms.ModelForm):
    """
        Formulaire de création d'un trader

        Utilisé par la vue "signup"
        Situé dans le template "signup.html"

    """

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
