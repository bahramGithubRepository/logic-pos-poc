package com.logicpos;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.ArrayList;
import java.util.List;

public class PricingServiceGeneratedTest {

    private final double DELTA = 0.01; // Tolerance for double comparisons

    // Helper method to create a Product
    private Product createProduct(String category, double price, int index) {
        ProductCategory productCategory = ProductCategory.valueOf(category.toUpperCase());
        // Using index for unique IDs and names, though not strictly used in calculations
        return new Product(category + index, category + "Item" + index, productCategory, price);
    }

    @Test
    void testStandardNoVolumeMixed() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Electronics", 20.00, 2));
        cart.add(createProduct("Luxury", 30.00, 3));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(60.00, receipt.getSubtotal(), DELTA);
        assertEquals(6.50, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(66.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testStandardVolumeMixed5Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Electronics", 20.00, 2));
        cart.add(createProduct("Luxury", 30.00, 3));
        cart.add(createProduct("Food", 5.00, 4));
        cart.add(createProduct("Electronics", 15.00, 5));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(80.00, receipt.getSubtotal(), DELTA);
        assertEquals(7.60, receipt.getTaxAmount(), DELTA);
        assertEquals(4.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(83.60, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testVeteranNoVolumePureFood() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Food", 15.00, 2));
        cart.add(createProduct("Food", 20.00, 3));

        UserRole userRole = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(45.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(6.75, receipt.getDiscountAmount(), DELTA);
        assertEquals(38.25, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testVeteranVolumeMixed6Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Electronics", 20.00, 2));
        cart.add(createProduct("Luxury", 30.00, 3));
        cart.add(createProduct("Food", 5.00, 4));
        cart.add(createProduct("Electronics", 15.00, 5));
        cart.add(createProduct("Luxury", 25.00, 6));

        UserRole userRole = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(105.00, receipt.getSubtotal(), DELTA);
        assertEquals(9.40, receipt.getTaxAmount(), DELTA);
        assertEquals(21.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(93.40, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testEmployeeNoVolumePureElectronics() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Electronics", 25.00, 1));
        cart.add(createProduct("Electronics", 35.00, 2));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(60.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.80, receipt.getTaxAmount(), DELTA);
        assertEquals(12.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(52.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testEmployeeVolumePureLuxury5Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Luxury", 50.00, 1));
        cart.add(createProduct("Luxury", 60.00, 2));
        cart.add(createProduct("Luxury", 70.00, 3));
        cart.add(createProduct("Luxury", 80.00, 4));
        cart.add(createProduct("Luxury", 90.00, 5));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(350.00, receipt.getSubtotal(), DELTA);
        assertEquals(42.00, receipt.getTaxAmount(), DELTA);
        assertEquals(70.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(322.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testStandardNoDiscountBoundary4Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Electronics", 20.00, 2));
        cart.add(createProduct("Luxury", 30.00, 3));
        cart.add(createProduct("Food", 5.00, 4));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(65.00, receipt.getSubtotal(), DELTA);
        assertEquals(6.50, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(71.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testStandardVolumePureFood6Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 1.00, 1));
        cart.add(createProduct("Food", 2.00, 2));
        cart.add(createProduct("Food", 3.00, 3));
        cart.add(createProduct("Food", 4.00, 4));
        cart.add(createProduct("Food", 5.00, 5));
        cart.add(createProduct("Food", 6.00, 6));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(21.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(1.05, receipt.getDiscountAmount(), DELTA);
        assertEquals(19.95, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testStandardSingleElectronics() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Electronics", 100.00, 1));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(100.00, receipt.getSubtotal(), DELTA);
        assertEquals(10.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(110.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testVeteranSingleLuxuryHighPrice() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Luxury", 500.00, 1));

        UserRole userRole = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(500.00, receipt.getSubtotal(), DELTA);
        assertEquals(63.75, receipt.getTaxAmount(), DELTA);
        assertEquals(75.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(488.75, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testEmployeeMixedVolumeVerifyMax5Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Electronics", 20.00, 1));
        cart.add(createProduct("Luxury", 30.00, 2));
        cart.add(createProduct("Food", 10.00, 3));
        cart.add(createProduct("Electronics", 25.00, 4));
        cart.add(createProduct("Luxury", 15.00, 5));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(100.00, receipt.getSubtotal(), DELTA);
        assertEquals(9.00, receipt.getTaxAmount(), DELTA);
        assertEquals(20.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(89.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testEmptyCart() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(0.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(0.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    void testStandardVolumeComprehensiveMixed6Items() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(createProduct("Food", 10.00, 1));
        cart.add(createProduct("Electronics", 20.00, 2));
        cart.add(createProduct("Luxury", 30.00, 3));
        cart.add(createProduct("Food", 5.00, 4));
        cart.add(createProduct("Electronics", 15.00, 5));
        cart.add(createProduct("Luxury", 25.00, 6));

        UserRole userRole = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, userRole);

        assertEquals(105.00, receipt.getSubtotal(), DELTA);
        assertEquals(11.16, receipt.getTaxAmount(), DELTA);
        assertEquals(5.25, receipt.getDiscountAmount(), DELTA);
        assertEquals(110.91, receipt.getGrandTotal(), DELTA);
    }
}