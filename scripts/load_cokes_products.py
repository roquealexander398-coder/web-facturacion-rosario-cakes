import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facturacion.settings')
django.setup()

from apps.products.models import Category, Product


def run():
    category, _ = Category.objects.get_or_create(
        name='Cokes',
        defaults={
            'description': 'Variedades de cokes y refrescos para venta',
            'is_active': True,
        },
    )

    products = [
        ('COKE-001', 'Coca Cola 350ml', 80, 50, 10),
        ('COKE-002', 'Coca Cola Zero 350ml', 85, 50, 10),
        ('COKE-003', 'Sprite 350ml', 75, 50, 10),
        ('COKE-004', 'Fanta Naranja 350ml', 75, 50, 10),
        ('COKE-005', 'Pepsi 350ml', 70, 50, 10),
        ('COKE-006', 'Mirinda 350ml', 70, 50, 10),
        ('COKE-007', 'Coca Cola 500ml', 110, 40, 10),
        ('COKE-008', 'Sprite 500ml', 100, 35, 10),
    ]

    for code, name, price, stock, min_stock in products:
        Product.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'description': 'Producto de ejemplo para ventas de cokes',
                'category': category,
                'price': price,
                'cost': round(price * 0.70, 2),
                'stock': stock,
                'min_stock': min_stock,
                'max_stock': 200,
                'is_active': True,
            },
        )

    print('Productos de cokes cargados correctamente.')


if __name__ == '__main__':
    run()
