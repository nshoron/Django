# Factory ERP - Models Quick Reference

## Model Summary Table

| Model | Purpose | Key Fields | Key Relations |
|-------|---------|-----------|----------------|
| **User** | Authentication & Authorization | username, email, role | Quotations, WorkOrders, PurchaseOrders, ProductionLogs, QCReports |
| **Vendor** | Supplier Information | name, contact, phone, email, address | Quotations, PurchaseOrders |
| **Product** | Product Catalog | sku, name, price | ProductMaterials, Quotations, WorkOrders, FinishedGoods, StockOut, Inventory |
| **Material** | Raw Materials | sku, name, unit, unit_cost | ProductMaterials, WorkOrderMaterials, StockIn, Inventory |
| **ProductMaterial** | Bill of Materials | product_id, material_id, required_qty | Product ↔ Material (M:M) |
| **Quotation** | Vendor Quotes | quotation_no, quantity, unit_price, status | Vendor, Product, WorkOrders |
| **WorkOrder** | Production Order | work_order_no, quantity, status, deadline | Quotation, Product, WorkOrderMaterials, PurchaseOrders, ProductionLogs, QCReports |
| **WorkOrderMaterial** | WO Materials | work_order_id, material_id, required_qty | WorkOrder, Material |
| **Inventory** | Stock Tracking | quantity, reorder_level, inventory_type | Material or Product |
| **PurchaseOrder** | Purchase Order | po_no, total_amount, status, order_date | Vendor, WorkOrder, StockIns |
| **StockIn** | Material Receipt | quantity, received_date | PurchaseOrder, Material |
| **ProductionLog** | Production Record | produced_qty, status, start_time, end_time | WorkOrder |
| **QCReport** | Quality Control | passed_qty, damaged_qty, status, remarks | WorkOrder |
| **FinishedGoods** | Completed Products | quantity, created_at | WorkOrder, Product |
| **StockOut** | Outgoing Inventory | quantity, destination, out_date | Product, WorkOrder (opt) |

---

## Model Field Reference

### User Model
```python
class User(AbstractUser):
    role = CharField(choices=['admin','manager','supervisor','operator','viewer'])
    is_active = BooleanField()
```

### Vendor Model
```python
class Vendor:
    name: str (max 255)
    contact: str (max 255)
    phone: str (max 20)
    email: EmailField
    address: TextField
```

### Product Model
```python
class Product:
    sku: str (max 100, unique)
    name: str (max 255)
    price: Decimal(10,2)
    description: TextField (optional)
```

### Material Model
```python
class Material:
    sku: str (max 100, unique)
    name: str (max 255)
    unit: str (max 50)  # kg, liter, pieces, etc.
    unit_cost: Decimal(10,2)
    description: TextField (optional)
```

### ProductMaterial Model (BOM)
```python
class ProductMaterial:
    product: ForeignKey(Product)
    material: ForeignKey(Material)
    required_qty: Decimal(10,2)
    # Unique: (product, material)
```

### Quotation Model
```python
class Quotation:
    vendor: ForeignKey(Vendor)
    product: ForeignKey(Product)
    quotation_no: str (max 100, unique)
    quantity: int
    unit_price: Decimal(10,2)
    total_price: Decimal(12,2)  # auto-calculated
    status: str (choices: draft, submitted, accepted, rejected, expired)
    created_by: ForeignKey(User)
```

### WorkOrder Model
```python
class WorkOrder:
    quotation: ForeignKey(Quotation, optional)
    product: ForeignKey(Product)
    work_order_no: str (max 100, unique)
    quantity: int
    material_cost: Decimal(12,2)
    labor_cost: Decimal(12,2)
    machine_cost: Decimal(12,2)
    overhead_cost: Decimal(12,2)
    total_cost: Decimal(12,2)  # auto-calculated
    per_piece_cost: Decimal(10,2)  # auto-calculated
    status: str (choices: draft, planned, in_progress, completed, cancelled)
    deadline: Date
    created_by: ForeignKey(User)
```

### WorkOrderMaterial Model
```python
class WorkOrderMaterial:
    work_order: ForeignKey(WorkOrder)
    material: ForeignKey(Material)
    required_qty: Decimal(10,2)
    total_cost: Decimal(12,2)  # auto-calculated (qty × unit_cost)
    # Unique: (work_order, material)
```

### Inventory Model
```python
class Inventory:
    material: ForeignKey(Material, optional)
    product: ForeignKey(Product, optional)
    inventory_type: str (choices: material, product)
    quantity: Decimal(12,2)
    reorder_level: Decimal(10,2)
    # Unique: (material, product, inventory_type)
```

### PurchaseOrder Model
```python
class PurchaseOrder:
    vendor: ForeignKey(Vendor)
    work_order: ForeignKey(WorkOrder, optional)
    po_no: str (max 100, unique)
    total_amount: Decimal(12,2)
    status: str (choices: draft, submitted, confirmed, received, cancelled)
    order_date: Date
    created_by: ForeignKey(User)
    approved_by: ForeignKey(User, optional)
```

