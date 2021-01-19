from rest_framework import serializers
from datetime import datetime, timezone


def date_validator(date):
    if date < datetime.now(timezone.utc):
        raise serializers.ValidationError("The date cannot be in the past!")
    return date


def security_code_validator(code):
    if len(str(code)) != 3:
        raise serializers.ValidationError("Length of Security code must be 3")
    return code


def credit_card_validator(number):
    number = int(number)
    if number <= 0:
        raise serializers.ValidationError("credit card can not be negative")

    as_string = str(number)
    reverse = as_string[::-1]

    odd_digits = reverse[::2]
    odd_sum = sum(int(i) for i in odd_digits)

    even_digits = reverse[1::2]
    doubled_even_digits = [int(i) * 2 for i in even_digits]
    summed_digits_for_even_doubles = [i // 10 + i % 10 for i in doubled_even_digits]
    sum_of_even_digit_sums = sum(summed_digits_for_even_doubles)

    if (sum_of_even_digit_sums + odd_sum) % 10 == 0:
        return str(number)
    else:
        raise serializers.ValidationError("credit card is not valid")


def cardholder_validator(name):
    if all(x.isalpha() or x.isspace() for x in name):
        return name
    raise serializers.ValidationError("Card holder name only contains letters")


class PaymentDetailSerializers(serializers.Serializer):
    CreditCardNumber = serializers.CharField(validators=[credit_card_validator])
    CardHolder = serializers.CharField(max_length=26, min_length=2, validators=[cardholder_validator])
    ExpirationDate = serializers.DateTimeField(validators=[date_validator])
    SecurityCode = serializers.IntegerField(min_value=1, validators=[security_code_validator], required=False)
    Amount = serializers.DecimalField(min_value=1, max_digits=10, decimal_places=2)


