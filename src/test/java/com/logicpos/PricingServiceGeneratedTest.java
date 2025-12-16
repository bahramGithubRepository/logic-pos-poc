package com.logicpos;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;

class PricingServiceGeneratedTest {

    private PricingService pricingService;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    @Test
    void testVeteranDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Bread", 2.50, ProductCategory.FOOD));
        cart.add(new Product("Laptop", 1200.00, ProductCategory.ELECTRONICS));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 1202.50;
        double expectedTax = 1200.00 * 0.15;
        double expectedRoleDiscount = expectedSubtotal * 0.10;
        double expectedFinalDiscount = expectedRoleDiscount; // No volume discount
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedFinalDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedFinalDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product("Candy", 1.00, ProductCategory.FOOD));
        }
        cart.add(new Product("Luxury Watch", 500.00, ProductCategory.LUXURY));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 506.00;
        double expectedTax = 500.00 * 0.20;
        double expectedVolumeDiscount = 6.0 * 0.05;
        double expectedFinalDiscount = expectedVolumeDiscount;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedFinalDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedFinalDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testTaxCalculation() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Bread", 2.00, ProductCategory.FOOD));
        cart.add(new Product("Laptop", 1000.00, ProductCategory.ELECTRONICS));
        cart.add(new Product("Luxury Bag", 500.00, ProductCategory.LUXURY));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 1502.00;
        double expectedFoodTax = 0.0;
        double expectedElectronicsTax = 1000.00 * 0.15;
        double expectedLuxuryTax = 500.00 * 0.20;
        double expectedTax = expectedFoodTax + expectedElectronicsTax + expectedLuxuryTax;
        double expectedGrandTotal = expectedSubtotal + expectedTax; //no discounts applied

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }
}