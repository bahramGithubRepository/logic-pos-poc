package com.logicpos;

import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    @Test
    void testStandard_Customer_No_Discount_Below_Threshold_Mixed() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 50.00));
        cart.add(new Product("2", "ElectronicsItem1", ProductCategory.ELECTRONICS, 50.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(100.00, receipt.getSubtotal(), 0.005);
        assertEquals(8.00, receipt.getTaxAmount(), 0.005);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(108.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testStandard_Customer_Volume_Discount_Exact_Threshold_Luxury() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "LuxuryItem1", ProductCategory.LUXURY, 1000.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(1000.00, receipt.getSubtotal(), 0.005);
        assertEquals(190.00, receipt.getTaxAmount(), 0.005);
        assertEquals(50.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1140.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testStandard_Customer_Volume_Discount_Above_Threshold_Mixed() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 100.00));
        cart.add(new Product("2", "ElectronicsItem1", ProductCategory.ELECTRONICS, 500.00));
        cart.add(new Product("3", "LuxuryItem1", ProductCategory.LUXURY, 500.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(1100.00, receipt.getSubtotal(), 0.005);
        assertEquals(167.20, receipt.getTaxAmount(), 0.005);
        assertEquals(55.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1212.20, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testVeteran_Customer_Base_Discount_Below_Threshold_Electronics() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "ElectronicsItem1", ProductCategory.ELECTRONICS, 500.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(500.00, receipt.getSubtotal(), 0.005);
        assertEquals(67.50, receipt.getTaxAmount(), 0.005);
        assertEquals(50.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(517.50, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testVeteran_Customer_Stacking_Discount_Exact_Threshold_Luxury() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "LuxuryItem1", ProductCategory.LUXURY, 1000.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(1000.00, receipt.getSubtotal(), 0.005);
        assertEquals(170.00, receipt.getTaxAmount(), 0.005);
        assertEquals(150.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1020.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testVeteran_Customer_Stacking_Discount_Above_Threshold_Mixed() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 100.00));
        cart.add(new Product("2", "ElectronicsItem1", ProductCategory.ELECTRONICS, 500.00));
        cart.add(new Product("3", "LuxuryItem1", ProductCategory.LUXURY, 500.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(1100.00, receipt.getSubtotal(), 0.005);
        assertEquals(149.60, receipt.getTaxAmount(), 0.005);
        assertEquals(165.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1084.60, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testEmployee_Customer_Base_Discount_Below_Threshold_Food() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 200.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        assertEquals(200.00, receipt.getSubtotal(), 0.005);
        assertEquals(1.60, receipt.getTaxAmount(), 0.005);
        assertEquals(40.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(161.60, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testEmployee_Customer_Volume_Logic_Exact_Threshold_Electronics() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "ElectronicsItem1", ProductCategory.ELECTRONICS, 1000.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        assertEquals(1000.00, receipt.getSubtotal(), 0.005);
        assertEquals(120.00, receipt.getTaxAmount(), 0.005);
        assertEquals(200.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(920.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testEmployee_Customer_Volume_Logic_Above_Threshold_Mixed() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 100.00));
        cart.add(new Product("2", "ElectronicsItem1", ProductCategory.ELECTRONICS, 500.00));
        cart.add(new Product("3", "LuxuryItem1", ProductCategory.LUXURY, 500.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        assertEquals(1100.00, receipt.getSubtotal(), 0.005);
        assertEquals(140.80, receipt.getTaxAmount(), 0.005);
        assertEquals(220.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1020.80, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testStandard_Customer_Just_Below_Volume_Threshold_Luxury() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "LuxuryItem1", ProductCategory.LUXURY, 999.99));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(999.99, receipt.getSubtotal(), 0.005);
        assertEquals(200.00, receipt.getTaxAmount(), 0.005);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1199.99, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testStandard_Customer_Just_Above_Volume_Threshold_Luxury() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "LuxuryItem1", ProductCategory.LUXURY, 1000.01));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(1000.01, receipt.getSubtotal(), 0.005);
        assertEquals(190.00, receipt.getTaxAmount(), 0.005);
        assertEquals(50.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1140.01, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testPure_Food_Cart_Standard_Below_Threshold() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 100.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(100.00, receipt.getSubtotal(), 0.005);
        assertEquals(1.00, receipt.getTaxAmount(), 0.005);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(101.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testPure_Electronics_Cart_Veteran_Stacking_Discount() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "ElectronicsItem1", ProductCategory.ELECTRONICS, 600.00));
        cart.add(new Product("2", "ElectronicsItem2", ProductCategory.ELECTRONICS, 600.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(1200.00, receipt.getSubtotal(), 0.005);
        assertEquals(153.00, receipt.getTaxAmount(), 0.005);
        assertEquals(180.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1173.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testPure_Luxury_Cart_Employee_Volume_Confirm_20_Percent() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "LuxuryItem1", ProductCategory.LUXURY, 1500.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        assertEquals(1500.00, receipt.getSubtotal(), 0.005);
        assertEquals(240.00, receipt.getTaxAmount(), 0.005);
        assertEquals(300.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(1440.00, receipt.getGrandTotal(), 0.005);
    }

    @Test
    void testMixed_Cart_No_Discount_Low_Value() {
        PricingService pricingService = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("1", "FoodItem1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("2", "ElectronicsItem1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("3", "LuxuryItem1", ProductCategory.LUXURY, 30.00));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(60.00, receipt.getSubtotal(), 0.005);
        assertEquals(9.10, receipt.getTaxAmount(), 0.005);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.005);
        assertEquals(69.10, receipt.getGrandTotal(), 0.005);
    }
}