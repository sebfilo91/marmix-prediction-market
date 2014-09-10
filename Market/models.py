from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import User

from django.db import models, connection


class Alert(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=6, max_digits=15)
    description = models.CharField(max_length=512, blank=True)
    claim = models.ForeignKey('Claim', db_column='num_alert_claim')
    trader = models.ForeignKey('Trader', db_column='num_alert_trader')
    class Meta:
        db_table = 'alert'

class Claim(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024)
    min_value = models.DecimalField(max_digits=15, decimal_places=6)
    max_value = models.DecimalField(max_digits=15, decimal_places=6)
    end_value = models.DecimalField(max_digits=15, decimal_places=6)
    price = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    ticks = models.DecimalField(max_digits=15, decimal_places=6)
    end_date = models.DateTimeField(blank=True, null=True)
    create_date = models.DateTimeField(default=datetime.now)
    ipo_date = models.DateTimeField(blank=True, null=True)
    description = models.CharField(max_length=255)
    success_condition = models.CharField(max_length=255)
    special_condition = models.CharField(blank=True, max_length=255)
    currency = models.ForeignKey('Currency', db_column='num_claim_currency')
    type = models.ForeignKey('ClaimType', db_column='num_claim_type')
    status = models.ForeignKey('ClaimStatus', db_column='num_claim_status')
    class Meta:
        db_table = 'claim'


class ClaimHistory(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now)
    price = models.DecimalField(max_digits=15, decimal_places=6)
    claim = models.ForeignKey(Claim, db_column='num_claim_history_claim')
    class Meta:
        db_table = 'claim_history'

class ClaimType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'claimtype'

class ClaimStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'claimstatus'

class Configuration(models.Model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    class Meta:
        db_table = 'configuration'

class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.symbol
    class Meta:
        db_table = 'currency'

class Exchange(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.now)
    rate = models.DecimalField(decimal_places=6, max_digits=15)
    currency_src = models.ForeignKey(Currency, db_column='num_currency_src',related_name="exchange_src")
    currency_dest = models.ForeignKey(Currency,db_column='num_currency_dest',related_name="exchange_dest")
    class Meta:
        db_table = 'exchange'

class Help(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.CharField(max_length=255, blank=True)
    html_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=1024)
    type = models.ForeignKey('HelpType', db_column='num_help_type')
    class Meta:
        db_table = 'help'

class HelpType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'helptype'

class Holding(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    price = models.DecimalField(decimal_places=6, max_digits=15)
    claim = models.ForeignKey(Claim, db_column='num_holding_claim')
    trader = models.ForeignKey('Trader', db_column='num_holding_trader')
    class Meta:
        db_table = 'holding'

class MarketMaker(models.Model):
    claim = models.ForeignKey(Claim, db_column='num_marketmaker_claim')
    trader = models.ForeignKey('Trader', db_column='num_marketmaker_trader')
    quantity = models.IntegerField()
    class Meta:
        db_table = 'marketmaker'

class MarketOrder(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    min_price = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    max_price = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    date_sent = models.DateTimeField(default=datetime.now)
    date_expire = models.DateTimeField()
    filled = models.BooleanField()
    trader = models.ForeignKey('Trader', db_column='num_order_trader')
    claim = models.ForeignKey(Claim, db_column='num_order_claim')
    type = models.ForeignKey('OrderType', db_column='num_order_type')
    class Meta:
        db_table = 'marketorder'


class OrderType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'ordertype'

class MarketTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=6, max_digits=15)
    result = models.DecimalField(decimal_places=6, max_digits=15)
    date = models.DateTimeField(default=datetime.now)
    trader = models.ForeignKey('Trader', db_column='num_transaction_trader')
    currency = models.ForeignKey(Currency, db_column='num_transaction_currency')
    order = models.ForeignKey(MarketOrder, unique=True, db_column='num_transaction_order')
    class Meta:
        db_table = 'markettransaction'

class Reward(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1024)
    condition = models.CharField(max_length=1024)
    trader = models.ForeignKey('Trader', db_column='num_reward_trader')
    type = models.ForeignKey('RewardType', db_column='num_reward_type')
    class Meta:
        db_table = 'reward'


class RewardType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name
    class Meta:
        db_table = 'rewardtype'

class Trader(models.Model):
    id = models.AutoField(primary_key=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    zipcode = models.CharField(max_length=10)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    countrystate = models.CharField(max_length=255, blank=True)
    birthdate = models.DateTimeField(null=True, blank=True)
    cash = models.DecimalField(decimal_places=6, max_digits=15)
    user = models.OneToOneField(User,db_column='num_trader_user')
    currency = models.ForeignKey(Currency, db_column='num_trader_currency')
    class Meta:
        db_table = 'trader'

class UserAction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    device_type = models.CharField(max_length=4)
    type = models.CharField(max_length=4)
    user = models.ForeignKey(User, db_column='num_user_action_user')
    class Meta:
        db_table = 'user_action'

class UserComment(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1024)
    date_update = models.DateTimeField(default=datetime.now,null=True, blank=True)
    trader = models.ForeignKey(Trader, db_column='num_comment_trader')
    claim = models.ForeignKey(Claim, db_column='num_comment_claim')
    class Meta:
        db_table = 'usercomment'
