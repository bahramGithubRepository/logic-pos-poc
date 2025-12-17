package com.logicpos;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    private PricingService pricingService;
    private InMemoryRepository repository;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
        repository = new InMemoryRepository();
        repository.seed();
    }

    @Test
    void testStandardCustomerSingleFoodItemTaxExemption() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerSingleElectronicsItemTaxApplication() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(1000.00, receipt.getSubtotal(), 0.001);
        assertEquals(150.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(1150.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerSingleFoodItemVeteranDiscountOnly() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.05, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.45, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerSingleElectronicsItemVeteranDiscountTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(1000.00, receipt.getSubtotal(), 0.001);
        assertEquals(150.00, receipt.getTaxAmount(), 0.001);
        assertEquals(100.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(1050.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerExactly5ItemsNoVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            cart.add(repository.getProduct("Laptop"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(5000.00, receipt.getSubtotal(), 0.001);
        assertEquals(750.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(5750.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerExactly6ItemsVolumeDiscountApplied() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(3.00, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.15, receipt.getDiscountAmount(), 0.001);
        assertEquals(2.85, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerExactly5ItemsVeteranDiscountOnlyNoVolume() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            cart.add(repository.getProduct("Laptop"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(5000.00, receipt.getSubtotal(), 0.001);
        assertEquals(750.00, receipt.getTaxAmount(), 0.001);
        assertEquals(500.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(5200.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testCriticalVeteranCustomer6MixedItemsStackedDiscountsVeteranVolume() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Laptop"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        double expectedGrandTotal = (30 + 300) * 0.85 + (300 * 0.15);

        assertEquals(330.00, receipt.getSubtotal(), 0.001);
        assertEquals(45.00, receipt.getTaxAmount(), 0.001);
        assertEquals(49.50, receipt.getDiscountAmount(), 0.001);
        assertEquals(325.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerMixedCategoriesNoDiscounts() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 2; i++) {
            cart.add(repository.getProduct("Laptop"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(2020.00, receipt.getSubtotal(), 0.001);
        assertEquals(300.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(2320.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerMixedCategoriesVeteranDiscountOnly() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 2; i++) {
            cart.add(repository.getProduct("Laptop"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(2020.00, receipt.getSubtotal(), 0.001);
        assertEquals(300.00, receipt.getTaxAmount(), 0.001);
        assertEquals(202.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(2118.00, receipt.getGrandTotal(), 0.001);
    }
}