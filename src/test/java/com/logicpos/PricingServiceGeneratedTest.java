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
    void testStandardCustomerSingleFoodItem() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerSingleElectronicsItem() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(25.00, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(28.75, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerSingleElectronicsItem() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(25.00, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(2.50, receipt.getDiscountAmount(), 0.001);
        assertEquals(26.25, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerExactlyFiveMixedItems() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));


        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(51.50, receipt.getSubtotal(), 0.001);
        assertEquals(7.50, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(59.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerExactlySixMixedItems() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(76.50, receipt.getSubtotal(), 0.001);
        assertEquals(11.25, receipt.getTaxAmount(), 0.001);
        assertEquals(3.825, receipt.getDiscountAmount(), 0.001);
        assertEquals(83.925, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerSixMixedItemsStackingDiscounts() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double subtotal = 76.50;
        double taxAmount = 11.25;
        double expectedDiscount = subtotal * 0.15;
        double expectedGrandTotal = (subtotal + taxAmount) - expectedDiscount;

        assertEquals(76.50, receipt.getSubtotal(), 0.001);
        assertEquals(11.25, receipt.getTaxAmount(), 0.001);
        assertEquals(11.475, receipt.getDiscountAmount(), 0.001);
        assertEquals(76.275, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerExactlyFiveMixedItems() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(51.50, receipt.getSubtotal(), 0.001);
        assertEquals(7.50, receipt.getTaxAmount(), 0.001);
        assertEquals(5.15, receipt.getDiscountAmount(), 0.001);
        assertEquals(53.85, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerMixedCartTaxationOnly() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Mouse"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(26.00, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(29.75, receipt.getGrandTotal(), 0.001);
    }
}