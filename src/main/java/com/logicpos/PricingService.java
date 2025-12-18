package com.logicpos;

import java.util.List;

public class PricingService {

    public Receipt calculate(List<Product> cart, UserRole role) {
        double subtotal = 0.0;
        double taxAmount = 0.0;
        double nonLuxurySubtotal = 0.0; // Subtotal for non-luxury items, specifically used for Employee volume discount

        // 1. Calculate Subtotal and Tax
        for (Product p : cart) {
            subtotal += p.getBasePrice();

            // Corrected Tax Rules based on system requirements and test expectations
            double taxRate = 0.0;
            switch (p.getCategory()) {
                case FOOD:
                    taxRate = 0.0; // 0% tax for Food
                    break;
                case ELECTRONICS:
                    taxRate = 0.10; // Corrected: 10% tax for Electronics (was 15%)
                    break;
                case LUXURY:
                    taxRate = 0.15; // Corrected: 15% tax for Luxury (was 20%)
                    break;
            }
            taxAmount += p.getBasePrice() * taxRate;

            if (p.getCategory() != ProductCategory.LUXURY) {
                nonLuxurySubtotal += p.getBasePrice();
            }
        }

        // 2. Volume Discount Percentage (based on total item count)
        // Rule: Luxury items COUNT for the threshold.
        int itemCount = cart.size();
        double volumeDiscountPercent = 0.0;
        if (itemCount > 10) {
            volumeDiscountPercent = 0.10; // 10% for > 10 items
        } else if (itemCount > 5) {
            volumeDiscountPercent = 0.05; // 5% for > 5 items
        }

        // 3. Role Discount Percentage (base discount rate for roles)
        double roleDiscountPercent = 0.0;
        if (role == UserRole.VETERAN) {
            roleDiscountPercent = 0.10; // 10% for Veteran
        } else if (role == UserRole.EMPLOYEE) {
            roleDiscountPercent = 0.20; // 20% for Employee
        }

        // 4. Final Discount Aggregation (Revised based on specific scenario requirements)
        double finalDiscountAmount = 0.0;

        if (role == UserRole.STANDARD) {
            // STANDARD: Only volume discount applies.
            // Based on tests, volume discount applies to the ENTIRE subtotal for STANDARD users.
            if (volumeDiscountPercent > 0) { // Check if volume threshold is met
                finalDiscountAmount = subtotal * volumeDiscountPercent;
            }
            // If no volume discount, finalDiscountAmount remains 0.0
        } else if (role == UserRole.VETERAN) {
            // VETERAN: Role discount is 10%. Stacks with volume, but has a total cap.
            // Interpretation from scenarios:
            // - If volume discount criteria is met (> 5 items), the TOTAL discount is 15% of the subtotal.
            // - If volume discount criteria is NOT met (<= 5 items), only the 10% role discount applies to subtotal.
            if (itemCount > 5) { // Check if volume threshold is met
                finalDiscountAmount = subtotal * 0.15; // Total discount for veteran with volume is 15% of subtotal
            } else {
                finalDiscountAmount = subtotal * roleDiscountPercent; // Only 10% role discount
            }
        } else if (role == UserRole.EMPLOYEE) {
            // EMPLOYEE: Role discount is 20%. Does NOT stack. Takes the larger of role or volume discount.
            // The "MAX 20 Percent" in scenario names implies the role discount itself is this maximum,
            // or the final discount does not exceed 20% of subtotal.
            // Volume discount for EMPLOYEE is applied to nonLuxurySubtotal, as per rule.
            double calculatedVolumeDiscountAmount = nonLuxurySubtotal * volumeDiscountPercent;
            double calculatedRoleDiscountAmount = subtotal * roleDiscountPercent;
            
            // Take the larger of the two calculated discounts
            finalDiscountAmount = Math.max(calculatedVolumeDiscountAmount, calculatedRoleDiscountAmount);
        }

        // 5. Grand Total
        double grandTotal = subtotal + taxAmount - finalDiscountAmount;

        return new Receipt(subtotal, taxAmount, finalDiscountAmount, grandTotal);
    }
}