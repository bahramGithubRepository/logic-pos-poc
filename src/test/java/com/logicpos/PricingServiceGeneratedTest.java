import com.logicpos.*;
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

    // I. Taxation Logic Verification
    @Test
    void testSingleFoodItemTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testMultipleFoodItemsTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Banana"));
        cart.add(repository.getProduct("Bread"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testSingleElectronicsItemTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testMultipleElectronicsItemsTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));
        cart.add(repository.getProduct("Mouse"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(153.75, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testMixedFoodAndElectronicsItemsTax() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Laptop"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
    }

    // II. Discount Logic Verification (Individual)
    @Test
    void testVeteranDiscountSmallPurchase() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Banana"));
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(0.09, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testStandardVolumeDiscountLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.15, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testStandardNoDiscountSmallPurchase() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Banana"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
    }

    // III. Discount Stacking Verification
    @Test
    void testVeteranDiscountStacking() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(0.45, receipt.getDiscountAmount(), 0.001);
    }

    // IV. Combined Taxation and Discount Logic Verification
    @Test
    void testVeteranElectronicsLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(330.0, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testStandardElectronicsLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(150.0, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testVeteranMixedItemsLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(165.15, receipt.getDiscountAmount(), 0.001);
    }

     @Test
    void testStandardMixedItemsLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(75.15, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testVeteranFoodLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(0.45, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testStandardFoodLargePurchase() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.15, receipt.getDiscountAmount(), 0.001);
    }

    // V. Edge Case / No Discounts Scenarios
    @Test
    void testVeteranFoodSmallPurchase() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Banana"));
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(0.09, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testStandardElectronicsSmallPurchase() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));
        cart.add(repository.getProduct("Mouse"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
    }
}