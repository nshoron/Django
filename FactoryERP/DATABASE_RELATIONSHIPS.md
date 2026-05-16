# Factory ERP - Database Relationship Diagram

## Entity Relationship Diagram (ASCII)

```
                            ┌─────────────┐
                            │    User     │
                            ├─────────────┤
                            │ id (PK)     │
                            │ username    │
                            │ email       │
                            │ role        │
                            └─────────────┘
                                   △
                    ┌──────────────┼──────────────┐
                    │              │              │
                    │ (created_by) │ (created_by) │ (created_by)
                    │              │              │
        ┌───────────▼────┐  ┌──────▼─────┐  ┌────▼──────┐
        │  Quotation     │  │  WorkOrder │  │PurchaseOrder│
        ├────────────────┤  ├────────────┤  ├────────────┤
        │ id (PK)        │  │ id (PK)    │  │ id (PK)    │
        │ vendor_id (FK) │  │ product_id │  │ vendor_id  │
        │ product_id (FK)│  │ quotation_ │  │ work_order_│
        │ quotation_no   │  │ id (FK)    │  │ id (FK)    │
        │ quantity       │  │ quantity   │  │ po_no      │
        │ unit_price     │  │ material_  │  │ total_      │
        │ total_price    │  │ cost       │  │ amount     │
        │ status         │  │ labor_cost │  │ status     │
        └────────────────┘  │ machine_   │  │ order_date │
             △              │ cost       │  └────────────┘
             │              │ overhead_  │         △
             │              │ cost       │         │
             │              │ total_cost │    (work_order_id)
             │              │ per_piece_ │         │
         (vendor_id)         │ cost       │  ┌──────▼──────┐
             │              │ status     │  │  StockIn    │
             │              │ deadline   │  ├─────────────┤
        ┌────▼────────┐     └────────────┘  │ id (PK)     │
        │   Vendor    │          △          │ purchase_   │
        ├─────────────┤          │          │ order_id(FK)│
        │ id (PK)     │   (quotation_id)    │ material_   │
        │ name        │          │          │ id (FK)     │
        │ contact     │     ┌────▼──────────┤ quantity    │
        │ phone       │     │               │ received_   │
        │ email       │     │               │ date        │
        │ address     │     │               └─────────────┘
        └─────────────┘     │
                            │
                    ┌───────▼────────┐
                    │   WorkOrder    │
                    │   (continued)  │
                    └────────────────┘
                            △
            ┌───────────────┼───────────────┐
            │               │               │
        (work_order_id) (work_order_id) (work_order_id)
            │               │               │
    ┌───────▼──────┐  ┌─────▼────────┐ ┌───▼──────────┐
    │Production    │  │  QCReport    │ │FinishedGoods │
    │Log           │  ├──────────────┤ ├──────────────┤
    ├──────────────┤  │ id (PK)      │ │ id (PK)      │
    │ id (PK)      │  │ work_order_  │ │ work_order_  │
    │ work_order_  │  │ id (FK)      │ │ id (FK)      │
    │ id (FK)      │  │ passed_qty   │ │ product_id   │
    │ start_time   │  │ damaged_qty  │ │ (FK)         │
    │ end_time     │  │ remarks      │ │ quantity     │
    │ produced_qty │  │ status       │ │ created_at   │
    │ status       │  └──────────────┘ └──────────────┘
    └──────────────┘

                    ┌──────────────┐
                    │   Product    │
                    ├──────────────┤
                    │ id (PK)      │
                    │ name         │
                    │ sku          │
                    │ price        │
                    └──────────────┘
                            △
            ┌───────────────┼───────────────┐
            │               │               │
        (product_id)    (product_id)   (product_id)
            │               │               │
    ┌───────▼──────────┐ ┌──▼─────────┐ ┌──▼────────┐
    │ProductMaterial   │ │ Inventory  │ │ StockOut  │
    ├──────────────────┤ ├────────────┤ ├───────────┤
    │ id (PK)          │ │ id (PK)    │ │ id (PK)   │
    │ product_id (FK)  │ │ material_  │ │ product_  │
    │ material_id (FK) │ │ id (FK)    │ │ id (FK)   │
    │ required_qty     │ │ product_id │ │ quantity  │
    └──────────────────┘ │ (FK)       │ │ out_date  │
            △            │ quantity   │ │ destina-  │
            │            │ reorder_   │ │ tion      │
        (material_id)     │ level      │ └───────────┘
            │             └────────────┘
            │
    ┌───────▼──────────┐
    │   Material       │
    ├──────────────────┤
    │ id (PK)          │
    │ name             │
    │ sku              │
    │ unit             │
    │ unit_cost        │
    └──────────────────┘
```

## Detailed Relationship Map

### Core Entities

#### Users & Permissions
- **User** (Central authentication hub)
  - Role-based access control
  - Audit trail for created/approved records

#### Master Data
- **Product** (Product catalog)
- **Material** (Raw materials)
- **Vendor** (Supplier information)

#### Linking Tables
- **ProductMaterial** (Many-to-Many: Products ↔ Materials - BOM)

### Operational Workflow

#### Sales & Planning
1. **Quotation** (Vendor quotes)
   - Links: Vendor → Quotation ← Product
   - Created by: User

2. **WorkOrder** (Production order)
   - From: Quotation (optional)
   - For: Product
   - Created by: User

#### Materials Management
3. **WorkOrderMaterial** (Required materials per WO)
   - Links: WorkOrder ← WorkOrderMaterial → Material
   - Auto-calculates: total_cost = required_qty × material.unit_cost

4. **Inventory** (Stock tracking)
   - Tracks: Material OR Product
   - Features: Reorder level monitoring