### StockIn Model
```python
class StockIn:
    purchase_order: ForeignKey(PurchaseOrder)
    material: ForeignKey(Material)
    quantity: Decimal(12,2)
    received_date: DateTime  # auto-set
```

### ProductionLog Model
```python
class ProductionLog:
    work_order: ForeignKey(WorkOrder)
    start_time: DateTime
    end_time: DateTime (optional)
    produced_qty: int
    status: str (choices: in_progress, paused, completed, aborted)
    created_by: ForeignKey(User)
```

### QCReport Model
```python
class QCReport:
    work_order: ForeignKey(WorkOrder)
    passed_qty: int
    damaged_qty: int
    remarks: TextField (optional)
    status: str (choices: pending, passed, failed, partial)
    created_by: ForeignKey(User)
```

### FinishedGoods Model
```python
class FinishedGoods:
    work_order: ForeignKey(WorkOrder)
    product: ForeignKey(Product)
    quantity: int
    created_at: DateTime  # auto-set
```

### StockOut Model
```python
class StockOut:
    product: ForeignKey(Product)
    quantity: int
    out_date: DateTime  # auto-set
    destination: str (max 255)
    work_order: ForeignKey(WorkOrder, optional)
```

---

## Common Operations

### Create a Quotation
```python
from erp.models import Quotation, Vendor, Product, User

vendor = Vendor.objects.get(id=1)
product = Product.objects.get(sku='PROD-001')
user = User.objects.get(username='admin')

quotation = Quotation.objects.create(
    vendor=vendor,
    product=product,
    quotation_no='QT-001',
    quantity=100,
    unit_price=50.00,
    status='submitted',
    created_by=user
)
# total_price automatically set to 5000.00
```

### Create a Work Order
```python
from datetime import date, timedelta
from erp.models import WorkOrder, Product, User

product = Product.objects.get(sku='PROD-001')
user = User.objects.get(username='admin')

work_order = WorkOrder.objects.create(
    product=product,
    work_order_no='WO-001',
    quantity=50,
    material_cost=500,
    labor_cost=300,
    machine_cost=200,
    overhead_cost=100,
    deadline=date.today() + timedelta(days=7),
    created_by=user
)
# total_cost = 1100, per_piece_cost = 22.00 (auto-calculated)
```

### Add Materials to Work Order
```python
from erp.models import WorkOrderMaterial, WorkOrder, Material

work_order = WorkOrder.objects.get(work_order_no='WO-001')
material = Material.objects.get(sku='MAT-001')

wom = WorkOrderMaterial.objects.create(
    work_order=work_order,
    material=material,
    required_qty=100  # kg or other unit
)
# total_cost automatically calculated
```

### Create Purchase Order
```python
from erp.models import PurchaseOrder, Vendor, WorkOrder, User

vendor = Vendor.objects.get(id=1)
work_order = WorkOrder.objects.get(work_order_no='WO-001')
user = User.objects.get(username='admin')

po = PurchaseOrder.objects.create(
    vendor=vendor,
    work_order=work_order,
    po_no='PO-001',
    total_amount=5000.00,
    status='submitted',
    order_date=date.today(),
    created_by=user
)
```

### Receive Stock
```python
from erp.models import StockIn, PurchaseOrder, Material

po = PurchaseOrder.objects.get(po_no='PO-001')
material = Material.objects.get(sku='MAT-001')

stock_in = StockIn.objects.create(
    purchase_order=po,
    material=material,
    quantity=100  # received quantity
)
# received_date automatically set to now
```

### Log Production
```python
from datetime import datetime
from erp.models import ProductionLog, WorkOrder, User

work_order = WorkOrder.objects.get(work_order_no='WO-001')
user = User.objects.get(username='operator')

log = ProductionLog.objects.create(
    work_order=work_order,
    start_time=datetime.now(),
    produced_qty=45,
    status='in_progress',
    created_by=user
)
```

### Record QC Results
```python
from erp.models import QCReport, WorkOrder, User

work_order = WorkOrder.objects.get(work_order_no='WO-001')
user = User.objects.get(username='qc_inspector')

qc = QCReport.objects.create(
    work_order=work_order,
    passed_qty=45,
    damaged_qty=0,
    remarks='All units passed inspection',
    status='passed',
    created_by=user
)
```

### Create Finished Goods
```python
from erp.models import FinishedGoods, WorkOrder, Product

work_order = WorkOrder.objects.get(work_order_no='WO-001')
product = work_order.product

finished = FinishedGoods.objects.create(
    work_order=work_order,
    product=product,
    quantity=45  # passed quantity from QC
)
```

### Record Stock Out
```python
from erp.models import StockOut, Product, WorkOrder

product = Product.objects.get(sku='PROD-001')
work_order = WorkOrder.objects.get(work_order_no='WO-001')

stock_out = StockOut.objects.create(
    product=product,
    quantity=45,
    destination='Customer XYZ',
    work_order=work_order
)
# out_date automatically set to now
```

