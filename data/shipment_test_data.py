from data.base_data import BaseData
from endpoints.shipment_endpoint import ShipmentEndPoint


class ShipmentTestData(BaseData):
    def get_test_shipments(self):
        return ShipmentEndPoint().get_shipment_items(self.get_request("shipments"))
