# Factory ERP - Individual Apps Structure

## 📦 Complete Refactor to Individual Apps

All 15 models have been reorganized into **9 individual, independent Django apps**, each with its own models, views, forms, admin configuration, and URL routing.

---

## Project Structure

```
FactoryERP/
├── manage.py
├── FactoryERP/                 # Project Configuration
│   ├── __init__.py
│   ├── settings.py             # ✅ Updated with 9 apps
│   ├── urls.py                 # ✅ Central URL routing
│   ├── views.py                # ✅ Dashboard view
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                   # 1️⃣ ACCOUNTS APP - User Management
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # AccountsConfig
│   ├── models.py               # User
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── masters/                    # 2️⃣ MASTERS APP - Master Data
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # MastersConfig
│   ├── models.py               # Vendor, Product, Material, ProductMaterial
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── quotations/                 # 3️⃣ QUOTATIONS APP - Vendor Quotations
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # QuotationsConfig
│   ├── models.py               # Quotation
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── work_orders/                # 4️⃣ WORK ORDERS APP - Production Orders
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # WorkOrdersConfig
│   ├── models.py               # WorkOrder, WorkOrderMaterial
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── inventory/                  # 5️⃣ INVENTORY APP - Stock Management
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # InventoryConfig
│   ├── models.py               # Inventory
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── purchasing/                 # 6️⃣ PURCHASING APP - Purchase Orders
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # PurchasingConfig
│   ├── models.py               # PurchaseOrder, StockIn
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── production/                 # 7️⃣ PRODUCTION APP - Production & QC
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # ProductionConfig
│   ├── models.py               # ProductionLog, QCReport
│   ├── admin.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── finished_goods/             # 8️⃣ FINISHED GOODS APP - Output Tracking
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # FinishedGoodsConfig
│   ├── models.py               # FinishedGoods
│   ├── admin.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
├── stock/                      # 9️⃣ STOCK APP - Distribution
│   ├── migrations/
│   ├── __init__.py
│   ├── apps.py                 # StockConfig
│   ├── models.py               # StockOut
│   ├── admin.py
│   ├── forms.py
│   ├── urls.py
│   └── tests.py
│
└── erp/                        # ❌ OLD (Can be deleted)
    └── (Previous monolithic app - superseded)
```

---

## 9 Individual Apps

### 1️⃣ **accounts** - Authentication & User Management
**Models:** User
- Role-based access control
- 5 user roles: admin, manager, supervisor, operator, viewer
- Admin configuration for user management
- Forms for user operations

**URL Prefix:** `/accounts/`

---

### 2️⃣ **masters** - Master Data (Reference Data)
**Models:** Vendor, Product, Material, ProductMaterial (BOM)
- Vendor/supplier information
- Product catalog
- Material inventory
- Bill of Materials (Product-Material relationships)
- Views for listing and detail
- Full admin integration

**URL Prefix:** `/masters/`
- `/masters/products/` - Product list
- `/masters/products/<id>/` - Product detail
- `/masters/materials/` - Material list
- `/masters/materials/<id>/` - Material detail
- `/masters/vendors/` - Vendor list
- `/masters/vendors/<id>/` - Vendor detail

---

### 3️⃣ **quotations** - Vendor Quotations
**Models:** Quotation
- Vendor quote tracking
- Status workflow: draft → submitted → accepted/rejected/expired
- Auto-calculated totals
- Linked to vendors and products
- Created by user audit trail

**URL Prefix:** `/quotations/`
- `/quotations/` - List
- `/quotations/<id>/` - Detail

---

### 4️⃣ **work_orders** - Manufacturing Work Orders
**Models:** WorkOrder, WorkOrderMaterial
- Production order creation and tracking
- Multi-level cost tracking (material, labor, machine, overhead)
- Auto-calculated total and per-piece costs
- Material requirements per work order
- Status workflow: draft → planned → in_progress → completed/cancelled
- Inline material editing in admin

