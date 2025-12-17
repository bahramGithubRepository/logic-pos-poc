package com.logicpos;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    private InMemoryRepository repo;
    private PricingService service;

    @BeforeEach
    void setUp() {
        repo = new InMemoryRepository();
        repo.seed();
        service = new PricingService();
    }

    @Test
    void SCENARIO_1_Standard_User_Single_FOOD_Item_No_Tax_No_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_2_Standard_User_Single_ELECTRONICS_Item_15Pct_Tax_No_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(25.00, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(28.75, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_3_Standard_User_Mixed_Categories_Item_Specific_Tax_No_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(25.50, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(29.25, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_4_Veteran_User_Single_FOOD_Item_10Pct_Veteran_Discount_No_Tax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));

        Receipt receipt = service.calculate(cart, UserRole.VETERAN);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.05, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.45, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_5_Veteran_User_Single_ELECTRONICS_Item_10Pct_Veteran_Discount_15Pct_Tax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.VETERAN);

        assertEquals(25.00, receipt.getSubtotal(), 0.001);
        assertEquals(3.75, receipt.getTaxAmount(), 0.001);
        assertEquals(2.50, receipt.getDiscountAmount(), 0.001);
        assertEquals(26.25, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_6_Boundary_Standard_User_Exactly_5_Items_No_Volume_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(26.50, receipt.getSubtotal(), 0.001);
        assertEquals(7.50, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(34.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_7_Boundary_Standard_User_Exactly_6_Items_With_Volume_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(51.50, receipt.getSubtotal(), 0.001);
        assertEquals(11.25, receipt.getTaxAmount(), 0.001);
        assertEquals(1.25, receipt.getDiscountAmount(), 0.001);
        assertEquals(61.50, receipt.getGrandTotal(), 0.001); // Should be 61.50
    }

    @Test
    void SCENARIO_8_CRITICAL_Veteran_User_Boundary_6_Items_Additive_Stacked_Discounts() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.VETERAN);

        assertEquals(51.50, receipt.getSubtotal(), 0.001);
        assertEquals(11.25, receipt.getTaxAmount(), 0.001);
        assertEquals(7.725, receipt.getDiscountAmount(), 0.001);
        assertEquals(55.025, receipt.getGrandTotal(), 0.001);

        // Explicit stacking assertion
        double expectedGrandTotal = (51.50 * 0.85) + 11.25;
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
        assertEquals(51.50 * 0.15, receipt.getDiscountAmount(), 0.001); // Verifies 15% combined discount.
    }

    @Test
    void SCENARIO_9_Veteran_User_Boundary_5_Items_Only_Veteran_Discount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Mouse"));
        cart.add(repo.getProduct("Mouse"));

        Receipt receipt = service.calculate(cart, UserRole.VETERAN);

        assertEquals(26.50, receipt.getSubtotal(), 0.001);
        assertEquals(7.50, receipt.getTaxAmount(), 0.001);
        assertEquals(2.65, receipt.getDiscountAmount(), 0.001);
        assertEquals(31.35, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void SCENARIO_10_Standard_User_Many_FOOD_Items_With_Volume_Discount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            cart.add(repo.getProduct("Apple"));
        }

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(5.00, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(5.00, receipt.getGrandTotal(), 0.001);

        cart.add(repo.getProduct("Apple"));

        receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(5.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.275, receipt.getDiscountAmount(), 0.001);
        assertEquals(5.225, receipt.getGrandTotal(), 0.001);

    }

    @Test
    void SCENARIO_11_Standard_User_Many_ELECTRONICS_Items_With_Volume_Discount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            cart.add(repo.getProduct("Mouse"));
        }

        Receipt receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(250.00, receipt.getSubtotal(), 0.001);
        assertEquals(37.50, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(287.50, receipt.getGrandTotal(), 0.001);

        cart.add(repo.getProduct("Mouse"));
        receipt = service.calculate(cart, UserRole.STANDARD);

        assertEquals(275.00, receipt.getSubtotal(), 0.001);
        assertEquals(41.25, receipt.getTaxAmount(), 0.001);
        assertEquals(13.75, receipt.getDiscountAmount(), 0.001);
        assertEquals(302.50+41.25-13.75, receipt.getGrandTotal(), 0.001);
    }
}