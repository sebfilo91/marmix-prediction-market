from rest_framework import serializers
from rest_framework.compat import User
from Market.models import Claim

__author__ = 'Sebastien'

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        #fields = ('id','name','minvalue','maxvalue','end_value','ticks','end_date','create_date','ipo_date','status',' type','description','success_condition','num_claim_currency')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim

class TraderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim