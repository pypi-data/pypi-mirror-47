# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from payu_api.conf import settings
from payu_api import signals
from django.utils import timezone

@python_2_unicode_compatible
class AbstractPayment(models.Model):

    # http://developers.payu.com/pl/restapi.html#notifications

    CURRENCY_CHOICE = settings.PAYU_API_CURRENCY_CHOICE

    PENDING = 99
    WAITING_FOR_CONFIRMATION = 10
    COMPLETED = 20
    CANCELED = 30
    REJECTED = 40
    NEW = 50
    REFUNDED = 60
    OTHER = 70

    STATUS_CHOICE = (
        (PENDING, _(u"Oczekująca")),
        (WAITING_FOR_CONFIRMATION, _(u"Do potwierdzenia w sklepie")),
        (COMPLETED, _(u"Zakończona")),
        (CANCELED, _(u"Anulowana")),
        (REJECTED, _(u"Odrzucona")),
        (NEW, _(u"Nowa")),
        (REFUNDED, _(u"Zwrócona")),
    )

    amount = models.DecimalField(max_digits = 8, decimal_places = 2)
    currency = models.CharField(choices = CURRENCY_CHOICE, max_length = 4, default = 'PLN')
    status = models.IntegerField(choices = STATUS_CHOICE, default = NEW)
    add_date = models.DateTimeField(auto_now_add = True)
    date_change = models.DateTimeField(auto_now = True)
    pay_date = models.DateTimeField(blank = True, null = True)
    amount_paid = models.IntegerField(default = 0)
    payu_order_id = models.CharField(max_length = 64, blank = True, null = True)

    order = models.ForeignKey(settings.PAYU_API_ORDER_MODEL, related_name = 'order_payments')

    pay_link = models.CharField(max_length = 512, blank = True, null = True)
    pay_link_valid_until = models.DateTimeField(blank = True, null = True)

    class Meta:
        abstract = True
        verbose_name = _(u"Płatność")
        verbose_name_plural = _(u"Płatności")

    def __str__(self):
        return u"%s" % (self.id,)

    def get_payment_value(self):
        return self.amount * settings.CURRENCY_DATA[self.currency]['sub_unit']

    def change_status(self, new_status):
        """
        Always change payment status via this method. Otherwise the signal
        will not be emitted.
        """
        if self.status != new_status:
            # do anything only when status is really changed
            old_status = self.status
            self.status = new_status
            if new_status == self.COMPLETED:
                self.pay_date = timezone.now()

            self.save()
            signals.rest_payment_status_changed.send(
                sender = type(self), instance = self,
                old_status = old_status, new_status = new_status
            )

