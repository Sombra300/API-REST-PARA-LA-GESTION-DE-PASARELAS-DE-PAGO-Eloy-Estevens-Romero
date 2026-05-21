from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

# Modelo de los Proveedores
class Provider(models.Model):
    environments_options=[
        ('dev', 'Desarrollo'),
        ('test', 'Testing'),
        ('prod', 'Producción'),
    ]


    name=models.CharField(max_length=100, unique=True)
    environment=models.CharField(choices=environments_options, default='test')
    active=models.BooleanField(default=False)
    creation_date=models.DateTimeField(auto_now_add=True)

    def clean(self):

        #Validar name
        if self.name is None or self.name.strip()=='':
            raise ValidationError('El nombre no puede estar vacio')
        
        if len(self.name)>100:
            raise ValidationError('El nombre es demasiado largo')
        
        if Provider.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError('El nombre ya esta en uso')

        #validar environment
        bool_environment_acepted=False
        for i in self.environments_options:
            if self.environment==i[0]:
                bool_environment_acepted=True
        
        if bool_environment_acepted==False:
            raise ValidationError('Datos manipulados: opcion no valida')

    def __str__(self):
        return self.name 



# Modelo de las transacciones
class Transaction(models.Model):
    type_transaction_options=[
        ('pending', 'Pago pendiente'), 
        ('completed', 'Pago completado'),
        ('failed', 'Pago fallido'),
        ('refuned', 'Pago devuelto'),
    ]

    id_proveedor=models.ForeignKey(Provider, on_delete=models.CASCADE)
    stripe_session_id = models.CharField(max_length=255, null=True, blank=True)
    amount=models.DecimalField(max_digits=5, decimal_places=2)
    currency=models.CharField(max_length=10, default='€')
    payment_state=models.CharField(choices=type_transaction_options, default='pending')
    creation_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now_add=True)

    def clean(self):

        #validar amount
        if self.amount is None:
            raise ValidationError('Tienes que procesar algun pago para realizar una transaccion')
        
        if self.amount<0:
            raise ValidationError('El pago no puede ser menor a 0')


        #validar currency
        if any(char.isdigit() for char in self.currency):
            raise ValidationError('Hay numeros en el campo del tipo de modera')
        
        if len(self.currency)>10:
            raise ValidationError('El tipo de moneda supera el tamaño maximo del texto')


        #validar payment state
        bool_transaction_acepted=False
        for i in self.type_transaction_options:
            if self.payment_state==i[0]:
                bool_transaction_acepted=True
        
        if bool_transaction_acepted==False:
            raise ValidationError('Datos manipulados: opcion no valida')


        # validar provider id
        if self.id_proveedor_id is None:
            raise ValidationError('Datos del proveedor no encontrados para la transaccion')
        
        if not Provider.objects.filter(pk=self.id_proveedor_id).exists():
            raise ValidationError('No se encuentra el proveedor')

    def __str__(self):
        return f'ID del proveedor: {self.id_proveedor}  -> {self.amount}  {self.currency}'
    

# Modelo de las incidencias
class Incidence(models.Model):
    type_incidence_options=[
        ('nonpayment','Impago'),
        ('connection_error','Error de conexion'),
        ('devolution','Devolucion'),
        ('timeout','Timeout'),
        ('authentication_error','Error de autenticacion'),
    ]

    id_transaction=models.ForeignKey(Transaction, on_delete=models.CASCADE)
    description=models.CharField(max_length=500, default='Sin descripcion')
    type=models.CharField(choices=type_incidence_options)
    creation_date=models.DateTimeField(auto_now=True)

    def clean(self):

        #validar id transaction
        if self.id_transaction is None:
            raise ValidationError('Datos de la transaccion no encontrados para la transaccion')
        
        if not Transaction.objects.filter(pk=self.id_transaction).exists():
            raise ValidationError('No se encuentra la transaccion')

        #validar description
        if len(self.description)>500:
            raise ValidationError('Descripcion demasiado larga')


        #validar type
        bool_type_acepted=False
        for i in self.type_incidence_options:
            if self.type==i[0]:
                bool_type_acepted=True
        
        if bool_type_acepted==False:
            raise ValidationError('Datos manipulados: opcion no valida')

    def __str__(self):
        return f'{self.id_transaction}  ->  {self.type}  ->  {self.description}'