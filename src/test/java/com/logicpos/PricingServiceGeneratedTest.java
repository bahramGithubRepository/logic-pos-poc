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

    @Test
    void verifyTaxForFoodItems() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void verifyTaxForElectronicsItems() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void verifyMixedCategoryTaxCalculation() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Laptop"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void verifyVeteranDiscountOnly() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));
        cart.add(repository.getProduct("Laptop"));
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(300.0, receipt.getTaxAmount(), 0.001);
        assertEquals(200.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(2100.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyVolumeDiscountOnly() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(900.0, receipt.getTaxAmount(), 0.001);
        assertEquals(300.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(6100.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyVolumeDiscountThreshold() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(750.0, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(5750.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyNoDiscountCondition() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));
        cart.add(repository.getProduct("Apple"));
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(1.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyAdditiveDiscountStacking() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(900.0, receipt.getTaxAmount(), 0.001);
        assertEquals(900.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(5100.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyAdditiveDiscountStackingWithMixedCart() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Laptop"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(450.0, receipt.getTaxAmount(), 0.001);
        assertEquals(457.5, receipt.getDiscountAmount(), 0.001);
        assertEquals(3492.5, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void verifyTaxCalculationOrderWithAllFoodItems() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
        assertEquals(0.45, receipt.getDiscountAmount(), 0.001);
        assertEquals(2.55, receipt.getGrandTotal(), 0.001);
    }
}