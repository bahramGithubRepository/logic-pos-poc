package com.logicpos;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class PricingServiceGeneratedTest {

    private PricingService pricingService;
    private static final double DELTA = 0.01; // Tolerance for double comparisons in currency calculations

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    /**
     * Helper method to create a list of Product objects from a list of ItemInput.
     * This decouples the test from specific seeded products in InMemoryRepository,
     * allowing flexible product definition based on test requirements.
     */
    private List<Product> createCart(List<ItemInput> itemInputs) {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < itemInputs.size(); i++) {
            ItemInput itemInput = itemInputs.get(i);
            // Create a generic product for testing based on category and price.
            // ID and Name are not used in PricingService's calculation logic.
            ProductCategory category = ProductCategory.valueOf(itemInput.getCategory().toUpperCase());
            Product product = new Product(UUID.randomUUID().toString(), "TestItem-" + i, category, itemInput.getPrice());
            cart.add(product);
        }
        return cart;
    }

    /**
     * Helper class to represent item inputs from the JSON requirements,
     * simplifying the creation of test data.
     */
    private static class ItemInput {
        private String category;
        private double price;

        public ItemInput(String category, double price) {
            this.category = category;
            this.price = price;
        }

        public String getCategory() {
            return category;
        }

        public double getPrice() {
            return price;
        }
    }

    // --- Test Scenarios based on Requirements ---

    @Test
    @DisplayName("Standard_Mixed_3_Items_NoDiscount")
    void testStandardMixed3ItemsNoDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(160.00, receipt.getSubtotal(), DELTA);
        assertEquals(12.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(172.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Standard_Mixed_5_Items_NoDiscount_Boundary")
    void testStandardMixed5ItemsNoDiscountBoundary() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(220.00, receipt.getSubtotal(), DELTA);
        assertEquals(16.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(236.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Standard_Mixed_6_Items_VolumeDiscount_Boundary")
    void testStandardMixed6ItemsVolumeDiscountBoundary() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(320.00, receipt.getSubtotal(), DELTA);
        assertEquals(24.00, receipt.getTaxAmount(), DELTA);
        assertEquals(32.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(312.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Standard_PureFood_5_Items")
    void testStandardPureFood5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(50.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Standard_PureElectronics_5_Items")
    void testStandardPureElectronics5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(250.00, receipt.getSubtotal(), DELTA);
        assertEquals(20.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(270.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Standard_PureLuxury_5_Items")
    void testStandardPureLuxury5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.STANDARD;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(500.00, receipt.getSubtotal(), DELTA);
        assertEquals(40.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(540.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Veteran_Mixed_3_Items_VeteranDiscount")
    void testVeteranMixed3ItemsVeteranDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.VETERAN;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(160.00, receipt.getSubtotal(), DELTA);
        assertEquals(12.00, receipt.getTaxAmount(), DELTA);
        assertEquals(24.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(148.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Veteran_Mixed_5_Items_VeteranDiscount")
    void testVeteranMixed5ItemsVeteranDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.VETERAN;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(220.00, receipt.getSubtotal(), DELTA);
        assertEquals(16.00, receipt.getTaxAmount(), DELTA);
        assertEquals(33.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(203.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Veteran_Mixed_6_Items_AdditiveDiscount")
    void testVeteranMixed6ItemsAdditiveDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.VETERAN;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(320.00, receipt.getSubtotal(), DELTA);
        assertEquals(24.00, receipt.getTaxAmount(), DELTA);
        assertEquals(80.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(264.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Veteran_PureFood_5_Items")
    void testVeteranPureFood5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        UserRole role = UserRole.VETERAN;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(7.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(42.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Veteran_PureElectronics_5_Items")
    void testVeteranPureElectronics5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        UserRole role = UserRole.VETERAN;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(250.00, receipt.getSubtotal(), DELTA);
        assertEquals(20.00, receipt.getTaxAmount(), DELTA);
        assertEquals(37.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(232.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Employee_Mixed_3_Items_EmployeeDiscount")
    void testEmployeeMixed3ItemsEmployeeDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.EMPLOYEE;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(160.00, receipt.getSubtotal(), DELTA);
        assertEquals(12.00, receipt.getTaxAmount(), DELTA);
        assertEquals(40.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(132.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Employee_Mixed_5_Items_EmployeeDiscount")
    void testEmployeeMixed5ItemsEmployeeDiscount() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.EMPLOYEE;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(220.00, receipt.getSubtotal(), DELTA);
        assertEquals(16.00, receipt.getTaxAmount(), DELTA);
        assertEquals(55.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(181.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Employee_Mixed_6_Items_MaxDiscount_Complex")
    void testEmployeeMixed6ItemsMaxDiscountComplex() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Luxury", 100.00));
        items.add(new ItemInput("Luxury", 100.00));
        UserRole role = UserRole.EMPLOYEE;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(320.00, receipt.getSubtotal(), DELTA);
        assertEquals(24.00, receipt.getTaxAmount(), DELTA);
        assertEquals(80.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(264.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Employee_PureFood_5_Items")
    void testEmployeePureFood5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        items.add(new ItemInput("Food", 10.00));
        UserRole role = UserRole.EMPLOYEE;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(12.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(37.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Employee_PureElectronics_5_Items")
    void testEmployeePureElectronics5Items() {
        List<ItemInput> items = new ArrayList<>();
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        items.add(new ItemInput("Electronics", 50.00));
        UserRole role = UserRole.EMPLOYEE;

        List<Product> cart = createCart(items);
        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(250.00, receipt.getSubtotal(), DELTA);
        assertEquals(20.00, receipt.getTaxAmount(), DELTA);
        assertEquals(62.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(207.50, receipt.getGrandTotal(), DELTA);
    }
}