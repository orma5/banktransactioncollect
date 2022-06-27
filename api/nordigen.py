import requests


class NordigenClient:

    def __init__(self, secret_id, secret_key) -> None:

        self.secret_id = secret_id
        self.secret_key = secret_key

        self.base_url = "https://ob.nordigen.com/api/v2"

        self._headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

        self._token = None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        self._headers["Authorization"] = f"Bearer {value}"

    def generate_token(self):

        url = f"{self.base_url}/token/new/"
        payload = {"secret_key": self.secret_key, "secret_id": self.secret_id}

        r = requests.post(url, payload, self._headers)
        reqStatus = r.status_code

        if reqStatus != 200:
            raise requests.ConnectionError("Expected status code 200, \
                                            but got"+reqStatus+" : "+r.reason)

        response = r.json()
        self.token = response["access"]

        return response

    def getAllTransactionsForAccount(self, bankAccountID):

        url = f"{self.base_url}/accounts/{bankAccountID}/transactions/"

        r = requests.get(url, headers=self._headers)
        reqStatus = r.status_code

        if reqStatus != 200:
            raise requests.ConnectionError("Expected status code 200, \
                                            but got"+reqStatus+" : "+r.reason)

        response = r.json()

        return response["transactions"]["booked"]

    def getTransactionsForAccount(self, bankAccountID, date_from, date_to):

        url = f"{self.base_url}/accounts/{bankAccountID}/transactions/"

        parameters = {"date_from": date_from, "date_to": date_to}

        r = requests.get(url, params=parameters, headers=self._headers)
        reqStatus = r.status_code

        if reqStatus != 200:
            raise requests.ConnectionError("Expected status code 200, \
                                            but got"+reqStatus+" : "+r.reason)

        response = r.json()

        return response["transactions"]["booked"]
