# Lab 3 - Component Modelling & Architectural Pattern Selection

**Student:** M P Shashank (PES1UG24AM160)
**Scenario:** Self-Service Coffee Kiosk System
**Chosen architecture:** Layered (Presentation -> Business/Application -> Infrastructure)

## Deliverables
| File | Description |
|------|-------------|
| `Component_Diagram.png` / `Component_Diagram.pdf` | UML component diagram |
| `Lab3_Architecture_Justification.docx` / `.pdf` | One-page written justification |

## Components (9)
Kiosk Touch UI, Order Controller, Menu Catalog, Payment Processor, Receipt Generator, Menu Store (database), Order Log (database), Card Terminal (device), Thermal Printer (device)

## Interfaces (9)
| Interface | Provided by | Required by | Technology |
|-----------|-------------|-------------|------------|
| IKioskOrder | Order Controller | Kiosk Touch UI | method call |
| IMenuQuery | Menu Catalog | Kiosk Touch UI | method call |
| IPriceLookup | Menu Catalog | Order Controller | method call |
| IPaymentAuth | Payment Processor | Order Controller | method call |
| IReceiptPrint | Receipt Generator | Order Controller | method call |
| IMenuData | Menu Store | Menu Catalog | SQL / SQLite |
| IOrderLog | Order Log | Order Controller | SQL insert |
| ICardTerminal | Card Terminal | Payment Processor | USB / EMV SDK |
| IPrinterDriver | Thermal Printer | Receipt Generator | USB / ESC-POS |
