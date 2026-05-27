# API-REST-PARA-LA-GESTION-DE-PASARELAS-DE-PAGO

Proyecto final desarrollado con Django y Django REST Framework para la gestión centralizada de proveedores de pago en plataformas e-Commerce.

---

# Descripción del proyecto

Este proyecto consiste en el desarrollo de una API REST que permita administrar diferentes pasarelas de pago, empezando con Stripe y con la posibilidad de extenderse a PayPal o Redsys desde un único backend.

El sistema permite:

- Registrar proveedores de pago.
- Gestionar transacciones.
- Controlar incidencias y errores.
- Consultar historiales de pagos.
- Proteger el acceso mediante autenticación.

La aplicación está diseñada siguiendo una arquitectura RESTful y buenas prácticas de desarrollo backend con Python y Django REST Framework.

---

# Objetivos

- Desarrollar una API REST profesional con Django REST Framework.
- Diseñar una base de datos relacional utilizando SQLite.
- Implementar operaciones CRUD completas.
- Gestionar estados e incidencias de transacciones.
- Aplicar autenticación y seguridad en endpoints.
- Mantener trazabilidad del proyecto mediante Git y GitHub.

---

# Tecnologías utilizadas

- Python 3
- Django
- Django REST Framework
- SQLite
- Git & GitHub
- Postman

---

# Estructura inicial del proyecto

```bash
GESTION_DE_PASARELAS/
│
├── blacklog/
├── config/
├── core/
├── frontent/
├── docs/
├── test/  
├── env
├── requirements.txt
├── README.md
└── manage.py
