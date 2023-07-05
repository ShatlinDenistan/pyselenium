"""Data Class to store Draft Shipment Objects"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Shipment:
    """Data Class to store Draft Shipment Objects"""

    selected: Optional[bool] = False
    due_date: Optional[str] = None
    name: Optional[str] = None
    po_number: Optional[str] = None
    dist_centre: Optional[str] = None
    status: Optional[str] = None
    qty_required: Optional[str] = None
    qty_sending: Optional[str] = None
    qty_received: Optional[str] = None
    qty_damaged: Optional[str] = None
    po_name: Optional[str] = None
    shipment_id: Optional[str] = None
    orders: Optional[list] = None
