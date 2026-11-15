# Precifica Fácil — MVP 001

Status: PROPOSED
Product slug: precifica-facil
Product format: XLSX

## Objective

Help small merchants estimate selling prices
based on product costs, operating expenses,
transaction fees and desired margins.

## Target Audience

- MEIs
- Small merchants
- Independent sellers

## Deliverable

An editable XLSX workbook.

### Worksheets

1. Instruções
2. Precificador
3. Simulador de Descontos
4. Exemplos

## Required Inputs

- Product name
- Purchase or production cost
- Additional variable cost per unit
- Allocated fixed cost per unit
- Percentage taxes, entered by user
- Percentage transaction fees
- Fixed transaction fee per sale
- Desired profit margin
- Optional discount

## Core Calculation

cost_base =
    product_cost
    + additional_variable_cost
    + allocated_fixed_cost
    + fixed_transaction_fee

rate_sum =
    tax_rate
    + transaction_fee_rate
    + desired_margin

suggested_price = cost_base / (1 - rate_sum)

All percentages use decimal representations.

If rate_sum >= 1, the price is not calculable
under these assumptions.

The calculated margin is an estimate based
only on costs and rates entered by the user.

## Outputs

- Suggested selling price
- Estimated revenue per unit
- Estimated costs and fees
- Estimated profit per unit
- Effective estimated margin
- Discount simulation
- Warnings for invalid inputs

## Acceptance Criteria

- Excel opens without errors
- Inputs are clearly distinguished from formulas
- Formulas are protected against accidental edits
- Invalid combinations display warnings
- Monetary results use BRL formatting
- No macros or external connections required
- Sample scenarios have verified calculations
- Instructions explain limitations

## Out of Scope

- Automatic tax determination
- Inventory management
- ERP integration
- Payment processing
- Guaranteed profitability
- AI features in the first version

## Commercial Readiness

The product must be built, tested and reviewed
before any sales landing page is published.

Marketing claims must reflect actual features.
