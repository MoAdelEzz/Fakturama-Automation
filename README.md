# Fakturama Automation

Automates [Fakturama](https://www.fakturama-project.org/) desktop invoicing on Windows. An order image is sent to an n8n webhook, parsed into structured data, and used to create master records, an order, and an invoice inside Fakturama.

## Prerequisites

- **Windows** (UI automation via `uiautomation` and `pywin32`)
- **Python 3.11+**
- **Fakturama** installed and running before you start the script
- **n8n webhook** configured to accept an order image and return JSON (see [n8n integration](#n8n-integration))

## Project structure

```
fakturama-automation/
├── requirements.txt          # Python dependencies
├── README.md
├── .env                      # Local config (not committed)
└── src/
    ├── main.py               # Entry point, orchestrates the full pipeline
    ├── env.py                # Loads .env variables
    │
    ├── models/               # Domain data, formatting, and JSON parsing
    │   ├── formatting.py     # Shared constants and data utils formatting
    │   ├── debtor.py         # Customer / billing address model
    │   ├── payment.py        # Payment method model and code mapping
    │   ├── vat.py            # VAT rate model and price calculations
    │   ├── product.py        # Product line item model
    │   └── order.py          # Order model and n8n parser
    │
    ├── vision/               # Image-based helpers
    │   ├── n8n_controller.py # N8N API handler
    │   └── image_processor.py# image processing helpers
    │
    ├── ui/                   # Low-level Fakturama window interaction
    │   ├── app.py            # Finds and connects to the Fakturama window
    │   ├── window.py         # Primitives: fields, buttons, tabs, save, etc.
    │   ├── dialogs/
    │   │   ├── common.py     # Shared dialog search/select helpers
    │   │   ├── address_picker.py  # "Select the address" dialog
    │   │   └── product_picker.py  # "Select a product" dialog + per product setups
    │   └── forms/
    │       ├── order_form.py    # New Order tab manager
    │       └── invoice_form.py  # New Invoice manager
    │
    ├── entities/             # Master-data CRUD in Fakturama sidebars
    │   ├── base.py           # Search, screenshot table, create-if-missing
    │   ├── debtors.py        # DebtorUI
    │   ├── products.py       # ProductsUI
    │   ├── VATs.py           # VATsUI
    │   └── payment_methods.py# PaymentMethodUI
    │
    └── workflows/            # Multi-step business processes
        ├── entity.py         # Ensure a master record exists (search → create)
        ├── order_creation.py # Create and fill a new order
        └── invoice_creation.py # Create invoice from open order
```

## What each layer does

| Layer | Role |
|-------|------|
| **models/** | Pure data no UI imports. Holds field mappings (`resolve_fields`), search strings resolution, and  formatting. |
| **vision/** | Image Processing & I/O, n8n webhook client and OpenCV image processing utilities. |
| **ui/** | All direct contact with the Fakturama window. Workflows never touch raw UI controls. |
| **entities/** | One UI adapter per master-data type. Searches the sidebar table; creates the record if none is found. |
| **workflows/** | calls models + ui + entities in sequence. |
| **main.py** | wires everything together from a single order image path. |

## High-level workflow

```mermaid
flowchart TD
    A[Order image] --> B[N8NClient.parse_order_image]
    B --> C[n8n webhook]
    C --> D[JSON response]
    D --> E[Order.from_json]

    E --> F[FakturamaApp.connect]
    F --> G[EntityWorkflow x N]

    G --> G1[Payment method]
    G --> G2[VAT rates]
    G --> G3[Debtor]
    G --> G4[Products]

    G1 & G2 & G3 & G4 --> H{Table has rows?}
    H -->|Yes| I[Skip — record exists]
    H -->|No| J[Create record in Fakturama]

    I & J --> K[OrderCreationWorkflow]
    K --> L[Fill order form, address, line items]
    L --> M[Save order]

    M --> N[InvoiceCreationWorkflow]
    N --> O[Open invoice from order tab]
    O --> P[Set payment info if paid]
    P --> Q[Save and close]
```

**Step by step:**

1. **Parse order** — `main.py` sends the image to n8n via `N8NClient`. The webhook returns JSON; `Order.from_json()` builds domain objects.
2. **Connect** — `FakturamaApp` attaches to the running Fakturama window.
3. **Ensure master data** — For each payment method, VAT, debtor, and product, `EntityWorkflow` searches the sidebar table (OpenCV row count). If rows exist, it skips; otherwise it opens the create form, fills fields from `resolve_fields()`, and saves.
4. **Create order** — `OrderCreationWorkflow` opens a new order, sets date/reference/discount, picks the debtor address, adds products with quantities, and saves.
5. **Create invoice** — `InvoiceCreationWorkflow` opens an invoice from the order tab, marks it paid if needed, saves, and closes the tab.

## n8n integration

The webhook receives a multipart POST with an `image` field and should respond with JSON like:

```json
{
  "success": true,
  "order": {
    "order_created_at": "2026-07-14",
    "order_external_refernece": "WEB-2026-0714-A17",
    "order_level_discount": 10,
    "debtor": { "...": "..." },
    "items": [ { "...": "..." } ],
    "payment": {
      "paymentMethod": "Bank Transfer",
      "isPaid": true,
      "paid_at": "2026-07-18"
    }
  }
}
```

On failure, return `"success": false` and an `"error"` object — `N8NClient` will raise a `RuntimeError`.

## Setup

### 1. Clone and create a virtual environment

```powershell
cd fakturama-automation
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure environment

Create a `.env` file in the project root:

```env
NN_INSTANCE_NAME=your-n8n-instance
```
| Contact me to get the instance name

### 3. Start Fakturama

Open Fakturama and leave it running. The script looks for a window matching `Fakturama*`.

## How to run

From the project root, with the virtual environment activated and Fakturama open:

```powershell
python -m src.main path\to\order-image.png
```

Supported image formats: `.png`, `.jpg`, `.jpeg`, `.webp`.

You can also test the n8n client alone:

```powershell
python -m src.vision.n8n_controller path\to\order-image.png
```

## Troubleshooting

| Issue | Likely cause |
|-------|----------------|
| `Fakturama.exe Is Not Running` | Start Fakturama before running the script |
| `Order image not found` | Check the image path passed on the command line |
| `SAVE_BUTTON_FAILED` | A form field was invalid or a dialog was left open |
| Entity always re-created | OpenCV row detection missed existing rows — check table visibility |
| n8n timeout | Increase the `timeout` in `n8n_controller.py` (default 120s) |

Debug screenshots can be saved from `entities/base.py` by uncommenting the `image.save(...)` line.
