package com.logicpos;

public class Receipt {
    private double subtotal;
    private double taxAmount;
    private double discountAmount;
    private double grandTotal;

    public Receipt(double subtotal, double taxAmount, double discountAmount, double grandTotal) {
        this.subtotal = subtotal;
        this.taxAmount = taxAmount;
        this.discountAmount = discountAmount;
        this.grandTotal = grandTotal;
    }

    public double getSubtotal() {
        return subtotal;
    }

    public double getTaxAmount() {
        return taxAmount;
    }

    public double getDiscountAmount() {
        return discountAmount;
    }

    public double getGrandTotal() {
        return grandTotal;
    }

    @Override
    public String toString() {
        return "Receipt:\n" +
               "  Subtotal:        " + String.format("%.2f", subtotal) + "\n" +
               "  Tax:             " + String.format("%.2f", taxAmount) + "\n" +
               "  Discounts:      -" + String.format("%.2f", discountAmount) + "\n" +
               "  ----------------------\n" +
               "  Grand Total:     " + String.format("%.2f", grandTotal);
    }
}
