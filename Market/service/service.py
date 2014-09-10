from Market.models import *
from datetime import datetime

class Service:
    ##-------------------------------------------------
    ##
    ##  Méthodes de création
    ##
    ##-------------------------------------------------
    @staticmethod
    def createTrader(trader,user):
        """ Méthode permettant la création d'un trader """
        trader.cash = 20000
        user.set_password(user.password)
        user.save()
        trader.user = user
        trader.save()

    @staticmethod
    def createClaim(claim):
        """
        Méthode permettant la création d'une prédiction
        """
        claim.end_date = datetime.now()
        claim.create_date = datetime.now()
        claim.ipo_date = datetime.now()
        ##claim.status = ClaimStatus.objects.get(name="CREATED")
        ## procédure d'IPO, mais pas encore implémenté alors la prédiction passe direct en actif
        claim.status = ClaimStatus.objects.get(name="RUNNING")
        claim.save()

    @staticmethod
    def createOrder(order,claim,trader):
        """ Méthode permettant la création d'ordre à l'aide d'une prédiction et d'un trader """
        if claim.status == ClaimStatus.objects.get(name="RUNNING"):
            order.date_sent = datetime.now()
            order.create_date = datetime.now()
            order.date_expire = datetime.now()
            order.trader = trader
            order.claimclaim = claim
            order.filled = False
            order.save()
            Service.processOrder(order)

    @staticmethod
    def createHolding(transaction,claim):
        """ Méthode de création d'une holding en utilisant une transaction et une prédiction"""

        holding = Holding()
        holding.date = datetime.now()
        holding.quantity = transaction.quantity
        holding.price = transaction.price
        holding.claim = claim
        holding.trader = transaction.trader
        holding.save()

    @staticmethod
    def createTransaction(order,currency):
        """ Méthode de création d'une transaction """
        transaction = MarketTransaction()
        transaction.order=order
        transaction.trader=order.trader
        transaction.currency=currency
        transaction.price=order.limit_price
        transaction.quantity=order.quantity
        transaction.result = transaction.price * transaction.quantity
        transaction.date=datetime.now()
        transaction.save()
        return transaction

    @staticmethod
    def createAlert(alert):
        """ Méthode de création d'une alerte """
        pass

    @staticmethod
    def createComment(comment):
        """ Méthode de création d'un commentaire """
        pass

    @staticmethod
    def createReward(reward):
        """ Méthode de création d'une récompense """
        pass

    @staticmethod
    def createClaimHistory(claim):
        """
            Méthode de création d'un historique d'une prédiction
        """
        claimHistory = ClaimHistory()
        claimHistory.claim = claim
        claimHistory.date = datetime.now()
        claimHistory.price = claim.price
        claimHistory.save()

        ##-------------------------------------------------
    ##
    ##  Méthodes de recherche
    ##
    ##-------------------------------------------------

    @staticmethod
    def getAllClaim():
        claims_list = Claim.objects.all()
        print(claims_list.__sizeof__())
        return claims_list

    @staticmethod
    def getAllTrader():
        """ Méthode de création d'une alerte """
        traders_list = Trader.objects.all()
        return traders_list

    @staticmethod
    def getAllTransaction(trader):
        transactions = MarketTransaction.objects.filter(trader=trader)
        return transactions

    @staticmethod
    def getAllHolding(trader):
        holdings_list = Holding.objects.filter(trader=trader)
        return holdings_list

    @staticmethod
    def getAllOrder(trader):
        orders_list = MarketOrder.objects.filter(trader=trader)
        return orders_list

    @staticmethod
    def getClaimById(id):
        claim = Claim.objects.get(id=id)
        return claim

    @staticmethod
    def getHelp(page):
        return "s"

    @staticmethod
    def getConfig(key):
        config = Configuration.objects.get(key=key)
        return config

    @staticmethod
    def getClaimHistory(claim):
        return "s"

    @staticmethod
    def getLeaderboard():
        #cursor = connection.cursor()

        traders = Trader.objects.raw("SELECT * FROM trader ORDER BY cash DESC LIMIT 10")

        #row = cursor.fetchone()
        return traders

    @staticmethod
    def getHelpTitleAsDict(page):
        helps = Help.objects.filter(page=page,type=HelpType.objects.get(name="TIP").id)
        help_title_dict = dict()
        for hlp in helps:
            help_title_dict[hlp.html_id] = hlp.title
        return help_title_dict

    @staticmethod
    def getHelpDescriptionAsDict(page):
        helps = Help.objects.filter(page=page,type=HelpType.objects.get(name="TIP").id)
        help_description_dict = dict()
        for hlp in helps:
            help_description_dict[hlp.html_id] = hlp.description
        return help_description_dict

    @staticmethod
    def getDataChartPerformance(trader):
        transactions = MarketTransaction.objects.raw("SELECT markettransaction.id,(20000+result) FROM markettransaction INNER JOIN trader ON markettransaction.num_transaction_trader=trader.id")
        data_performance = dict()
        for transac in transactions:
            data_performance[transac.date.year]=transac.result
        return data_performance


    ##-------------------------------------------------
    ##
    ##  Méthodes "privées" de la classe Service, utilisé
    ##  seulement au sein de cette classe
    ##-------------------------------------------------
    @staticmethod
    def processOrder(order):
        """

            Cette méthode est appelée createOrder(order)

            - Test si un ordre est compatible pour une transaction -> Service.matchingOrder(order)
            - Si un matching_order existe alors :
                - Création d'une transaction pour chaque trader
                - On set l'ordre comme quoi il est rempli -> order.filled = True
                - Test si une holding existe déjà pour cette prédiction
                    - Si oui : on incrémente notre holding
                    - Si non : on créer une nouvelle holding
                -- Changement du prix de la prédiction
                -- Création de l'historique

        """
        ##find matching order
        matching_order = Service.matchingOrder(order)
        claim = order.claim
        ##if there's a matching order -> create transaction and set both Orders as filled
        if matching_order is not None:
            transaction1 = Service.createTransaction(order,order.trader.currency)
            transaction2 = Service.createTransaction(matching_order,matching_order.trader.currency)
            order.filled = True
            matching_order.filled = True
            holding1 = Holding.objects.get(trader=order.trader,claim=claim)
            holding2 = Holding.objects.get(trader=matching_order.trader,claim=claim)

            if holding1 is None and not order.type==OrderType.objects.get(name="SELL"):
                Service.createHolding(transaction1,claim)
            else:
                ## modify holding 1
                pass

            if holding2 is None and not matching_order.type==OrderType.objects.get(name="SELL"):
                Service.createHolding(transaction2,claim)
            else:
                ## modify holding 2
                pass

            Service.createClaimHistory(claim)
            claim.price = transaction1.price


    @staticmethod
    def matchingOrder(order):
        """
            Méthode qui test si un ordre compatible avec celui en paramètre existe

            - On va simplement rechercher un ordre au même prix ou dans la même limite de prix
            -- Retourne l'ordre "matchant" si il existe
            -- Sinon retourne None
        """
        if order.type.name=='BUY':
            sell = OrderType.objects.get(name="SELL")
            list_matching_order = MarketOrder.objects.filter(limit_price=order.limit_price,type=sell,filled=False).exclude(trader=order.trader).order_by('date_sent')
            if list_matching_order.count()> 0:
                return list_matching_order[0]
            else:
                return None
        else:
            buy = OrderType.objects.get(name="BUY")
            list_matching_order = MarketOrder.objects.filter(limit_price=order.limit_price,type=buy,filled=False).exclude(trader=order.trader).order_by('date_sent')
            if list_matching_order.count()> 0:
                return list_matching_order[0]
            else:
                return None


    @staticmethod
    def sendNewClaimMail(claim):
        """
            Méthode permettant l'envoi d'un mail pour cause de nouvelle prédiction aux traders

            La méthode utilise la classe Tools
        """
        pass

    @staticmethod
    def sendSubscriptionMail(self,trader):
        """
            Méthode permettant l'envoi d'un mail lors d'une inscription

            La méthode utilise la classe Tools
        """
        pass

    @staticmethod
    def sendOrderActivatedMail(self,order):
        """
            Méthode permettant l'envoi d'un mail lorsqu'un ordre a été validée

            La méthode utilise la classe Tools
        """
        pass

    @staticmethod
    def sendEndClaimMail(self,claim):
        """
            Méthode permettant l'envoi d'un mail pour cause de fun de prédiction aux traders

            La méthode utilise la classe Tools
        """
        pass

