# System Requirements Specification: LogicPOS Pricing Engine

## 1. Overview
The LogicPOS Pricing Engine calculates transaction details for a customer's shopping cart.

## 2. Data Entities
* **Product:** Defined by ID, Name, Price, and Category.
* **Category:**
    * `FOOD`
    * `ELECTRONICS`
    * `LUXURY` (High-value items like watches, jewelry)
* **User Role:**
    * `STANDARD`
    * `VETERAN`
    * `EMPLOYEE`

## 3. Business Rules

### 3.1. Taxation Logic
* **FOOD:** Tax-exempt (0%).
* **ELECTRONICS:** 15% sales tax.
* **LUXURY:** 20% sales tax.
* *Tax is calculated on the base price before discounts.*

### 3.2. Discount Logic
* **Veteran Discount:** 10% off the **entire order**.
* **Employee Discount:** 20% off the **entire order**.
* **Volume Discount:** 5% off the **entire order** if the cart contains strictly more than 5 items (>5).
* **Standard:** No base discount.

### 3.3. Discount Stacking Rules
* **Veteran:** STACKS with Volume Discount (Additive).
    * *Example:* 10% + 5% = 15%.
* **Employee:** DOES NOT STACK.
    * *Rule:* The system applies the **better** of the two discounts (Max of Employee vs. Volume).
    * *Example:* Employee (20%) vs Volume (5%) -> Final Discount is 20%.

## 4. Output
Receipt must include: Subtotal, Tax Amount, Discount Amount, Grand Total.