**URL Prefix:** `/work-orders/`
- `/work-orders/` - List
- `/work-orders/<id>/` - Detail with materials

---

### 5️⃣ **inventory** - Stock Level Management
**Models:** Inventory
- Tracks both material and product inventory
- Quantity and reorder level management
- Low stock detection
- Separate entries for materials and products

**URL Prefix:** `/inventory/`
- `/inventory/` - List all inventory

---

### 6️⃣ **purchasing** - Purchase Order Management
**Models:** PurchaseOrder, StockIn
- Purchase orders to vendors
- Approval workflow (created_by, approved_by)
- Material receiving (Stock In) tracking
- Status workflow: draft → submitted → confirmed → received/cancelled
- Linked to work orders

**URL Prefix:** `/purchasing/`
- `/purchasing/purchase-orders/` - PO list
- `/purchasing/purchase-orders/<id>/` - PO detail with stock ins

---

### 7️⃣ **production** - Production & Quality Control
**Models:** ProductionLog, QCReport
- Production activity logging (start/end times)
- Quality control reporting
- Pass/fail/damage tracking
- Status management for both logs and QC
- Created by user audit trail

**URL Prefix:** `/production/`
- `/production/production-logs/` - Production log list
- `/production/qc-reports/` - QC report list
- `/production/qc-reports/<id>/` - QC report detail

---

### 8️⃣ **finished_goods** - Finished Product Tracking
**Models:** FinishedGoods
- Tracks completed products from work orders
- Links production output to finished goods inventory
- Quantity recording with timestamp

**URL Prefix:** `/finished-goods/`

---

### 9️⃣ **stock** - Stock Out / Distribution
**Models:** StockOut
- Shipment/outgoing inventory tracking
- Destination logging
- Links to work orders (optional)
- Auto-timestamped shipment date

**URL Prefix:** `/stock/`

---

## Key Changes from Monolithic to Individual Apps

### ✅ What's Better with Individual Apps

1. **Separation of Concerns**
   - Each app has a specific responsibility
   - Easier to understand and modify
   - Clear module boundaries

2. **Scalability**
   - Each app can be developed independently
   - Easy to add new features to specific areas
   - Reusable in other projects

3. **Testing**
   - Tests isolated to each app's domain
   - Easier to test specific functionality
   - Better test organization

4. **Maintenance**
   - Easier to debug issues in specific areas
   - Clear where code belongs
   - Reduced file sizes (no 500+ line models.py)

5. **Team Development**
   - Multiple developers can work on different apps
   - No merge conflicts in giant files
   - Clear ownership of app areas

6. **Dependency Management**
   - Clear import paths
   - Easy to track app dependencies
   - Can visualize app relationships

---

## Database Relationships Between Apps

```
accounts
    └── User

masters
    ├── Vendor
    ├── Product
    ├── Material
    └── ProductMaterial (M:M between Product & Material)

quotations
    ├── Quotation (vendor → Vendor, product → Product, created_by → User)
    └── → work_orders.WorkOrder

work_orders
    ├── WorkOrder (quotation → Quotation, product → Product, created_by → User)
    ├── WorkOrderMaterial (material → Material)
    └── → purchasing, production, finished_goods, stock apps

inventory
    └── Inventory (material → Material, product → Product)

purchasing
    ├── PurchaseOrder (vendor → Vendor, work_order → WorkOrder, created_by → User)
    └── StockIn (material → Material)

production
    ├── ProductionLog (work_order → WorkOrder, created_by → User)
    └── QCReport (work_order → WorkOrder, created_by → User)

finished_goods
    └── FinishedGoods (work_order → WorkOrder, product → Product)

stock
    └── StockOut (product → Product, work_order → WorkOrder)
```

---

## Updated settings.py

