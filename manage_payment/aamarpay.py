from ast import Str
import json
import requests

sandBoxUrl = 'https://sandbox.aamarpay.com/index.php'
productionUrl = 'https://secure.aamarpay.com/index.php'
succesUrl = 'http://127.0.0.1:8000/payment/payment_success'
failUrl = 'https://example.com/payment/fail'
cancelUrl = 'https://example.com/payment/cancel'
signature = 'dbb74894e82415a2f7ff0ec3a97e4183'
storeID = 'aamarpaytest'
sandboxReturnUrl = 'https://sandbox.aamarpay.com'
productionReturnUrl = 'https://sandbox.aamarpay.com'


class aamarPay:
    isSandbox: bool
    storeID: str
    successUrl: str
    failUrl: str
    cancelUrl: str
    transactionID: str
    transactionAmount: int
    signature: str
    description: str
    customerName: str
    customerEmail: str
    customerMobile: str
    customerAddress1: str
    customerAddress2: str
    customerCity: str
    customerState: str
    customerPostCode: str

    def __init__(self, isSandbox=True, storeID=storeID, successUrl=succesUrl, failUrl=failUrl,
                 cancelUrl=cancelUrl, transactionID='testTrId', transactionAmount='100',
                 signature=signature, description='Description', customerName='Test user',
                 customerEmail='sandbox@email.com', customerMobile='0111111111', customerAddress1='',
                 customerAddress2='', customerCity='', customerState='', customerPostCode='') -> None:
        self.isSandbox = isSandbox
        self.storeID = storeID
        self.successUrl = successUrl
        self.failUrl = failUrl
        self.cancelUrl = cancelUrl
        self.transactionID = transactionID
        self.transactionAmount = transactionAmount
        self.signature = signature
        self.description = description
        self.customerName = customerName
        self.customerEmail = customerEmail
        self.customerMobile = customerMobile
        self.customerAddress1 = customerAddress1
        self.customerAddress2 = customerAddress2
        self.customerCity = customerCity
        self.customerState = customerState
        self.customerPostCode = customerPostCode

    def payment(self):
        try:
            payload = {
                "store_id": self.storeID,
                "tran_id": self.transactionID,
                "success_url": self.successUrl,
                "fail_url": self.failUrl,
                "cancel_url": self.cancelUrl,
                "amount": self.transactionAmount,
                "currency": "BDT",
                "signature_key": self.signature,
                "desc": self.description,
                "cus_name": self.customerName,
                "cus_email": self.customerEmail,
                "cus_add1":
                    self.customerAddress1,
                "cus_add2":
                    self.customerAddress2,
                "cus_city": self.customerCity,
                "cus_state":
                    self.customerState,
                "cus_postcode": self.customerPostCode,
                "cus_country": "Bangladesh",
                "cus_phone": self.customerMobile,
                "type": "json"
            }
            response = requests.post(sandBoxUrl if self.isSandbox else productionUrl, payload)
            parseRes = json.loads(response.text)
            if response.status_code == 200:
                if type(parseRes) is not Str and "payment_url" in parseRes:
                    return parseRes["payment_url"]
                return response.text
            return response.text
        except:
            return "unkonwn error"
