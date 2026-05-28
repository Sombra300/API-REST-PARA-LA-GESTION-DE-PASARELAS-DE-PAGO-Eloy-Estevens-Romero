from pasarela.models import Provider, Transaction, Incidence
from pasarela.api.serializers import ProviderSerializer, TransactionSerializer, IncidenceSerializer
from rest_framework.viewsets import  ModelViewSet
import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt


stripe.api_key=settings.STRIPE_SECRET_KEY


class ProviderModelViewSet(ModelViewSet):
    serializer_class=ProviderSerializer
    queryset=Provider.objects.all()



class TransactionModelViewSet(ModelViewSet):
    serializer_class=TransactionSerializer
    queryset=Transaction.objects.all()



class IncidenceModelViewSet(ModelViewSet):
    serializer_class=IncidenceSerializer
    queryset=Incidence.objects.all()


#Crear transaction
@api_view(['POST'])
def create_payment(request):

    provider_id=request.data.get('provider_id')
    amount=request.data.get('amount')
    currency = request.data.get('currency', 'EUR')

    try:

        if not isinstance(amount, (int, float)):
            raise ValueError("El importe debe ser un número")

        if amount<=0 or amount=='':
            raise Exception('El importe tiene que ser superior a 0')

        provider=Provider.objects.get(id=provider_id)

        # crear sesión stripe
        checkout_session=stripe.checkout.Session.create(
            payment_method_types=['card'],

            line_items=[
                {
                    'price_data': {
                        'currency': currency,
                        'product_data': {
                            'name': f'Pago usando el proveedor {provider.name}',
                        },
                        'unit_amount': int(float(amount)*100),
                    },
                    'quantity': 1,
                }
            ],

            mode='payment',

            success_url='http://127.0.0.1:8000/api/transaction/',
            cancel_url='http://127.0.0.1:8000/api/transaction/',
        )

        transaction=Transaction.objects.create(
            id_proveedor=provider,
            amount=amount,
            currency=currency,
            payment_state='pending',
            stripe_session_id=checkout_session.id,
        )

        return Response({
            'checkout_url': checkout_session.url,
            'transaction_id_create': transaction.id
        })

    except Provider.DoesNotExist:

        return Response({
            'error': 'Proveedor no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:

        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    

#Actualizar transaction pendiente->completa
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
            payment_intent=session['payment_intent']
            transaction=Transaction.objects.get(
                stripe_session_id=stripe_session_id
            )
            transaction.payment_state='completed'
            transaction.stripe_payment_intent=payment_intent
            transaction.save()

        return Response(status=200)

    except Exception as e:

        print('ERROR WEBHOOK:')
        print(str(e))

        return Response(
            {'error': str(e)},
            status=400
        )
    


# Hacer devoluciones
@api_view(['POST'])
def refund_payment(request):

    transaction_id_create=request.data.get('transaction_id')

    try:

        transaction=Transaction.objects.get(id=transaction_id_create)
        if transaction.payment_state!='completed':
            return Response({
                'error': 'Solo se pueden devolver pagos completados'
            }, status=400)


        if not transaction.stripe_payment_intent:
            return Response({
                'error': 'La transacción no tiene payment intent'
            }, status=400)

        refund=stripe.Refund.create(
            payment_intent=transaction.stripe_payment_intent
        )

        transaction.payment_state='refunded'
        transaction.save()

        incidence_create=Incidence.objects.create(
            id_transaction=transaction,
            description='Devolution',
            type='devolution'
        )

        return Response({
            'message': 'Refund realizado correctamente',
            'refund_id': refund.id,
            'incidence_id': incidence_create.id
        })

    except Transaction.DoesNotExist:
        return Response({
            'error': 'Transacción no encontrada'
        }, status=404)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=400)