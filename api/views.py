from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PaymentDetailSerializers
from.PaymentGateway import PremiumPaymentGateway, ExpensivePaymentGateway, CheapPaymentGateway, ExpensivePaymentGatewayAvailable


class ProcessPayment(APIView):
    def post(self, request):
        _comment = "Server error"
        try:
            validate = PaymentDetailSerializers(data=request.data)
            if validate.is_valid():
                _status = status.HTTP_200_OK
                _comment = "Payment is Processed"
                amount = float(validate.data.get("Amount"))

                # Cheap Payment Gateway
                if amount < 20:
                    if CheapPaymentGateway():
                        _status = status.HTTP_200_OK
                    else:
                        _status = status.HTTP_500_INTERNAL_SERVER_ERROR

                # Expensive Payment Gateway
                elif 20 <= amount <= 500:
                    if ExpensivePaymentGatewayAvailable():      # checking if Expensive Payment gateway is available
                        if ExpensivePaymentGateway():
                            _status = status.HTTP_200_OK
                        else:
                            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                    else:                                       # if not available then go with cheap payment gateway
                        if CheapPaymentGateway():
                            _status = status.HTTP_200_OK
                        else:
                            _status = status.HTTP_500_INTERNAL_SERVER_ERROR

                # Premium Payment Gateway
                elif amount > 500:
                    if PremiumPaymentGateway():                 # try 3 times to success payment
                        _status = status.HTTP_200_OK
                    elif PremiumPaymentGateway():
                        _status = status.HTTP_200_OK
                    elif PremiumPaymentGateway():
                        _status = status.HTTP_200_OK
                    else:
                        _status = status.HTTP_500_INTERNAL_SERVER_ERROR
                else:
                    _status = status.HTTP_500_INTERNAL_SERVER_ERROR

            else:
                _status = status.HTTP_400_BAD_REQUEST
                _comment = validate.errors
        except:
            _status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(_comment, status=_status)




#{"CardHolder": "Ronak jain", "ExpirationDate": "2021-01-19 13:20:56.121152", "SecurityCode": "123", "Amount": "100", "CreditCardNumber": "378282246310005"}