# Factory ERP - Setup & Configuration Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Initial Setup

### Step 1: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install django
# Optional but recommended
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install django-filter
pip install djangorestframework
```

### Step 3: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
# Follow the prompts to create admin account
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

Access the application at: `http://localhost:8000`

---

## Configuration

### Update settings.py

The following have been configured automatically:

1. **Added ERP App:**
```python
INSTALLED_APPS = [
    ...
    'erp.apps.ErpConfig',
]
```

2. **Set Custom User Model:**
```python
AUTH_USER_MODEL = 'erp.User'
```

3. **Included ERP URLs:**
```python
# In urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('erp.urls')),
]
```

---

## Running Common Commands

### Create/Update Models
```bash
python manage.py makemigrations
python manage.py migrate
```

### Access Django Admin
1. Run: `python manage.py runserver`
2. Visit: `http://localhost:8000/admin/`
3. Login with superuser credentials

### Create Test Data
```bash
python manage.py shell
```

Then in the Python shell:
```python
from erp.models import Vendor, Product, Material

# Create a vendor
vendor = Vendor.objects.create(
    name='Test Vendor',
    contact='John Doe',
    phone='1234567890',
    email='vendor@test.com',
    address='123 Test Street'
)

# Create a material
material = Material.objects.create(
    name='Steel Sheet',
    sku='MAT-001',
    unit='kg',
    unit_cost=50.00
)

# Create a product
product = Product.objects.create(
    name='Industrial Component',
    sku='PROD-001',
    price=150.00
)

print("Test data created successfully!")
exit()
```

---

## Project Structure

```
FactoryERP/
├── manage.py                 # Django management script
├── MODELS_README.md         # Models documentation
├── SETUP_GUIDE.md           # This file
├── FactoryERP/              # Project configuration folder
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
├── erp/                     # ERP Application
│   ├── migrations/          # Database migrations
│   │   └── __init__.py
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── forms.py             # Django forms
│   ├── models.py            # All database models
│   ├── tests.py             # Unit tests
│   ├── urls.py              # ERP URL patterns
│   └── views.py             # View classes
└── venv/                    # Virtual environment (after creation)
```

---

## Database Models

The ERP system includes the following models:

1. **User** - Custom user with role-based access
2. **Vendor** - Supplier information
3. **Product** - Product catalog
4. **Material** - Raw materials
5. **ProductMaterial** - Bill of Materials
6. **Quotation** - Vendor quotations
7. **WorkOrder** - Manufacturing orders
8. **WorkOrderMaterial** - Materials for work orders
9. **Inventory** - Stock levels
10. **PurchaseOrder** - PO to vendors
11. **StockIn** - Receiving materials
12. **ProductionLog** - Production records
13. **QCReport** - Quality control reports
14. **FinishedGoods** - Completed products
15. **StockOut** - Outgoing inventory

---

## Key Features Implemented

### Authentication & Authorization
- Custom User model with role-based access control
- Roles: admin, manager, supervisor, operator, viewer
- Integration-ready with Django's auth system

### Inventory Management
- Material and product tracking
- Reorder level monitoring
- Stock in/out logging

### Production Workflow
- Quotation management
- Work order creation and tracking
- Material requirements calculation
- Production logging
- Quality control reporting

### Cost Tracking
- Material costs
- Labor costs
- Machine/equipment costs
- Overhead allocation
- Per-piece cost calculation

### Supply Chain
- Vendor management
- Purchase order generation
- Receiving/stock-in tracking

---

## Admin Interface

Access Django Admin at: `http://localhost:8000/admin/`

All models are registered in the admin interface with:
- List views with appropriate filters and search
- Inline editing for related models
- Read-only fields for calculated values
- Custom admin classes for better UX

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** 
```bash
pip install django
```

### Issue: "No changes detected in app 'erp'"
**Solution:** 
```bash
python manage.py makemigrations erp
python manage.py migrate
```

### Issue: "django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'erp.User' that has not been installed"
**Solution:** Ensure `'erp.apps.ErpConfig'` is in INSTALLED_APPS before running migrations

### Issue: Migrations conflicts
**Solution:**
```bash
# Delete all migration files except __init__.py
# Then:
python manage.py makemigrations
python manage.py migrate
```

---

## Next Steps

1. Create HTML templates in `erp/templates/` for views
2. Implement API endpoints using Django REST Framework (optional)
3. Add authentication views (login, logout, registration)
4. Configure static files for CSS/JavaScript
5. Set up email configuration for notifications
6. Implement reporting features
7. Add data export functionality (CSV, PDF)

---

## Documentation Links

- Django Official Docs: https://docs.djangoproject.com/
- Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Django Admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/
- Django Views: https://docs.djangoproject.com/en/stable/topics/http/views/

---

## Support

For model structure reference, see **MODELS_README.md**

For API endpoint information, see **MODELS_README.md** - API Endpoints section
