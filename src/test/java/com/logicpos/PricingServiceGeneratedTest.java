package com.logicpos;

import org.junit.jupiter.api.*;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PricingServiceGeneratedTest {

    private PricingService pricingService;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    @Test
    void testVeteranDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Item1", 100.0, ProductCategory.FOOD));
        cart.add(new Product("Item2", 200.0, ProductCategory.ELECTRONICS));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        // Expected discount: (100 + 200) * 0.10 = 30
        assertEquals(30.0, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Item1", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Item2", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Item3", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Item4", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Item5", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Item6", 10.0, ProductCategory.FOOD));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Expected discount: 60 * 0.05 = 3
        assertEquals(3.0, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testElectronicsTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Electronics", 100.0, ProductCategory.ELECTRONICS));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Expected tax: 100 * 0.15 = 15
        assertEquals(15.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testFoodTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Food", 100.0, ProductCategory.FOOD));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        // Expected tax: 100 * 0.0 = 0
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testVolumeAndVeteranDiscountStacking() {
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("Food1", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Food2", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Food3", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Food4", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Food5", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Food6", 10.0, ProductCategory.FOOD));
        cart.add(new Product("Electronic1", 10.0, ProductCategory.ELECTRONICS));
        cart.add(new Product("Electronic2", 10.0, ProductCategory.ELECTRONICS));
        cart.add(new Product("Electronic3", 10.0, ProductCategory.ELECTRONICS));
        cart.add(new Product("Electronic4", 10.0, ProductCategory.ELECTRONICS));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        // Subtotal = 100
        // Tax = 40 * 0.15 = 6
        // Volume Discount = 100 * 0.0 = 0.0 (since nonLuxurySubtotal is 60)
        // Veteran Discount = 100 * 0.10 = 10
        // Total Discount = 10

        List<Product> cart2 = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
             cart2.add(new Product("Food" + i, 10.0, ProductCategory.FOOD));
        }
         for (int i = 0; i < 4; i++) {
             cart2.add(new Product("Electronic" + i, 10.0, ProductCategory.ELECTRONICS));
        }

        Receipt receipt2 = pricingService.calculate(cart2, UserRole.VETERAN);

        double expectedDiscount = (60*.05) + (100*.10);
        assertEquals(expectedDiscount, receipt2.getDiscountAmount(), 0.001);
    }
}