# Factory ERP - Django Models Documentation

## Overview
This document describes all the Django models for the Factory ERP system based on the crows-foot database schema.

## Project Structure
```
FactoryERP/
├── manage.py
├── FactoryERP/          # Project configuration
│   ├── settings.py      # Updated with 'erp' app
│   ├── urls.py          # Updated with 'erp' URLs
│   ├── wsgi.py
│   └── asgi.py
└── erp/                 # Django ERP App
    ├── migrations/      # Database migrations
    ├── models.py        # All models
    ├── views.py         # Views
    ├── urls.py          # URL patterns
    ├── forms.py         # Django Forms
    ├── admin.py         # Django Admin configuration
    ├── tests.py         # Unit tests
    ├── apps.py          # App configuration
    └── __init__.py
```

## Models Overview

### 1. User Model
**Description:** Custom user model for authentication and role-based access control.

**Fields:**
- `id` (PK) - Primary key
- `username` - Unique username
- `email` - Email address
- `password` - Encrypted password
- `role` - User role (admin, manager, supervisor, operator, viewer)
- `is_active` - Account status
- `first_name` - User's first name
- `last_name` - User's last name

**Relationships:**
- Quotations created by user
- Work orders created by user
- Purchase orders created/approved by user
- Production logs created by user
- QC reports created by user

---

### 2. Vendor Model
**Description:** Supplier information for purchasing materials and services.

**Fields:**
- `id` (PK) - Primary key
- `name` - Vendor name
- `contact` - Primary contact person
- `phone` - Phone number
- `email` - Email address
- `address` - Physical address

**Relationships:**
- Has many quotations
- Has many purchase orders

---

### 3. Product Model
**Description:** Product catalog - finished goods or product types.

**Fields:**
- `id` (PK) - Primary key
- `name` - Product name
- `sku` - Unique stock keeping unit
- `price` - Product price
- `description` - Product description

**Relationships:**
- Has many product_materials (BOM)
- Has many quotations
- Has many work orders
- Has many inventory records
- Has many finished goods
- Has many stock outs

---

### 4. Material Model
**Description:** Raw materials used in manufacturing.

**Fields:**
- `id` (PK) - Primary key
- `name` - Material name
- `sku` - Unique stock keeping unit
- `unit` - Unit of measurement (kg, liter, pieces, etc.)
- `unit_cost` - Cost per unit

**Relationships:**
- Has many product_materials (BOM)
- Has many work_order_materials
- Has many inventory records
- Has many stock ins (from purchase orders)

---

### 5. ProductMaterial Model
**Description:** Bill of Materials (BOM) - defines materials required for each product.

**Fields:**
- `id` (PK) - Primary key
- `product_id` (FK) - Reference to Product
- `material_id` (FK) - Reference to Material
- `required_qty` - Quantity of material required

**Key Points:**
- Unique constraint on (product, material) combination
- Defines what materials and quantities are needed for each product

---

### 6. Quotation Model
**Description:** Vendor quotations for materials or services.

**Fields:**
- `id` (PK) - Primary key
- `vendor_id` (FK) - Reference to Vendor
- `product_id` (FK) - Reference to Product
- `quotation_no` - Unique quotation number
- `quantity` - Quantity quoted
- `unit_price` - Price per unit
- `total_price` - Total amount (auto-calculated)
- `status` - Status (draft, submitted, accepted, rejected, expired)
- `created_by` (FK) - Reference to User
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

**Relationships:**
- Has many work orders

---

### 7. WorkOrder Model
**Description:** Manufacturing work orders - tracks production orders for products.

**Fields:**
- `id` (PK) - Primary key
- `quotation_id` (FK) - Reference to Quotation (optional)
- `product_id` (FK) - Reference to Product
- `work_order_no` - Unique work order number
- `quantity` - Quantity to produce
- `material_cost` - Cost of materials
- `labor_cost` - Labor cost
- `machine_cost` - Machine/equipment cost
- `overhead_cost` - Overhead allocation
- `total_cost` - Total cost (auto-calculated)
- `per_piece_cost` - Cost per unit (auto-calculated)
- `status` - Status (draft, planned, in_progress, completed, cancelled)
- `deadline` - Production deadline
- `created_by` (FK) - Reference to User
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

**Relationships:**
- Has many work_order_materials
- Has many purchase orders
- Has many production logs
- Has many QC reports
- Has many finished goods
- Has many stock outs

---

### 8. WorkOrderMaterial Model
**Description:** Materials required for a specific work order.

**Fields:**
- `id` (PK) - Primary key
- `work_order_id` (FK) - Reference to WorkOrder
- `material_id` (FK) - Reference to Material
- `required_qty` - Quantity required for this work order
- `total_cost` - Total cost (auto-calculated)

**Key Points:**
- Tracks specific material requirements for each work order
- Unique constraint on (work_order, material)

---

### 9. Inventory Model
**Description:** Stock levels tracking for materials and products.

**Fields:**
- `id` (PK) - Primary key
- `material_id` (FK) - Reference to Material (optional)
- `product_id` (FK) - Reference to Product (optional)
- `inventory_type` - Type (material or product)
- `quantity` - Current stock quantity
- `reorder_level` - Minimum stock level
- `updated_at` - Last update timestamp

**Key Points:**
- Tracks both material and product inventory
- Supports stock level monitoring with reorder levels

---

