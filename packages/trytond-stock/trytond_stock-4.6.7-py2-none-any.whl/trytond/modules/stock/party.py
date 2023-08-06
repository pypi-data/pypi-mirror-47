# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['PartyReplace']


class PartyReplace:
    __metaclass__ = PoolMeta
    __name__ = 'party.replace'

    @classmethod
    def fields_to_replace(cls):
        return super(PartyReplace, cls).fields_to_replace() + [
            ('stock.shipment.in', 'supplier'),
            ('stock.shipment.in.return', 'supplier'),
            ('stock.shipment.out', 'customer'),
            ('stock.shipment.out.return', 'customer'),
            ]
