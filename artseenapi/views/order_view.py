"""View module for handling requests about viewer order"""
import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from artseenapi.models import Order, Payment, Viewer, Piece, OrderPiece
from .piece_view import PieceSerializer


class OrderLineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for line items """

    piece = PieceSerializer(many=False)

    class Meta:
        model = OrderPiece
        
        fields = ('id', 'piece')
        depth = 1

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for viewer orders"""

    lineitems = OrderLineItemSerializer(many=True)

    class Meta:
        model = Order
    
        fields = ('id', 'created_date', 'payment_type', 'viewer', 'lineitems')


class OrderView(ViewSet):
    """View for interacting with viewer orders"""

    def retrieve(self, request, pk=None):
        """
        @api {GET} /cart/:id GET single order
        @apiName GetOrder
        @apiGroup Orders

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611


        @apiSuccess (200) {id} id Order id
        @apiSuccess (200) {String} url Order URI
        @apiSuccess (200) {String} created_date Date order was created
        @apiSuccess (200) {String} payment_type Payment URI
        @apiSuccess (200) {String} viewer Viewer URI
        """
        try:
            viewer = Viewer.objects.get(user=request.auth.user)
            order = Order.objects.get(pk=pk, viewer=viewer)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)

        except Order.DoesNotExist as ex:
            return Response(
                {'message': 'The requested order does not exist, or you do not have permission to access it.'},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """
        @api {PUT} /order/:id PUT new payment for order
        @apiName AddPayment
        @apiGroup Orders

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} id Order Id route parameter
        @apiParam {id} payment_type Payment Id to pay for the order
        @apiParamExample {json} Input
            {
                "payment_type": 6
            }

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        viewer = Viewer.objects.get(user=request.auth.user)
        order = Order.objects.get(pk=pk, viewer=viewer)
        payment_type = Payment.objects.get(pk=request.data['payment_type'])
        order.payment_type = payment_type
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """
        @api {GET} /orders GET viewer orders
        @apiName GetOrders
        @apiGroup Orders

        @apiHeader {String} Authorization Auth token
        @apiHeaderExample {String} Authorization
            Token 9ba45f09651c5b0c404f37a2d2572c026c146611

        @apiParam {id} payment_id Query param to filter by payment used

        @apiSuccess (200) {Object[]} orders Array of order objects
        @apiSuccess (200) {id} orders.id Order id
        @apiSuccess (200) {String} orders.url Order URI
        @apiSuccess (200) {String} orders.created_date Date order was created
        @apiSuccess (200) {String} orders.payment_type Payment URI
        @apiSuccess (200) {String} orders.viewer Viewer URI
        """
        viewer = Viewer.objects.get(user=request.auth.user)
        orders = Order.objects.filter(viewer=viewer)

        payment = self.request.query_params.get('payment_id', None)
        if payment is not None:
            orders = orders.filter(payment__id=payment)

        json_orders = OrderSerializer(
            orders, many=True, context={'request': request})

        return Response(json_orders.data)
