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
        // Arrange
        Product product1 = new Product("1", "Bread", ProductCategory.FOOD, 2.0);
        Product product2 = new Product("2", "Milk", ProductCategory.FOOD, 3.0);
        List<Product> cart = new ArrayList<>();
        cart.add(product1);
        cart.add(product2);

        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        // Assert
        double expectedSubtotal = 5.0;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = 0.5; // 10% of 5.0
        double expectedGrandTotal = 4.5;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        // Arrange
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Item " + i, ProductCategory.FOOD, 10.0));
        }

        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Assert
        double expectedSubtotal = 60.0;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = 3.0; // 5% of 60.0
        double expectedGrandTotal = 57.0;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testTaxCalculation() {
        // Arrange
        Product food = new Product("1", "Bread", ProductCategory.FOOD, 2.0);
        Product electronics = new Product("2", "Laptop", ProductCategory.ELECTRONICS, 1000.0);
        Product luxury = new Product("3", "Watch", ProductCategory.LUXURY, 500.0);
        List<Product> cart = new ArrayList<>();
        cart.add(food);
        cart.add(electronics);
        cart.add(luxury);

        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Assert
        double expectedSubtotal = 1502.0;
        double expectedTaxAmount = (1000.0 * 0.15) + (500.0 * 0.20) ; // 150 + 100 = 250
        double expectedDiscountAmount = 0.0;
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testLargeVolumeDiscountLuxuryIncluded() {
         // Arrange
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Item " + i, ProductCategory.FOOD, 10.0));
        }
        cart.add(new Product("7", "LuxuryItem", ProductCategory.LUXURY, 100.0));

        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Assert
        double expectedSubtotal = 160.0;
        double expectedTaxAmount = 20.0;
        double expectedDiscountAmount = 3.0; //5% of 60
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);

    }

    @Test
    void testEmployeeDiscountNoStackingVolumeSmaller() {
        // Arrange
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Item " + i, ProductCategory.FOOD, 10.0));
        }
        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        // Assert
        double expectedSubtotal = 30.0;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = 6.0; //20% of 30
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testEmployeeDiscountNoStackingVolumeLarger() {
        // Arrange
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Item " + i, ProductCategory.FOOD, 10.0));
        }
        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        // Assert
        double expectedSubtotal = 60.0;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = 12.0; //20% of 60
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranDiscountStackingVolume() {
        // Arrange
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Item " + i, ProductCategory.FOOD, 10.0));
        }
        // Act
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        // Assert
        double expectedSubtotal = 60.0;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = 6.0; //5% + 10% = 15% of 40
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

}