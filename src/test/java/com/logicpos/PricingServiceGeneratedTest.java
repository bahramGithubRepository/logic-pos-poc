import com.logicpos.*;
import org.junit.jupiter.api.*;

import java.util.ArrayList;
import java.util.List;

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
    void testVeteranDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple")); // 0.50
        cart.add(repository.getProduct("Banana")); // 0.40
        cart.add(repository.getProduct("Bread"));  // 2.50

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        double expectedDiscount = (0.50 + 0.40 + 2.50) * 0.10;
        Assertions.assertEquals(expectedDiscount, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple")); // 6 * 0.50 = 3.00
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        double expectedDiscount = 3.00 * 0.05;
        Assertions.assertEquals(expectedDiscount, receipt.getDiscountAmount(), 0.001);
    }

     @Test
    void testLargeVolumeDiscount() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            cart.add(repository.getProduct("Apple")); // 11 * 0.50 = 5.50
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        double expectedDiscount = 5.50 * 0.10;
        Assertions.assertEquals(expectedDiscount, receipt.getDiscountAmount(), 0.001);
    }


    @Test
    void testTaxCalculation() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));      // FOOD - No tax
        cart.add(repository.getProduct("Laptop"));     // ELECTRONICS - 15% tax
        cart.add(repository.getProduct("Diamond Ring")); // LUXURY - 20% Tax

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);
        double expectedTax = (1000.00 * 0.15) + (5000.00 * 0.20);
        Assertions.assertEquals(expectedTax, receipt.getTaxAmount(), 0.001);
    }

    @Test
    void testVeteranAndVolumeDiscountStacking() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple")); // 6 * 0.50 = 3.00
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);
        double volumeDiscount = 3.00 * 0.05;
        double veteranDiscount = 3.00 * 0.10;
        double expectedDiscount = volumeDiscount + veteranDiscount;
        Assertions.assertEquals(expectedDiscount, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testEmployeeVolumeDiscountTakesHigher() {
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Apple")); // 6 * 0.50 = 3.00
        }
        Receipt receipt = pricingService.calculate(cart, UserRole.EMPLOYEE);
        double volumeDiscount = 3.00 * 0.05;
        double employeeDiscount = 3.00 * 0.20;
        double expectedDiscount = Math.max(volumeDiscount, employeeDiscount);
        Assertions.assertEquals(expectedDiscount, receipt.getDiscountAmount(), 0.001);
    }

    @Test
    void testLargeCartWithAllProductCategoriesAndVeteranDiscount() {
        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple")); // Food: 0.50
        cart.add(repository.getProduct("Laptop")); // Electronics: 1000.00
        cart.add(repository.getProduct("Diamond Ring")); // Luxury: 5000.00
        cart.add(repository.getProduct("Banana"));
        cart.add(repository.getProduct("Bread"));
        cart.add(repository.getProduct("Mouse"));
        cart.add(repository.getProduct("Keyboard"));
        cart.add(repository.getProduct("Monitor"));
        cart.add(repository.getProduct("Gold Watch"));
        cart.add(repository.getProduct("Perfume"));
        cart.add(repository.getProduct("Apple")); // Add extra item to exceed volume threshold
        cart.add(repository.getProduct("Apple")); // Add extra item to exceed volume threshold

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double subtotal = 0.50 + 1000.00 + 5000.00 + 0.40 + 2.50 + 25.00 + 50.00 + 200.00 + 2500.00 + 100.00 + 0.50 + 0.50;
        double foodSubtotal = 0.50 + 0.40 + 2.50 + 0.50 + 0.50;
        double electronicsSubtotal = 1000.00 + 25.00 + 50.00 + 200.00;
        double luxurySubtotal = 5000.00 + 2500.00 + 100.00;

        double taxAmount = (electronicsSubtotal * 0.15) + (luxurySubtotal * 0.20);

        double volumeDiscountPercent = 0.10; // Because items > 10
        double nonLuxurySubtotal = foodSubtotal + electronicsSubtotal;
        double volumeDiscountAmount = nonLuxurySubtotal * volumeDiscountPercent;
        double veteranDiscountAmount = subtotal * 0.10;
        double expectedDiscountAmount = volumeDiscountAmount + veteranDiscountAmount;

        double expectedGrandTotal = subtotal + taxAmount - expectedDiscountAmount;


        Assertions.assertEquals(subtotal, receipt.getSubtotal(), 0.001);
        Assertions.assertEquals(taxAmount, receipt.getTaxAmount(), 0.001);
        Assertions.assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        Assertions.assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }
}