### 10. PurchaseOrder Model
**Description:** Purchase orders sent to vendors for material procurement.

**Fields:**
- `id` (PK) - Primary key
- `vendor_id` (FK) - Reference to Vendor
- `work_order_id` (FK) - Reference to WorkOrder (optional)
- `po_no` - Unique PO number
- `total_amount` - Total PO amount
- `status` - Status (draft, submitted, confirmed, received, cancelled)
- `order_date` - Date of order
- `created_by` (FK) - Reference to User
- `approved_by` (FK) - Reference to User (optional)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

**Relationships:**
- Has many stock_ins

---

### 11. StockIn Model
**Description:** Material receipt log - tracks incoming materials from purchase orders.

**Fields:**
- `id` (PK) - Primary key
- `purchase_order_id` (FK) - Reference to PurchaseOrder
- `material_id` (FK) - Reference to Material
- `quantity` - Quantity received
- `received_date` - Date/time received (auto-set)

---

### 12. ProductionLog Model
**Description:** Production logs - tracks production activities for each work order.

**Fields:**
- `id` (PK) - Primary key
- `work_order_id` (FK) - Reference to WorkOrder
- `start_time` - Production start time
- `end_time` - Production end time (optional)
- `produced_qty` - Quantity produced
- `status` - Status (in_progress, paused, completed, aborted)
- `created_by` (FK) - Reference to User
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

---

### 13. QCReport Model
**Description:** Quality Control reports - tracks quality inspection results.

**Fields:**
- `id` (PK) - Primary key
- `work_order_id` (FK) - Reference to WorkOrder
- `passed_qty` - Quantity passed QC
- `damaged_qty` - Quantity damaged/failed QC
- `remarks` - QC remarks/notes
- `status` - Status (pending, passed, failed, partial)
- `created_by` (FK) - Reference to User
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

---

### 14. FinishedGoods Model
**Description:** Finished goods inventory - tracks completed products from work orders.

**Fields:**
- `id` (PK) - Primary key
- `work_order_id` (FK) - Reference to WorkOrder
- `product_id` (FK) - Reference to Product
- `quantity` - Quantity of finished goods
- `created_at` - Creation timestamp

---

### 15. StockOut Model
**Description:** Stock out log - tracks outgoing products/materials.

**Fields:**
- `id` (PK) - Primary key
- `product_id` (FK) - Reference to Product
- `quantity` - Quantity shipped out
- `out_date` - Date/time of shipment (auto-set)
- `destination` - Destination location
- `work_order_id` (FK) - Reference to WorkOrder (optional)

---

## Setup Instructions

### 1. Installation
```bash
cd FactoryERP
pip install django
```

### 2. Create Migrations
```bash
python manage.py makemigrations
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run Development Server
```bash
python manage.py runserver
```

### 6. Access Django Admin
```
http://localhost:8000/admin/
```

---

## Database Relationships Summary

### One-to-Many Relationships:
- Vendor → Quotations
- Vendor → Purchase Orders
- Product → ProductMaterials
- Product → Quotations
- Product → Work Orders
- Product → Finished Goods
- Product → Stock Out
- Material → ProductMaterials
- Material → Work Order Materials
- Material → Inventory
- Material → Stock In
- Quotation → Work Orders
- Work Order → Work Order Materials
- Work Order → Purchase Orders
- Work Order → Production Logs
- Work Order → QC Reports
- Work Order → Finished Goods
- Work Order → Stock Out
- Purchase Order → Stock In
- User → Quotations Created
- User → Work Orders Created
- User → Purchase Orders Created
- User → Purchase Orders Approved
- User → Production Logs Created
- User → QC Reports Created

### Many-to-Many Relationships:
- Products ↔ Materials (through ProductMaterial)

---

## Key Features

1. **Bill of Materials (BOM):** ProductMaterial model defines what materials and quantities are needed for each product.

2. **Cost Tracking:** Work orders automatically calculate total cost and per-piece cost based on component costs.

3. **Role-Based Access:** Custom User model with different roles for access control.

4. **Inventory Management:** Tracks both materials and products with reorder levels.

5. **Production Workflow:** Tracks from quotation → work order → production → QC → finished goods.

6. **Purchase Management:** Manages vendor quotations and purchase orders with status tracking.

7. **Stock Management:** Tracks incoming (stock_in) and outgoing (stock_out) inventory.

---

## API Endpoints (via Django Views)

```
GET    /                              # Dashboard
GET    /products/                     # Product list
GET    /products/<id>/                # Product detail
GET    /materials/                    # Material list
GET    /materials/<id>/               # Material detail
GET    /quotations/                   # Quotation list
GET    /quotations/<id>/              # Quotation detail
GET    /work-orders/                  # Work order list
GET    /work-orders/<id>/             # Work order detail
GET    /purchase-orders/              # Purchase order list
GET    /purchase-orders/<id>/         # Purchase order detail
GET    /inventory/                    # Inventory list
GET    /production-logs/              # Production log list
GET    /qc-reports/                   # QC report list
GET    /qc-reports/<id>/              # QC report detail
```

---

## Notes

- All timestamps are automatically managed (auto_now_add, auto_now)
- Foreign keys use CASCADE delete by default (some use SET_NULL for audit trails)
- Unique constraints prevent duplicate entries where appropriate
- Models include string representations (__str__) for easy identification
- Admin interface is fully configured with list displays and search capabilities
