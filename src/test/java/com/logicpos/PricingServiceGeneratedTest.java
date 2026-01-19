package com.logicpos;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    private PricingService pricingService;
    private static final double DELTA = 0.001; // For double comparisons

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    /**
     * Helper method to create a list of Product objects from a list of item details.
     * Each item detail map should contain "category" (String) and "price" (double).
     */
    private List<Product> createProductList(List<Map<String, Object>> itemDetails) {
        List<Product> products = new ArrayList<>();
        int idCounter = 1; // Simple unique ID generator for test products
        for (Map<String, Object> item : itemDetails) {
            String categoryStr = (String) item.get("category");
            ProductCategory category = ProductCategory.valueOf(categoryStr.toUpperCase());
            double price = ((Number) item.get("price")).doubleValue();
            products.add(new Product("item-" + (idCounter++), categoryStr, category, price));
        }
        return products;
    }

    @Test
    @DisplayName("Scenario: Standard_Electronics_NoVolume_5Items")
    void testStandard_Electronics_NoVolume_5Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(55.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_Electronics_Volume10_6Items")
    void testStandard_Electronics_Volume10_6Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(60.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.80, receipt.getTaxAmount(), DELTA);
        assertEquals(6.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(59.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_Electronics_Volume15_11Items")
    void testStandard_Electronics_Volume15_11Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(110.00, receipt.getSubtotal(), DELTA);
        assertEquals(8.80, receipt.getTaxAmount(), DELTA);
        assertEquals(16.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(103.30, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_Electronics_NoVolume_5Items")
    void testVeteran_Electronics_NoVolume_5Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.00, receipt.getTaxAmount(), DELTA);
        assertEquals(5.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(50.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_Electronics_Volume10_6Items_Stacked20")
    void testVeteran_Electronics_Volume10_6Items_Stacked20() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(60.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.80, receipt.getTaxAmount(), DELTA);
        assertEquals(12.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(53.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_Electronics_Volume15_11Items_Stacked25")
    void testVeteran_Electronics_Volume15_11Items_Stacked25() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(110.00, receipt.getSubtotal(), DELTA);
        assertEquals(8.80, receipt.getTaxAmount(), DELTA);
        assertEquals(27.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(92.30, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Employee_Electronics_NoVolume_5Items_20Percent")
    void testEmployee_Electronics_NoVolume_5Items_20Percent() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(50.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.00, receipt.getTaxAmount(), DELTA);
        assertEquals(10.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(45.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Employee_Electronics_Volume10_6Items_Max20")
    void testEmployee_Electronics_Volume10_6Items_Max20() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(60.00, receipt.getSubtotal(), DELTA);
        assertEquals(4.80, receipt.getTaxAmount(), DELTA);
        assertEquals(12.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(53.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Employee_Electronics_Volume15_11Items_Max20")
    void testEmployee_Electronics_Volume15_11Items_Max20() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(110.00, receipt.getSubtotal(), DELTA);
        assertEquals(8.80, receipt.getTaxAmount(), DELTA);
        assertEquals(22.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(97.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_Food_NoTax_3Items")
    void testStandard_Food_NoTax_3Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            items.add(Map.of("category", "Food", "price", 5.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(15.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(16.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_Luxury_HighTax_2Items")
    void testStandard_Luxury_HighTax_2Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            items.add(Map.of("category", "Luxury", "price", 100.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(200.00, receipt.getSubtotal(), DELTA);
        assertEquals(26.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(227.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_MixedCart_Small_3Items")
    void testStandard_MixedCart_Small_3Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(115.00, receipt.getSubtotal(), DELTA);
        assertEquals(13.80, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(129.80, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_MixedCart_Volume10_6Items")
    void testStandard_MixedCart_Volume10_6Items() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(230.00, receipt.getSubtotal(), DELTA);
        assertEquals(27.60, receipt.getTaxAmount(), DELTA);
        assertEquals(23.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(235.60, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_MixedCart_Volume10_6Items_Stacked20")
    void testVeteran_MixedCart_Volume10_6Items_Stacked20() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(230.00, receipt.getSubtotal(), DELTA);
        assertEquals(27.60, receipt.getTaxAmount(), DELTA);
        assertEquals(46.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(212.60, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Employee_MixedCart_Volume10_6Items_Max20")
    void testEmployee_MixedCart_Volume10_6Items_Max20() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Food", "price", 5.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Electronics", "price", 10.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        items.add(Map.of("category", "Luxury", "price", 100.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(230.00, receipt.getSubtotal(), DELTA);
        assertEquals(27.60, receipt.getTaxAmount(), DELTA);
        assertEquals(46.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(212.60, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Standard_Single_Electronics_1Item")
    void testStandard_Single_Electronics_1Item() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Electronics", "price", 25.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(25.00, receipt.getSubtotal(), DELTA);
        assertEquals(2.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(28.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_Single_Food_NoTax_1Item")
    void testVeteran_Single_Food_NoTax_1Item() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Food", "price", 15.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(15.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(1.50, receipt.getDiscountAmount(), DELTA);
        assertEquals(14.50, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: ZeroCost_Item_Standard")
    void testZeroCost_Item_Standard() {
        List<Map<String, Object>> items = new ArrayList<>();
        items.add(Map.of("category", "Electronics", "price", 0.00));
        
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(0.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(0.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(1.00, receipt.getGrandTotal(), DELTA);
    }
    
    @Test
    @DisplayName("Scenario: Employee_Electronics_10Items_Volume10_Max20")
    void testEmployee_Electronics_10Items_Volume10_Max20() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(100.00, receipt.getSubtotal(), DELTA);
        assertEquals(8.00, receipt.getTaxAmount(), DELTA);
        assertEquals(20.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(89.00, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Veteran_Electronics_10Items_Volume10_Stacked20")
    void testVeteran_Electronics_10Items_Volume10_Stacked20() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            items.add(Map.of("category", "Electronics", "price", 10.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(100.00, receipt.getSubtotal(), DELTA);
        assertEquals(8.00, receipt.getTaxAmount(), DELTA);
        assertEquals(20.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(89.00, receipt.getGrandTotal(), DELTA);
    }
    
    @Test
    @DisplayName("Scenario: Veteran_Food_11Items_Volume15_Stacked25_NoTax")
    void testVeteran_Food_11Items_Volume15_Stacked25_NoTax() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            items.add(Map.of("category", "Food", "price", 5.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(55.00, receipt.getSubtotal(), DELTA);
        assertEquals(0.00, receipt.getTaxAmount(), DELTA);
        assertEquals(13.75, receipt.getDiscountAmount(), DELTA);
        assertEquals(42.25, receipt.getGrandTotal(), DELTA);
    }

    @Test
    @DisplayName("Scenario: Employee_Luxury_11Items_Volume15_Max20_HighTax")
    void testEmployee_Luxury_11Items_Volume15_Max20_HighTax() {
        List<Map<String, Object>> items = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            items.add(Map.of("category", "Luxury", "price", 100.00));
        }
        List<Product> cart = createProductList(items);
        UserRole role = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(cart, role);

        assertEquals(1100.00, receipt.getSubtotal(), DELTA);
        assertEquals(143.00, receipt.getTaxAmount(), DELTA);
        assertEquals(220.00, receipt.getDiscountAmount(), DELTA);
        assertEquals(1024.00, receipt.getGrandTotal(), DELTA);
    }
}