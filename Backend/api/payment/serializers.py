from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def validate_transaction_uuid(self, value):
        super().validate(value)  # Call the superclass validation

        if Payment.objects.filter(transaction_uuid=value).exists():
            raise serializers.ValidationError("UUID already exists")

        return value
    
    def validate_transaction_code(self, value):
        super().validate(value)  # Call the superclass validation

        if Payment.objects.filter(transaction_code=value).exists():
            raise serializers.ValidationError("Transaction code already exists")

        return value