#### Purchase & Receiving
5. **PurchaseOrder** (PO to vendors)
   - From: Vendor
   - For: WorkOrder (optional)
   - Created by: User
   - Approved by: User

6. **StockIn** (Material receipt)
   - Links: PurchaseOrder ← StockIn → Material
   - Updates: Inventory quantity

#### Production & Quality
7. **ProductionLog** (Production record)
   - Tracks: WorkOrder production activity
   - Records: Start/end time, quantity produced
   - Created by: User

8. **QCReport** (Quality control)
   - Tracks: WorkOrder QC inspection
   - Records: Passed/damaged quantities
   - Created by: User

9. **FinishedGoods** (Completed inventory)
   - Links: WorkOrder ← FinishedGoods → Product
   - Created from: Passed QC → Production

#### Distribution
10. **StockOut** (Shipment record)
    - Tracks: Product outgoing
    - Records: Quantity, destination, date
    - Related to: WorkOrder (optional)

---

## Relationship Types

### One-to-Many (1:N)
- User → Quotations
- User → WorkOrders
- User → PurchaseOrders
- Vendor → Quotations
- Vendor → PurchaseOrders
- Product → WorkOrders
- Product → Quotations
- Material → ProductMaterials
- Quotation → WorkOrders
- WorkOrder → WorkOrderMaterials
- WorkOrder → PurchaseOrders
- WorkOrder → ProductionLogs
- WorkOrder → QCReports
- WorkOrder → FinishedGoods
- WorkOrder → StockOuts
- PurchaseOrder → StockIns
- Inventory (by material or product)

### Many-to-Many (M:N)
- Products ↔ Materials (through ProductMaterial)

### Optional Relationships (FK with null=True)
- WorkOrder → Quotation (can create WO without quotation)
- WorkOrder → User (can be set to null if user deleted)
- StockOut → WorkOrder (optional association)

---

## Data Flow Example: Complete Production Cycle

```
1. QUOTATION PHASE
   Vendor → Quotation ← Product
   ↓
2. PLANNING PHASE
   Quotation → WorkOrder (with Product)
   WorkOrder → WorkOrderMaterial ← Material (from BOM)
   ↓
3. PROCUREMENT PHASE
   WorkOrder → PurchaseOrder → Vendor
   ↓
4. RECEIVING PHASE
   PurchaseOrder → StockIn → Material
   Material → Inventory (quantity updated)
   ↓
5. PRODUCTION PHASE
   WorkOrder → ProductionLog (production activity)
   ↓
6. QUALITY CONTROL PHASE
   WorkOrder → QCReport (inspection results)
   ↓
7. FINISHED GOODS PHASE
   WorkOrder → FinishedGoods → Product
   FinishedGoods → Inventory
   ↓
8. DISTRIBUTION PHASE
   Product → StockOut (shipment record)
   Inventory (quantity updated)
```

---

## Database Constraints & Rules

### Unique Constraints
- `Product.sku` - Unique
- `Material.sku` - Unique
- `Quotation.quotation_no` - Unique
- `WorkOrder.work_order_no` - Unique
- `PurchaseOrder.po_no` - Unique
- `ProductMaterial(product, material)` - Combined unique
- `WorkOrderMaterial(work_order, material)` - Combined unique

### Calculated Fields (Auto-Updated)
- `Quotation.total_price` = quantity × unit_price
- `WorkOrder.total_cost` = material_cost + labor_cost + machine_cost + overhead_cost
- `WorkOrder.per_piece_cost` = total_cost / quantity
- `WorkOrderMaterial.total_cost` = required_qty × material.unit_cost
- `Inventory.is_low_stock()` = quantity ≤ reorder_level

### Timestamps (Auto-Managed)
- `created_at` - Set on creation
- `updated_at` - Updated on modification
- `received_date` - Set on StockIn creation
- `out_date` - Set on StockOut creation

---

## Access Patterns (Query Optimization)

### Common Queries
```python
# Get all materials for a product
product.materials.all()

# Get all work orders for a quotation
quotation.work_orders.all()

# Get inventory status
inventory = Inventory.objects.filter(is_low_stock=True)

# Get pending quotations
quotations = Quotation.objects.filter(status='draft')

# Get active work orders
work_orders = WorkOrder.objects.filter(status__in=['planned', 'in_progress'])

# Get purchase orders awaiting approval
pos = PurchaseOrder.objects.filter(status='submitted')

# Get completed work orders with their QC reports
work_orders = WorkOrder.objects.filter(status='completed').prefetch_related('qc_reports')

# Get finished goods by work order
finished = FinishedGoods.objects.filter(work_order__status='completed')
```

---

## Related Model Queries

### Bill of Materials (BOM)
```
Product → ProductMaterial → Material
```
Get materials needed for a product with quantities

### Work Order Materials
```
WorkOrder → WorkOrderMaterial → Material
```
Get materials for a specific work order (may differ from BOM)

### Production to Quality
```
WorkOrder → ProductionLog (production records)
WorkOrder → QCReport (quality inspection)
WorkOrder → FinishedGoods (output)
```

### Complete Supply Chain
```
Quotation → WorkOrder → PurchaseOrder → StockIn → Inventory → FinishedGoods → StockOut
```

---

## Performance Considerations

1. **Use select_related()** for foreign keys (1:1 relationships)
2. **Use prefetch_related()** for reverse relations (1:N, M:N)
3. **Index frequently searched fields**: `sku`, `status`, `created_at`
4. **Batch operations** for bulk updates
5. **Archive old records** for historical data

---

See **MODELS_README.md** for detailed field descriptions of each model.
