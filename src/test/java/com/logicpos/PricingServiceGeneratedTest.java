import com.logicpos.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

class PricingServiceGeneratedTest {

    private PricingService pricingService;
    private InMemoryRepository repository;

    @BeforeEach
    void setUp() {
        pricingService = new PricingService();
        repository = new InMemoryRepository();
        repository.seed();
    }

    // Helper method to create a cart with specified products
    private List<Product> createCart(String... productNames) {
        List<Product> cart = new ArrayList<>();
        for (String productName : productNames) {
            cart.add(repository.getProduct(productName));
        }
        return cart;
    }

    // Helper method for assertion with delta
    private void assertReceiptValues(Receipt expected, Receipt actual, double delta) {
        assertEquals(expected.getSubtotal(), actual.getSubtotal(), delta);
        assertEquals(expected.getTaxAmount(), actual.getTaxAmount(), delta);
        assertEquals(expected.getDiscountAmount(), actual.getDiscountAmount(), delta);
        assertEquals(expected.getGrandTotal(), actual.getGrandTotal(), delta);
    }

    @Test
    void testBaseTaxCalculation_FoodOnly() {
        List<Product> cart = createCart("Apple", "Banana", "Bread");
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        Receipt expected = new Receipt(3.40, 0.0, 0.0, 3.40);
        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testBaseTaxCalculation_ElectronicsOnly() {
        List<Product> cart = createCart("Laptop", "Mouse", "Keyboard");
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double subtotal = 1075.00;
        double taxAmount = subtotal * 0.15;
        Receipt expected = new Receipt(subtotal, taxAmount, 0.0, subtotal + taxAmount);
        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testBaseTaxCalculation_MixedCart() {
        List<Product> cart = createCart("Apple", "Laptop", "Bread");
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double subtotal = 1003.0;
        double electronicsTax = repository.getProduct("Laptop").getBasePrice() * 0.15;
        double expectedTax = electronicsTax;
        Receipt expected = new Receipt(subtotal, expectedTax, 0.0, subtotal + expectedTax);
        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testVeteranDiscountApplication() {
        List<Product> cart = createCart("Apple", "Laptop", "Bread");
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double subtotal = 1003.0;
        double electronicsTax = repository.getProduct("Laptop").getBasePrice() * 0.15;
        double expectedTax = electronicsTax;
        double discount = subtotal * 0.10;
        Receipt expected = new Receipt(subtotal, expectedTax, discount, subtotal + expectedTax - discount);

        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testVolumeDiscountApplication() {
        List<Product> cart = createCart("Apple", "Banana", "Bread", "Laptop", "Mouse", "Keyboard");
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double subtotal = 1078.4;
        double electronicsTax = (repository.getProduct("Laptop").getBasePrice() + repository.getProduct("Mouse").getBasePrice() + repository.getProduct("Keyboard").getBasePrice()) * 0.15;
        double nonLuxurySubtotal = subtotal - repository.getProduct("Laptop").getBasePrice() * 0;
        double volumeDiscount = 5.0/100.0 * (subtotal);

        Receipt expected = new Receipt(subtotal, electronicsTax, 0.0, subtotal + electronicsTax);

        double nonLuxury = 0;

        for (Product p : cart) {
          if (p.getCategory() != ProductCategory.LUXURY) {
            nonLuxury += p.getBasePrice();
          }
        }

        double discount = nonLuxury * .05;

        Receipt expected2 = new Receipt(subtotal, electronicsTax, discount, subtotal + electronicsTax - discount);
        assertReceiptValues(expected2, receipt, 0.001);
    }

    @Test
    void testVolumeDiscountBoundaryCondition() {
        List<Product> cart = createCart("Apple", "Banana", "Bread", "Laptop", "Mouse");
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        double subtotal = 1028.4;
        double electronicsTax = (repository.getProduct("Laptop").getBasePrice() + repository.getProduct("Mouse").getBasePrice()) * 0.15;

        Receipt expected = new Receipt(subtotal, electronicsTax, 0.0, subtotal + electronicsTax);
        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testDiscountStacking() {
        List<Product> cart = createCart("Apple", "Banana", "Bread", "Laptop", "Mouse", "Keyboard");
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double subtotal = 1078.4;
        double electronicsTax = (repository.getProduct("Laptop").getBasePrice() + repository.getProduct("Mouse").getBasePrice() + repository.getProduct("Keyboard").getBasePrice()) * 0.15;
        double nonLuxurySubtotal = subtotal;
        double discount = subtotal * 0.15;

        Receipt expected = new Receipt(subtotal, electronicsTax, discount, subtotal + electronicsTax - discount);
        assertReceiptValues(expected, receipt, 0.001);
    }

    @Test
    void testComprehensiveGrandTotalCalculation_VeteranVolume() {
        List<Product> cart = createCart("Apple", "Banana", "Bread", "Laptop", "Mouse", "Keyboard");
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double subtotal = 1078.4;
        double electronicsTax = (repository.getProduct("Laptop").getBasePrice() + repository.getProduct("Mouse").getBasePrice() + repository.getProduct("Keyboard").getBasePrice()) * 0.15;
        double nonLuxurySubtotal = subtotal;
        double discount = subtotal * 0.15;

        Receipt expected = new Receipt(subtotal, electronicsTax, discount, subtotal + electronicsTax - discount);
        assertReceiptValues(expected, receipt, 0.001);
    }
}