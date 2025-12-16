# System Requirements Specification: LogicPOS Pricing Engine

## 1. Overview
The LogicPOS Pricing Engine is responsible for calculating the final transaction details for a customer's shopping cart. It processes a list of products and the customer's profile to generate a detailed receipt.

## 2. Data Entities
* **Product:** Defined by a unique ID, Name, Price, and Category.
* **Category:** Items are classified into specific groups, currently including `FOOD` and `ELECTRONICS`.
* **User Role:** Customers are identified by roles, specifically `STANDARD` or `VETERAN`.

## 3. Business Rules

### 3.1. Taxation Logic
Tax calculation is based on the product category:
* **FOOD Category:** These items are tax-exempt (0% tax rate).
* **ELECTRONICS Category:** These items are subject to a **15% sales tax**.
* *Note: Tax is calculated on the item price before discounts are applied.*

### 3.2. Discount Logic
Discounts are applied to the transaction subtotal based on the following criteria:
* **Veteran Discount:** Customers with the `VETERAN` role receive a flat **10% discount** on the entire order.
* **Volume Discount:** Any transaction containing **strictly more than 5 items** (Quantity > 5) receives a **5% discount**.
* **Standard Customers:** Customers with the `STANDARD` role receive no role-based discount.

### 3.3. Discount Stacking Rule
* Discounts are **additive**.
* If a customer qualifies for multiple discounts (e.g., a Veteran buying 6 items), the percentages are added together.
* **Example:** 10% (Veteran) + 5% (Volume) = **15% Total Discount**.

## 4. Output Requirements
The system must generate a Receipt containing:
* **Subtotal:** Sum of all product prices.
* **Tax Amount:** Total calculated tax.
* **Discount Amount:** Total value deducted from the subtotal.
* **Grand Total:** Final amount to be paid (Subtotal + Tax - Discount).