All 9 apps added to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Individual ERP Apps
    'accounts.apps.AccountsConfig',
    'masters.apps.MastersConfig',
    'quotations.apps.QuotationsConfig',
    'work_orders.apps.WorkOrdersConfig',
    'inventory.apps.InventoryConfig',
    'purchasing.apps.PurchasingConfig',
    'production.apps.ProductionConfig',
    'finished_goods.apps.FinishedGoodsConfig',
    'stock.apps.StockConfig',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'
```

---

## Central URL Routing (urls.py)

```python
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    
    # Individual App URLs
    path('accounts/', include('accounts.urls')),
    path('masters/', include('masters.urls')),
    path('quotations/', include('quotations.urls')),
    path('work-orders/', include('work_orders.urls')),
    path('inventory/', include('inventory.urls')),
    path('purchasing/', include('purchasing.urls')),
    path('production/', include('production.urls')),
    path('finished-goods/', include('finished_goods.urls')),
    path('stock/', include('stock.urls')),
]
```

---

## Admin Interface by App

Each app has complete admin configuration:

| App | Admin URLs | Models |
|-----|-----------|--------|
| accounts | `/admin/accounts/user/` | User (1) |
| masters | `/admin/masters/` | Vendor, Product, Material, ProductMaterial (4) |
| quotations | `/admin/quotations/quotation/` | Quotation (1) |
| work_orders | `/admin/work_orders/` | WorkOrder, WorkOrderMaterial (2) |
| inventory | `/admin/inventory/inventory/` | Inventory (1) |
| purchasing | `/admin/purchasing/` | PurchaseOrder, StockIn (2) |
| production | `/admin/production/` | ProductionLog, QCReport (2) |
| finished_goods | `/admin/finished_goods/` | FinishedGoods (1) |
| stock | `/admin/stock/stockout/` | StockOut (1) |

---

## App Dependencies

```
accounts (base - no dependencies)
    ↓
masters (depends: accounts)
    ↓
quotations (depends: masters, accounts)
    ↓
work_orders (depends: quotations, masters, accounts)
    ↓
├── inventory (depends: masters)
├── purchasing (depends: masters, work_orders, accounts)
├── production (depends: work_orders, accounts)
├── finished_goods (depends: work_orders, masters)
└── stock (depends: masters, work_orders)
```

---

## Migration Order

When running migrations, ensure you apply them in this order:
```bash
python manage.py migrate accounts
python manage.py migrate masters
python manage.py migrate quotations
python manage.py migrate work_orders
python manage.py migrate inventory
python manage.py migrate purchasing
python manage.py migrate production
python manage.py migrate finished_goods
python manage.py migrate stock
```

Or simply:
```bash
python manage.py migrate  # Applies all in correct order
```

---

## Quick Setup

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install Django
pip install django

# 3. Run migrations (all apps)
python manage.py makemigrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver

# 6. Access:
# Dashboard: http://localhost:8000/
# Admin: http://localhost:8000/admin/
# API: http://localhost:8000/masters/products/
```

---

## What to Delete

The old monolithic `erp/` app can be deleted:
```bash
rm -r erp/  # Remove old erp directory
```

All functionality has been migrated to the 9 individual apps.

---

## Next Steps

1. ✅ Create migrations for all apps
2. ✅ Run migrations to create database
3. ✅ Create superuser account
4. ✅ Load test data (if needed)
5. Create HTML templates for views
6. Add CSS/JavaScript styling
7. Implement additional business logic
8. Add API endpoints (Django REST Framework - optional)
9. Deploy to production

---

## Summary

**Before:** 1 monolithic `erp/` app with 15 models
**After:** 9 individual apps, each with focused responsibility
**Models:** 15 models distributed logically across 9 apps
**Code Quality:** Better maintainability, testability, and scalability
**Team Development:** Easy parallel development across apps

Each app is **completely independent** with its own:
- ✅ models.py
- ✅ admin.py
- ✅ forms.py
- ✅ views.py
- ✅ urls.py
- ✅ tests.py
- ✅ apps.py
- ✅ migrations/

**Status: READY FOR MIGRATION** 🚀
