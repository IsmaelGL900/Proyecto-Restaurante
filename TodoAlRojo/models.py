from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

#LOGIN Y REGISTRO--------------------------------------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, rol, password=None):
        if not email:
            raise ValueError("El usuario debe tener un email")
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, rol=rol)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, rol='admin', password=None):
        usuario = self.create_user(email, nombre, rol, password)
        usuario.is_superuser = True
        usuario.is_staff = True
        usuario.save(using=self._db)
        return usuario


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('cocinero', 'Cocinero'),
        ('camarero', 'Camarero'),
    )

    email = models.EmailField(max_length=500, unique=True)
    nombre = models.CharField(max_length=250)
    rol = models.CharField(max_length=25, choices=ROLES, default='cliente')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'rol']

    def __str__(self):
        return f"{self.email} - {self.nombre} ({self.rol})"

#LOGIN Y REGISTRO--------------------------------------------------------------

class Producto(models.Model):
    TIPOS_PRODUCTO = [
        ('HAMBURGUESA', 'Hamburguesa'),
        ('ENTRANTE', 'Entrante'),
        ('BEBIDA', 'Bebida'),
        ('POSTRE', 'Postre'),
    ]

    nombre = models.CharField(max_length=100)
    imagen = models.CharField(max_length=1000)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=50, choices=TIPOS_PRODUCTO)
    ingredientes = models.CharField(max_length=1000, null=True, blank=True)


    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Mesa(models.Model):
    ESTADOS = [
        ('DISPONIBLE', 'Disponible'),
        ('OCUPADA', 'Ocupada'),
    ]
    numero = models.IntegerField(unique=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='DISPONIBLE')

    def __str__(self):
        return f"Mesa {self.numero} ({self.estado})"

class Carrito(models.Model):
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, limit_choices_to={'rol': 'cliente'})
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.cliente.nombre}"

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (${self.subtotal})"

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PREPARACION', 'En preparación'),
        ('ENTREGADO', 'Entregado'),
    ]

    cliente = models.ForeignKey('Usuario', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'rol': 'cliente'}, related_name='pedidos_como_cliente')
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    camarero = models.ForeignKey('Usuario', limit_choices_to={'rol': 'camarero'}, on_delete= models.CASCADE, related_name='pedidos_como_camarero', null=True, blank=True)
    cocinero = models.ForeignKey('Usuario', limit_choices_to={'rol': 'cocinero'}, on_delete= models.CASCADE, related_name='pedidos_como_cocinero', null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='PENDIENTE')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nombre} ({self.estado})"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre} (${self.subtotal})"


class PedidoTerminado(models.Model):
    cliente = models.CharField(max_length=250, null=True, blank=True)
    mesa_numero = models.IntegerField()
    camarero = models.CharField(max_length=250, null=True, blank=True)
    cocinero = models.CharField(max_length=250, null=True, blank=True)
    fecha = models.DateTimeField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"PedidoTerminado #{self.id} - {self.cliente} - Mesa {self.mesa_numero}"


class ItemPedidoTerminado(models.Model):
    pedido_terminado = models.ForeignKey(PedidoTerminado, related_name='items', on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto} (${self.subtotal})"