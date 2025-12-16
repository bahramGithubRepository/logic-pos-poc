import com.logicpos.*;
import org.junit.jupiter.api.*;

import java.util.Arrays;
import java.util.List;

public class PricingServiceGeneratedTest {

    private PricingService pricingService;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
    }

    @Test
    void testVeteranDiscount() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Banana", ProductCategory.FOOD, 0.5);
        List<Product> cart = Arrays.asList(product1, product2);

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 1.5;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = expectedSubtotal * 0.10; // 10% Veteran discount
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Banana", ProductCategory.FOOD, 0.5);
        Product product3 = new Product("3", "Orange", ProductCategory.FOOD, 1.2);
        Product product4 = new Product("4", "Grapes", ProductCategory.FOOD, 2.3);
        Product product5 = new Product("5", "Melon", ProductCategory.FOOD, 3.0);
        Product product6 = new Product("6", "Mango", ProductCategory.FOOD, 1.7);

        List<Product> cart = Arrays.asList(product1, product2, product3, product4, product5, product6);

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 9.7;
        double expectedTaxAmount = 0.0;
        double expectedDiscountAmount = expectedSubtotal * 0.05; // 5% Volume discount
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testTaxCalculation() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Laptop", ProductCategory.ELECTRONICS, 100.0);
        Product product3 = new Product("3", "Handbag", ProductCategory.LUXURY, 50.0);

        List<Product> cart = Arrays.asList(product1, product2, product3);

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 151.0;
        double expectedTaxAmount = 100.0 * 0.15 + 50.0 * 0.20;  // Electronics (15%) + Luxury (20%)
        double expectedDiscountAmount = 0.0;
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranDiscountStacksWithVolumeDiscount() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Banana", ProductCategory.FOOD, 0.5);
        Product product3 = new Product("3", "Orange", ProductCategory.FOOD, 1.2);
        Product product4 = new Product("4", "Grapes", ProductCategory.FOOD, 2.3);
        Product product5 = new Product("5", "Melon", ProductCategory.FOOD, 3.0);
        Product product6 = new Product("6", "Mango", ProductCategory.FOOD, 1.7);

        List<Product> cart = Arrays.asList(product1, product2, product3, product4, product5, product6);

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 9.7;
        double expectedTaxAmount = 0.0;

        double volumeDiscount = expectedSubtotal * 0.05;
        double veteranDiscount = expectedSubtotal * 0.10;
        double expectedDiscountAmount = veteranDiscount + volumeDiscount;

        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVolumeDiscountOnlyAppliesToNonLuxuryItems() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Banana", ProductCategory.FOOD, 0.5);
        Product product3 = new Product("3", "Orange", ProductCategory.FOOD, 1.2);
        Product product4 = new Product("4", "Grapes", ProductCategory.FOOD, 2.3);
        Product product5 = new Product("5", "Melon", ProductCategory.FOOD, 3.0);
        Product product6 = new Product("6", "Mango", ProductCategory.FOOD, 1.7);
        Product product7 = new Product("7", "Diamond Ring", ProductCategory.LUXURY, 1000.0);

        List<Product> cart = Arrays.asList(product1, product2, product3, product4, product5, product6, product7);

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double expectedSubtotal = 1009.7;
        double expectedTaxAmount = 1000.0 * 0.20;
        double nonLuxurySubtotal = expectedSubtotal - 1000.0; // Remove luxury item for volume discount calculation
        double expectedDiscountAmount = nonLuxurySubtotal * 0.05; // 5% Volume discount
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testEmployeeDiscountTakesLargerValue() {
        Product product1 = new Product("1", "Apple", ProductCategory.FOOD, 1.0);
        Product product2 = new Product("2", "Banana", ProductCategory.FOOD, 0.5);
        Product product3 = new Product("3", "Orange", ProductCategory.FOOD, 1.2);
        Product product4 = new Product("4", "Grapes", ProductCategory.FOOD, 2.3);
        Product product5 = new Product("5", "Melon", ProductCategory.FOOD, 3.0);
        Product product6 = new Product("6", "Mango", ProductCategory.FOOD, 1.7);
        Product product7 = new Product("7", "Diamond Ring", ProductCategory.LUXURY, 1000.0);
        Product product8 = new Product("8", "TV", ProductCategory.ELECTRONICS, 500.0);
        Product product9 = new Product("9", "Chair", ProductCategory.FOOD, 50.0);
        Product product10 = new Product("10", "Computer", ProductCategory.ELECTRONICS, 1000.0);
        Product product11 = new Product("11", "Tablet", ProductCategory.ELECTRONICS, 250.0);

        List<Product> cart = Arrays.asList(product1, product2, product3, product4, product5, product6, product7, product8, product9, product10, product11);
        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);

        double expectedSubtotal = 2809.7;
        double expectedTaxAmount = 500.0 * 0.15 + 1000.0 * 0.15 + 250.0 * 0.15 + 1000.0 * 0.20; //Electronics + Luxury
        double volumeDiscount = (expectedSubtotal - 1000.0) * 0.10; // luxury removed
        double employeeDiscount = expectedSubtotal * 0.20;
        double expectedDiscountAmount = Math.max(volumeDiscount, employeeDiscount);
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        Assertions.assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }
}