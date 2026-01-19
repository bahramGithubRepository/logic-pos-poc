package com.logicpos;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.util.ArrayList;
import java.util.List;

public class PricingServiceGeneratedTest {

    private static final double DELTA = 0.001; // Tolerance for double comparisons

    // Scenario: Standard_Mixed_Boundary_5_Items_No_Discount
    @Test
    void testStandard_Mixed_Boundary_5_Items_No_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.STANDARD;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(90.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Standard_Mixed_Boundary_5_Items_No_Discount");
        Assertions.assertEquals(9.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Standard_Mixed_Boundary_5_Items_No_Discount");
        Assertions.assertEquals(0.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Standard_Mixed_Boundary_5_Items_No_Discount");
        Assertions.assertEquals(99.50, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Standard_Mixed_Boundary_5_Items_No_Discount");
    }

    // Scenario: Standard_Mixed_Boundary_6_Items_10_Percent_Discount
    @Test
    void testStandard_Mixed_Boundary_6_Items_10_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));
        cart.add(new Product("L2", "Luxury Item 2", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.STANDARD;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(120.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Standard_Mixed_Boundary_6_Items_10_Percent_Discount");
        Assertions.assertEquals(14.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Standard_Mixed_Boundary_6_Items_10_Percent_Discount");
        Assertions.assertEquals(12.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Standard_Mixed_Boundary_6_Items_10_Percent_Discount");
        Assertions.assertEquals(122.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Standard_Mixed_Boundary_6_Items_10_Percent_Discount");
    }

    // Scenario: Veteran_Mixed_Boundary_5_Items_10_Percent_Discount
    @Test
    void testVeteran_Mixed_Boundary_5_Items_10_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.VETERAN;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(90.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Veteran_Mixed_Boundary_5_Items_10_Percent_Discount");
        Assertions.assertEquals(9.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Veteran_Mixed_Boundary_5_Items_10_Percent_Discount");
        Assertions.assertEquals(9.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Veteran_Mixed_Boundary_5_Items_10_Percent_Discount");
        Assertions.assertEquals(90.50, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Veteran_Mixed_Boundary_5_Items_10_Percent_Discount");
    }

    // Scenario: Veteran_Mixed_Boundary_6_Items_15_Percent_Discount
    @Test
    void testVeteran_Mixed_Boundary_6_Items_15_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));
        cart.add(new Product("L2", "Luxury Item 2", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.VETERAN;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(120.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Veteran_Mixed_Boundary_6_Items_15_Percent_Discount");
        Assertions.assertEquals(14.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Veteran_Mixed_Boundary_6_Items_15_Percent_Discount");
        Assertions.assertEquals(18.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Veteran_Mixed_Boundary_6_Items_15_Percent_Discount");
        Assertions.assertEquals(116.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Veteran_Mixed_Boundary_6_Items_15_Percent_Discount");
    }

    // Scenario: Employee_Mixed_Boundary_5_Items_20_Percent_Discount
    @Test
    void testEmployee_Mixed_Boundary_5_Items_20_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(90.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Employee_Mixed_Boundary_5_Items_20_Percent_Discount");
        Assertions.assertEquals(9.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Employee_Mixed_Boundary_5_Items_20_Percent_Discount");
        Assertions.assertEquals(18.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Employee_Mixed_Boundary_5_Items_20_Percent_Discount");
        Assertions.assertEquals(81.50, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Employee_Mixed_Boundary_5_Items_20_Percent_Discount");
    }

    // Scenario: Employee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack
    @Test
    void testEmployee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 10.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 10.00));
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 20.00));
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 30.00));
        cart.add(new Product("L2", "Luxury Item 2", ProductCategory.LUXURY, 30.00));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(120.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Employee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack");
        Assertions.assertEquals(14.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Employee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack");
        Assertions.assertEquals(24.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Employee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack");
        Assertions.assertEquals(110.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Employee_Mixed_Boundary_6_Items_20_Percent_Discount_NoStack");
    }

    // Scenario: Standard_PureFood_Volume_Discount
    @Test
    void testStandard_PureFood_Volume_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("F1", "Food Item 1", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F2", "Food Item 2", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F3", "Food Item 3", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F4", "Food Item 4", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F5", "Food Item 5", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F6", "Food Item 6", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F7", "Food Item 7", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F8", "Food Item 8", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F9", "Food Item 9", ProductCategory.FOOD, 5.00));
        cart.add(new Product("F10", "Food Item 10", ProductCategory.FOOD, 5.00));

        UserRole userRole = UserRole.STANDARD;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(50.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Standard_PureFood_Volume_Discount");
        Assertions.assertEquals(2.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Standard_PureFood_Volume_Discount");
        Assertions.assertEquals(5.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Standard_PureFood_Volume_Discount");
        Assertions.assertEquals(47.50, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Standard_PureFood_Volume_Discount");
    }

    // Scenario: Veteran_PureElectronics_Volume_Discount
    @Test
    void testVeteran_PureElectronics_Volume_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E2", "Electronics Item 2", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E3", "Electronics Item 3", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E4", "Electronics Item 4", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E5", "Electronics Item 5", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E6", "Electronics Item 6", ProductCategory.ELECTRONICS, 25.00));
        cart.add(new Product("E7", "Electronics Item 7", ProductCategory.ELECTRONICS, 25.00));

        UserRole userRole = UserRole.VETERAN;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(175.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Veteran_PureElectronics_Volume_Discount");
        Assertions.assertEquals(17.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Veteran_PureElectronics_Volume_Discount");
        Assertions.assertEquals(26.25, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Veteran_PureElectronics_Volume_Discount");
        Assertions.assertEquals(166.25, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Veteran_PureElectronics_Volume_Discount");
    }

    // Scenario: Employee_PureLuxury_SmallOrder_Discount
    @Test
    void testEmployee_PureLuxury_SmallOrder_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 50.00));
        cart.add(new Product("L2", "Luxury Item 2", ProductCategory.LUXURY, 50.00));
        cart.add(new Product("L3", "Luxury Item 3", ProductCategory.LUXURY, 50.00));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(150.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Employee_PureLuxury_SmallOrder_Discount");
        Assertions.assertEquals(22.50, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Employee_PureLuxury_SmallOrder_Discount");
        Assertions.assertEquals(30.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Employee_PureLuxury_SmallOrder_Discount");
        Assertions.assertEquals(142.50, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Employee_PureLuxury_SmallOrder_Discount");
    }

    // Scenario: Standard_EmptyCart
    @Test
    void testStandard_EmptyCart() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();

        UserRole userRole = UserRole.STANDARD;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(0.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Standard_EmptyCart");
        Assertions.assertEquals(0.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Standard_EmptyCart");
        Assertions.assertEquals(0.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Standard_EmptyCart");
        Assertions.assertEquals(0.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Standard_EmptyCart");
    }

    // Scenario: Veteran_SingleLuxuryItem_10_Percent_Discount
    @Test
    void testVeteran_SingleLuxuryItem_10_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("L1", "Luxury Item 1", ProductCategory.LUXURY, 100.00));

        UserRole userRole = UserRole.VETERAN;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(100.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Veteran_SingleLuxuryItem_10_Percent_Discount");
        Assertions.assertEquals(15.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Veteran_SingleLuxuryItem_10_Percent_Discount");
        Assertions.assertEquals(10.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Veteran_SingleLuxuryItem_10_Percent_Discount");
        Assertions.assertEquals(105.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Veteran_SingleLuxuryItem_10_Percent_Discount");
    }

    // Scenario: Employee_SingleElectronicsItem_20_Percent_Discount
    @Test
    void testEmployee_SingleElectronicsItem_20_Percent_Discount() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        cart.add(new Product("E1", "Electronics Item 1", ProductCategory.ELECTRONICS, 100.00));

        UserRole userRole = UserRole.EMPLOYEE;
        Receipt actualReceipt = service.calculate(cart, userRole);

        Assertions.assertEquals(100.00, actualReceipt.getSubtotal(), DELTA, "Subtotal mismatch for Employee_SingleElectronicsItem_20_Percent_Discount");
        Assertions.assertEquals(10.00, actualReceipt.getTaxAmount(), DELTA, "Tax mismatch for Employee_SingleElectronicsItem_20_Percent_Discount");
        Assertions.assertEquals(20.00, actualReceipt.getDiscountAmount(), DELTA, "Discount mismatch for Employee_SingleElectronicsItem_20_Percent_Discount");
        Assertions.assertEquals(90.00, actualReceipt.getGrandTotal(), DELTA, "Total mismatch for Employee_SingleElectronicsItem_20_Percent_Discount");
    }
}