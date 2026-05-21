from pasarela.models import Provider, Transaction, Incidence
from pasarela.api.serializers import ProviderSerializer, TransactionSerializer, IncidenceSerializer
from rest_framework.viewsets import  ModelViewSet
from rest_framework.permissions import IsAdminUser
import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProviderModelViewSet(ModelViewSet):
    #permission_classes=[IsAdminUser] #solo admins puede interactuar
    serializer_class=ProviderSerializer
    queryset=Provider.objects.all()
    #http_method_names=['get', 'put']-> limita el CRUD para ser solo get y put



class TransactionModelViewSet(ModelViewSet):
    #permission_classes=[IsAdminUser]
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()



class IncidenceModelViewSet(ModelViewSet):
    #permission_classes=[IsAdminUser]
    serializer_class=IncidenceSerializer
    queryset=Incidence.objects.all()


@api_view(['POST'])
def create_payment(request):

    provider_id=request.data.get('provider_id')
    amount=request.data.get('amount')

    try:

        provider=Provider.objects.get(id=provider_id)

        # crear sesión stripe
        checkout_session=stripe.checkout.Session.create(
            payment_method_types=['card'],

            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': f'Pago proveedor {provider.id}',
                        },
                        'unit_amount': int(float(amount)*100),
                    },
                    'quantity': 1,
                }
            ],

            mode='payment',

            success_url='http://localhost:3000/success',
            cancel_url='http://localhost:3000/cancel',
        )

        transaction=Transaction.objects.create(
            id_proveedor=provider,
            amount=amount,
            currency='EUR',
            payment_state='pending',
            stripe_session_id=checkout_session.id,
        )

        return Response({
            'checkout_url': checkout_session.url,
            'transaction_id': transaction.id
        })

    except Provider.DoesNotExist:

        return Response({
            'error': 'Proveedor no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    


@csrf_exempt
@api_view(['POST'])
def stripe_webhook(request):

    payload=request.body
    sig_header=request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event=stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )

        # pago completado
        if event['type']=='checkout.session.completed':

            session=event['data']['object']

            stripe_session_id=session['id']

            transaction=Transaction.objects.get(
                stripe_session_id=stripe_session_id
            )

            transaction.payment_state='completed'
            transaction.save()

        return Response(status=200)

    except Exception as e:

        print("ERROR WEBHOOK:")
        print(str(e))

        return Response(
            {"error": str(e)},
            status=400
        )