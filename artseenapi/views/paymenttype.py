"""View module for handling requests about viewer payment types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from artseenapi.models import Payment, Viewer


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for Payment

    Arguments:
        serializers
    """
    class Meta:
        model = Payment
        fields = ('id', 'merchant_name', 'account_number',
                  'expiration_date', 'create_date')


class PaymentTypesView(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized payment instance
        """
        new_payment = Payment()
        new_payment.merchant_name = request.data["merchant_name"]
        new_payment.account_number = request.data["account_number"]
        new_payment.expiration_date = request.data["expiration_date"]
        new_payment.zip_code = request.data["zip_code"]
        viewer = Viewer.objects.get(user=request.auth.user)
        new_payment.viewer = viewer
        new_payment.save()

        serializer = PaymentSerializer(
            new_payment, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment_type instance
        """
        try:
            payment_type = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(
                payment_type, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single payment type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to payment type resource"""
        payment_types = Payment.objects.all()
        viewer = Viewer.objects.get(user=request.auth.user)

        if viewer is not None:
            payment_types = payment_types.filter(viewer=viewer)


            if len(payment_types) >= 1:
                for payment in payment_types:
                    last_four = str(int(payment.account_number))[-4:]
                    payment.account_number = last_four

                serializer = PaymentSerializer(
                payment_types, many=True, context={'request': request})
                return Response(serializer.data)

            else:
                return Response({'message': 'Viewer does not have any payment methods saved'}, status=status.HTTP_200_OK)