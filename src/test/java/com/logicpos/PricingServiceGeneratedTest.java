package com.logicpos;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

import java.util.ArrayList;
import java.util.List;

public class PricingServiceGeneratedTest {

    private PricingService pricingService;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    @Test
    void testVeteranDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "Bread", ProductCategory.FOOD, 2.0));
        cart.add(new Product("2", "Milk", ProductCategory.FOOD, 3.0));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 5.0;
        double expectedTax = 0.0;
        double expectedDiscount = expectedSubtotal * 0.10;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "Bread", ProductCategory.FOOD, 2.0));
        cart.add(new Product("2", "Milk", ProductCategory.FOOD, 3.0));
        cart.add(new Product("3", "Eggs", ProductCategory.FOOD, 4.0));
        cart.add(new Product("4", "Butter", ProductCategory.FOOD, 5.0));
        cart.add(new Product("5", "Cheese", ProductCategory.FOOD, 6.0));
        cart.add(new Product("6", "Apples", ProductCategory.FOOD, 7.0)); // 6 items

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 27.0;
        double expectedTax = 0.0;
        double expectedDiscount = expectedSubtotal * 0.05;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testElectronicsTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "Laptop", ProductCategory.ELECTRONICS, 1000.0));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 1000.0;
        double expectedTax = 1000.0 * 0.15;
        double expectedDiscount = 0.0;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

   @Test
    void testFoodTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "Bread", ProductCategory.FOOD, 2.0));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 2.0;
        double expectedTax = 0.0;
        double expectedDiscount = 0.0;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranAndVolumeDiscountStacking() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "Bread", ProductCategory.FOOD, 2.0));
        cart.add(new Product("2", "Milk", ProductCategory.FOOD, 3.0));
        cart.add(new Product("3", "Eggs", ProductCategory.FOOD, 4.0));
        cart.add(new Product("4", "Butter", ProductCategory.FOOD, 5.0));
        cart.add(new Product("5", "Cheese", ProductCategory.FOOD, 6.0));
        cart.add(new Product("6", "Apples", ProductCategory.FOOD, 7.0));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 27.0;
        double expectedTax = 0.0;
        double volumeDiscount = expectedSubtotal * 0.05;
        double veteranDiscount = expectedSubtotal * 0.10;
        double expectedDiscount = volumeDiscount + veteranDiscount;
        double expectedGrandTotal = expectedSubtotal + expectedTax - expectedDiscount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscount, receipt.getFinalDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }
}