### Query Examples
```python
from erp.models import *

# Get all pending quotations
pending_quotes = Quotation.objects.filter(status='draft')

# Get active work orders
active_wos = WorkOrder.objects.filter(status__in=['planned', 'in_progress'])

# Get low stock inventory
low_stock = Inventory.objects.filter(quantity__lte=F('reorder_level'))

# Get work order materials with total costs
wom = WorkOrderMaterial.objects.select_related('material').filter(
    work_order__work_order_no='WO-001'
)

# Get all QC reports for a work order
qc_reports = QCReport.objects.filter(work_order__work_order_no='WO-001')

# Get finished goods with product info
finished = FinishedGoods.objects.select_related('product').filter(
    work_order__status='completed'
)

# Get purchase orders awaiting approval
pending_po = PurchaseOrder.objects.filter(
    status='submitted',
    approved_by__isnull=True
)

# Get materials by product (BOM)
bom = ProductMaterial.objects.filter(product__sku='PROD-001')

# Get recent stock in records
recent_stock = StockIn.objects.order_by('-received_date')[:10]
```

---

## URLs/Endpoints

```
GET    /                              Dashboard
GET    /products/                     Product List
GET    /products/<id>/                Product Detail
GET    /materials/                    Material List
GET    /materials/<id>/               Material Detail
GET    /quotations/                   Quotation List
GET    /quotations/<id>/              Quotation Detail
GET    /work-orders/                  Work Order List
GET    /work-orders/<id>/             Work Order Detail
GET    /purchase-orders/              PO List
GET    /purchase-orders/<id>/         PO Detail
GET    /inventory/                    Inventory List
GET    /production-logs/              Production Log List
GET    /qc-reports/                   QC Report List
GET    /qc-reports/<id>/              QC Report Detail
```

---

## Admin Panel Shortcuts

- **User Administration:** `/admin/erp/user/`
- **Vendor Management:** `/admin/erp/vendor/`
- **Product Catalog:** `/admin/erp/product/`
- **Material Master:** `/admin/erp/material/`
- **Bill of Materials:** `/admin/erp/productmaterial/`
- **Quotations:** `/admin/erp/quotation/`
- **Work Orders:** `/admin/erp/workorder/`
- **Inventory:** `/admin/erp/inventory/`
- **Purchase Orders:** `/admin/erp/purchaseorder/`
- **Stock In:** `/admin/erp/stockin/`
- **Production Logs:** `/admin/erp/productionlog/`
- **QC Reports:** `/admin/erp/qcreport/`
- **Finished Goods:** `/admin/erp/finishedgoods/`
- **Stock Out:** `/admin/erp/stockout/`

---

## Status Choices Reference

### Quotation Status
- `draft` - Initial state
- `submitted` - Sent to vendor
- `accepted` - Approved
- `rejected` - Not approved
- `expired` - Out of date

### Work Order Status
- `draft` - Initial state
- `planned` - Ready for production
- `in_progress` - Currently being produced
- `completed` - Production finished
- `cancelled` - Cancelled

### Purchase Order Status
- `draft` - Initial state
- `submitted` - Sent to vendor
- `confirmed` - Acknowledged by vendor
- `received` - Items received
- `cancelled` - Cancelled

### Inventory Type
- `material` - Raw material inventory
- `product` - Finished product inventory

### Production Log Status
- `in_progress` - Currently running
- `paused` - Temporarily stopped
- `completed` - Finished
- `aborted` - Stopped abnormally

### QC Report Status
- `pending` - Awaiting inspection
- `passed` - Passed QC
- `failed` - Failed QC
- `partial` - Partial pass

### User Roles
- `admin` - Full access
- `manager` - Management functions
- `supervisor` - Supervisory tasks
- `operator` - Production operations
- `viewer` - Read-only access

---

## Tips & Best Practices

1. **Always use select_related() and prefetch_related()** for optimized queries
2. **Check reorder_level** regularly to manage inventory
3. **Use status filters** to get current/relevant records
4. **Track created_by/approved_by** for audit trails
5. **Validate data** before creating records
6. **Use transactions** for related record updates
7. **Archive old records** periodically
8. **Monitor inventory** for low stock conditions
9. **Track production metrics** through ProductionLog
10. **Document QC results** for quality assurance

---

## Files Location
- **Project:** `/FactoryERP/`
- **App:** `/FactoryERP/erp/`
- **Models:** `/FactoryERP/erp/models.py`
- **Admin:** `/FactoryERP/erp/admin.py`
- **Views:** `/FactoryERP/erp/views.py`
- **URLs:** `/FactoryERP/erp/urls.py`
- **Forms:** `/FactoryERP/erp/forms.py`

---

For more details, see:
- **MODELS_README.md** - Complete model documentation
- **DATABASE_RELATIONSHIPS.md** - Detailed relationship diagrams
- **SETUP_GUIDE.md** - Installation and setup instructions
