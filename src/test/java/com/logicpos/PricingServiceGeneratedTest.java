import com.logicpos.*;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    @Test
    void testStandard_User_Mixed_Cart_No_Discounts() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(160.00, receipt.getSubtotal(), 0.001);
        assertEquals(20.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(180.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandard_User_Volume_Discount_6_Items() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("4", "Food2", ProductCategory.FOOD, 10.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("6", "Luxury2", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(320.00, receipt.getSubtotal(), 0.001);
        assertEquals(40.00, receipt.getTaxAmount(), 0.001);
        assertEquals(16.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(344.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandard_User_Volume_Boundary_5_Items() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("4", "Food2", ProductCategory.FOOD, 10.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 50.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(220.00, receipt.getSubtotal(), 0.001);
        assertEquals(25.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(245.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteran_User_Role_Discount_No_Volume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.VETERAN;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(160.00, receipt.getSubtotal(), 0.001);
        assertEquals(20.00, receipt.getTaxAmount(), 0.001);
        assertEquals(16.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(164.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteran_User_Volume_Stacking_Capped_15_Percent() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("4", "Food2", ProductCategory.FOOD, 10.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("6", "Luxury2", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.VETERAN;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(320.00, receipt.getSubtotal(), 0.001);
        assertEquals(40.00, receipt.getTaxAmount(), 0.001);
        assertEquals(48.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(312.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testEmployee_User_Role_Discount_No_Volume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.EMPLOYEE;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(160.00, receipt.getSubtotal(), 0.001);
        assertEquals(20.00, receipt.getTaxAmount(), 0.001);
        assertEquals(32.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(148.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testEmployee_User_Volume_Stacking_MAX_20_Percent() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("4", "Food2", ProductCategory.FOOD, 10.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("6", "Luxury2", ProductCategory.LUXURY, 100.00));
        UserRole user_role = UserRole.EMPLOYEE;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(320.00, receipt.getSubtotal(), 0.001);
        assertEquals(40.00, receipt.getTaxAmount(), 0.001);
        assertEquals(64.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(296.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testPure_Food_Cart_No_Tax() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Food2", ProductCategory.FOOD, 15.00));
        items.add(new Product("3", "Food3", ProductCategory.FOOD, 5.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(30.00, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(30.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testPure_Electronics_Cart_10_Percent_Tax() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("2", "Electronics2", ProductCategory.ELECTRONICS, 75.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(125.00, receipt.getSubtotal(), 0.001);
        assertEquals(12.50, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(137.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testPure_Luxury_Cart_15_Percent_Tax() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("2", "Luxury2", ProductCategory.LUXURY, 200.00));
        UserRole user_role = UserRole.STANDARD;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(300.00, receipt.getSubtotal(), 0.001);
        assertEquals(45.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(345.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testEmployee_Complex_Mixed_Cart_Volume_HighValue_MAX_Discount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Luxury1", ProductCategory.LUXURY, 1000.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 250.00));
        items.add(new Product("3", "Food1", ProductCategory.FOOD, 20.00));
        items.add(new Product("4", "Luxury2", ProductCategory.LUXURY, 500.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 150.00));
        items.add(new Product("6", "Food2", ProductCategory.FOOD, 30.00));
        items.add(new Product("7", "Electronics3", ProductCategory.ELECTRONICS, 75.00));
        UserRole user_role = UserRole.EMPLOYEE;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(2025.00, receipt.getSubtotal(), 0.001);
        assertEquals(272.50, receipt.getTaxAmount(), 0.001);
        assertEquals(405.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(1892.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteran_User_Volume_Boundary_5_Items_No_Volume_Discount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("1", "Food1", ProductCategory.FOOD, 10.00));
        items.add(new Product("2", "Electronics1", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("3", "Luxury1", ProductCategory.LUXURY, 100.00));
        items.add(new Product("4", "Food2", ProductCategory.FOOD, 10.00));
        items.add(new Product("5", "Electronics2", ProductCategory.ELECTRONICS, 50.00));
        UserRole user_role = UserRole.VETERAN;

        Receipt receipt = new PricingService().calculate(items, user_role);

        assertEquals(220.00, receipt.getSubtotal(), 0.001);
        assertEquals(25.00, receipt.getTaxAmount(), 0.001);
        assertEquals(22.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(223.00, receipt.getGrandTotal(), 0.001);
    }
}