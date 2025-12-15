package com.logicpos;

import java.util.List;

public class PricingService {

    public Receipt calculate(List<Product> cart, UserRole role) {
        double subtotal = 0.0;
        double taxAmount = 0.0;
        double nonLuxurySubtotal = 0.0;
        
        // 1. Calculate Subtotal and Tax
        for (Product p : cart) {
            subtotal += p.getBasePrice();
            
            // Tax Rules
            double taxRate = 0.0;
            switch (p.getCategory()) {
                case FOOD:
                    taxRate = 0.0;
                    break;
                case ELECTRONICS:
                    taxRate = 0.15;
                    break;
                case LUXURY:
                    taxRate = 0.20;
                    break;
            }
            taxAmount += p.getBasePrice() * taxRate;

            if (p.getCategory() != ProductCategory.LUXURY) {
                nonLuxurySubtotal += p.getBasePrice();
            }
        }

        // 2. Volume Discount Calculation
        // Rule: Luxury items COUNT for the threshold, but discount applies to non-Luxury subtotal
        int itemCount = cart.size();
        double volumeDiscountPercent = 0.0;
        if (itemCount > 10) {
            volumeDiscountPercent = 0.10;
        } else if (itemCount > 5) {
            volumeDiscountPercent = 0.05;
        }
        
        double volumeDiscountAmount = nonLuxurySubtotal * volumeDiscountPercent;

        // 3. Role Discount Calculation
        // Assumption: Role discount applies to the ENTIRE subtotal (unless otherwise constrained, but standard role discounts are usually global)
        // If the requirement meant Role Discount also excludes Luxury, it would likely be explicit. 
        // We will apply Role Discount to the Full Subtotal based on standard interpretation.
        
        double roleDiscountPercent = 0.0;
        if (role == UserRole.VETERAN) {
            roleDiscountPercent = 0.10;
        } else if (role == UserRole.EMPLOYEE) {
            roleDiscountPercent = 0.20;
        }
        
        double roleDiscountAmount = subtotal * roleDiscountPercent;

        // 4. Final Discount Aggregation
        double finalDiscountAmount = 0.0;

        if (role == UserRole.VETERAN) {
            // VETERAN: Stacks with Volume
            finalDiscountAmount = volumeDiscountAmount + roleDiscountAmount;
        } else if (role == UserRole.EMPLOYEE) {
            // EMPLOYEE: Does NOT stack. Take larger.
            finalDiscountAmount = Math.max(volumeDiscountAmount, roleDiscountAmount);
        } else {
            // STANDARD: Just Volume
            finalDiscountAmount = volumeDiscountAmount;
        }

        // 5. Grand Total
        double grandTotal = subtotal + taxAmount - finalDiscountAmount;

        return new Receipt(subtotal, taxAmount, finalDiscountAmount, grandTotal);
    }
}
