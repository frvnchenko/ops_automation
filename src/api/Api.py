
import requests
class Api:
    BASE_URL = "http://192.168.30.167:8081"
    ENDPOINT_MANUAL_INDEX = "/ops-tp-integration/service-api/process"

    def get_manual_index_ops(self):
        response = requests.get(self.BASE_URL+self.ENDPOINT_MANUAL_INDEX)
        return response