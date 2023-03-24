"""View module for handling requests about viewer shopping cart"""
import datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from artseenapi.models import Order, Viewer, Piece, OrderPiece
from .piece_view import PieceSerializer
from .order_view import OrderSerializer
from django.db.models import Sum


class CartView(ViewSet):
    """Shopping cart for ArtSeen eCommerce"""

    def create(self, request):
        """
        @api {POST} /cart POST new line items to cart
        @apiName AddLineItem
        @apiGroup ShoppingCart

        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        @apiParam {Number} piece_id Id of piece to add
        """
        current_user = Viewer.objects.get(user=request.auth.user)

        try:
            open_order = Order.objects.get(
                viewer=current_user, payment_type__isnull=True)
        except Order.DoesNotExist:
            open_order = Order()
            open_order.created_date = datetime.datetime.now()
            open_order.viewer = current_user
            open_order.save()

        line_item = OrderPiece()
        line_item.piece = Piece.objects.get(pk=request.data["piece_id"])
        line_item.order = open_order
        line_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """
        @api {DELETE} /cart/:id DELETE line item from cart
        @apiName RemoveLineItem
        @apiGroup ShoppingCart

        @apiParam {id} id Piece Id to remove from cart
        @apiSuccessExample {json} Success
            HTTP/1.1 204 No Content
        """
        current_user = Viewer.objects.get(user=request.auth.user)
        open_order = Order.objects.get(
            viewer=current_user, payment_type=None)

        line_item = OrderPiece.objects.filter(
            piece__id=pk,
            order=open_order
        )[0]
        line_item.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """
        @api {GET} /cart GET line items in cart
        @apiName GetCart
        @apiGroup ShoppingCart

        @apiSuccess (200) {Number} id Order cart
        @apiSuccess (200) {String} url URL of order
        @apiSuccess (200) {String} created_date Date created
        @apiSuccess (200) {Object} payment_type Payment id use to complete order
        @apiSuccess (200) {String} viewer URI for viewer
        @apiSuccess (200) {Number} size Number of items in cart
        @apiSuccess (200) {Object[]} line_items Line items in cart
        @apiSuccess (200) {Number} line_items.id Line item id
        @apiSuccess (200) {Object} line_items.piece Piece in cart
        """
        current_user = Viewer.objects.get(user=request.auth.user)
        try:
            open_order = Order.objects.get(
                viewer=current_user, payment_type=None)

            pieces_on_order = Piece.objects.filter(
                lineitems__order=open_order)

            serialized_order = OrderSerializer(
                open_order, many=False, context={'request': request})

            piece_list = PieceSerializer(
                pieces_on_order, many=True, context={'request': request})

            final = {
                "order": serialized_order.data
            }
            final["order"]["pieces"] = piece_list.data
            final["order"]["size"] = len(pieces_on_order)
            final["order"]["total"] = pieces_on_order.aggregate(Sum('price'))

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        return Response(final["order"])
