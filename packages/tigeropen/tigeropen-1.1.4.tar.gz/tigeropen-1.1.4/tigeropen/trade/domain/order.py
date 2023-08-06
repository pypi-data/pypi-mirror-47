# -*- coding: utf-8 -*-
"""
Created on 2018/9/20

@author: gaoan
"""
from six import text_type
from tigeropen.common.consts import OrderStatus

ORDER_FIELDS_TO_IGNORE = {'type', '_status', 'contract', '_remaining'}


class Order(object):
    __slots__ = ["account", "id", "order_id", "parent_id", "order_time", "reason", "trade_time", "contract", "action",
                 "quantity", "filled", "_remaining", "avg_fill_price", "commission", "realized_pnl", "_status",
                 "trail_stop_price", "limit_price", "aux_price", "trailing_percent", "percent_offset", "action",
                 "order_type", "time_in_force", "outside_rth"]

    def __init__(self, account, contract, action, order_type, quantity, limit_price=None, aux_price=None,
                 trail_stop_price=None, trailing_percent=None, percent_offset=None, time_in_force=None,
                 outside_rth=None, filled=0, avg_fill_price=0, commission=None, realized_pnl=None,
                 id=None, order_id=None, parent_id=None):
        """
        @dt - datetime.datetime that the order was placed
        @contract - contract for the order.
        @quantity - the number of shares to buy/sell
                  a positive sign indicates a buy
                  a negative sign indicates a sell
        @filled - how many shares of the order have been filled so far
        """

        self.id = id
        self.order_id = order_id
        self.parent_id = parent_id
        self.account = account
        self.reason = None
        self.contract = contract
        self.action = action
        self.quantity = quantity
        self.filled = filled
        self._remaining = None
        self.avg_fill_price = avg_fill_price
        self.realized_pnl = realized_pnl
        self.commission = commission
        self._status = OrderStatus.NEW
        self.time_in_force = time_in_force
        self.outside_rth = outside_rth
        self.order_type = order_type
        self.limit_price = limit_price
        self.aux_price = aux_price
        self.trail_stop_price = trail_stop_price
        self.trailing_percent = trailing_percent
        self.percent_offset = percent_offset
        self.order_time = None
        self.trade_time = None

    def to_dict(self):
        dct = {name: getattr(self, name) for name in self.__slots__ if name not in ORDER_FIELDS_TO_IGNORE}

        dct['contract'] = self.contract
        if self.status:
            dct['status'] = self.status.name
        dct['remaining'] = self.remaining

        return dct

    @property
    def status(self):
        if not self.remaining:
            return OrderStatus.FILLED
        elif self._status == OrderStatus.HELD and self.filled:
            return OrderStatus.PARTIALLY_FILLED
        else:
            return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def active(self):
        return self.status in [OrderStatus.PENDING_NEW, OrderStatus.NEW, OrderStatus.PARTIALLY_FILLED,
                               OrderStatus.HELD, OrderStatus.PENDING_CANCEL]

    @property
    def remaining(self):
        return self.quantity - self.filled

    def __repr__(self):
        """
        String representation for this object.
        """
        return "Order(%s)" % self.to_dict().__repr__()

    def __unicode__(self):
        """
        Unicode representation for this object.
        """
        return text_type(repr(self))
