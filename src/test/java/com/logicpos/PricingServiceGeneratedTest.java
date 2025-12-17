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

    @Test
    void testStandardCustomerBuysSingleFoodItem() {
        // Scenario: Standard Customer Buys Single Food Item (Tax Exemption Verification)
        // Description: A STANDARD customer purchases 1 'Apple' (Category: FOOD, Price: $0.50).
        // Expected Outcome: Subtotal: $0.50. Tax Amount: $0 (0% on FOOD items). Discount Amount: $0. Grand Total: $0.50.

        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Apple"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(0.50, receipt.getSubtotal(), 0.001);
        assertEquals(0.0, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(0.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerBuysSingleElectronicsItem() {
        // Scenario: Standard Customer Buys Single Electronics Item (15% Tax Verification)
        // Description: A STANDARD customer purchases 1 'Laptop' (Category: ELECTRONICS, Price: $1000).
        // Expected Outcome: Subtotal: $1000. Tax Amount: $150 (15% on ELECTRONICS items). Discount Amount: $0. Grand Total: $1150.

        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(1000.0, receipt.getSubtotal(), 0.001);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(1150.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerBuysSingleElectronicsItem() {
        // Scenario: Veteran Customer Buys Single Electronics Item (10% Veteran Discount)
        // Description: A VETERAN customer purchases 1 'Laptop' (Category: ELECTRONICS, Price: $1000).
        // Expected Outcome: Subtotal: $1000. Tax Amount: $150 (15% on ELECTRONICS). Discount Amount: $100 (10% Veteran discount on $1000 subtotal). Grand Total: $1050 (1000 + 150 - 100).

        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Laptop"));

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        assertEquals(1000.0, receipt.getSubtotal(), 0.001);
        assertEquals(150.0, receipt.getTaxAmount(), 0.001);
        assertEquals(100.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(1050.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerBuysExactly5ElectronicsItems() {
        // Scenario: Standard Customer Buys Exactly 5 Electronics Items (Volume Discount Boundary - NO Discount)
        // Description: A STANDARD customer purchases 5 'Mouse' items (Category: ELECTRONICS, Price: $25 each). Total quantity: 5.
        // Expected Outcome: Subtotal: $125 (5 * $25). Tax Amount: $18.75 (15% on $125). Discount Amount: $0 (Volume discount applies strictly for > 5 items). Grand Total: $143.75 (125 + 18.75 - 0).

        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 5; i++) {
            cart.add(repository.getProduct("Mouse"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(125.0, receipt.getSubtotal(), 0.001);
        assertEquals(18.75, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(143.75, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerBuysExactly6ElectronicsItems() {
        // Scenario: Standard Customer Buys Exactly 6 Electronics Items (Volume Discount Boundary - Discount APPLIES)
        // Description: A STANDARD customer purchases 6 'Mouse' items (Category: ELECTRONICS, Price: $25 each). Total quantity: 6.
        // Expected Outcome: Subtotal: $150 (6 * $25). Tax Amount: $22.5 (15% on $150). Discount Amount: $7.5 (5% Volume discount on $150 subtotal). Grand Total: $165 (150 + 22.5 - 7.5).

        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(repository.getProduct("Mouse"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(150.0, receipt.getSubtotal(), 0.001);
        assertEquals(22.5, receipt.getTaxAmount(), 0.001);
        assertEquals(7.5, receipt.getDiscountAmount(), 0.001);
        assertEquals(165.0, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testVeteranCustomerBuys6MixedItemsStackedDiscountAndMixedTax() {
        // Scenario: CRITICAL: Veteran Customer Buys 6 Mixed Items (Stacked 15% Discount & Mixed Tax)
        // Description: A VETERAN customer purchases 6 items: 3 'Apple' (FOOD, $0.50 each) and 3 'Monitor' (ELECTRONICS, $200 each). Total quantity: 6.
        // Expected Outcome: Product Breakdown: 3 FOOD items (Subtotal: $1.50), 3 ELECTRONICS items (Subtotal: $600). Overall Subtotal: $601.50. Tax Calculation: $0 on FOOD items, $90 (15% on $600) on ELECTRONICS items. Total Tax Amount: $90. Discount Calculation: 10% (Veteran) + 5% (Volume for > 5 items) = 15% total discount. Discount Amount: $90.225 (15% of $601.50 subtotal). Grand Total: $601.275 (601.50 + 90 - 90.225).

        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Apple"));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(repository.getProduct("Monitor"));
        }

        Receipt receipt = pricingService.calculate(cart, UserRole.VETERAN);

        double expectedSubtotal = 601.50;
        double expectedTaxAmount = 90.0;
        double expectedDiscountAmount = 601.50 * 0.15;
        double expectedGrandTotal = expectedSubtotal + expectedTaxAmount - expectedDiscountAmount;

        assertEquals(expectedSubtotal, receipt.getSubtotal(), 0.001);
        assertEquals(expectedTaxAmount, receipt.getTaxAmount(), 0.001);
        assertEquals(expectedDiscountAmount, receipt.getDiscountAmount(), 0.001);
        assertEquals(expectedGrandTotal, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void testStandardCustomerBuysMixedFoodAndElectronicsItems() {
        // Scenario: Standard Customer Buys Mixed Food and Electronics Items (Verify Category-Specific Tax)
        // Description: A STANDARD customer purchases 1 'Banana' (FOOD, $0.40) and 1 'Keyboard' (ELECTRONICS, $50).
        // Expected Outcome: Product Breakdown: 1 FOOD item (Subtotal: $0.40), 1 ELECTRONICS item (Subtotal: $50). Overall Subtotal: $50.40. Tax Calculation: $0 on FOOD item, $7.50 (15% on $50) on ELECTRONICS item. Total Tax Amount: $7.50. Discount Amount: $0. Grand Total: $57.90 (50.40 + 7.50 - 0).

        List<Product> cart = new ArrayList<>();
        cart.add(repository.getProduct("Banana"));
        cart.add(repository.getProduct("Keyboard"));

        Receipt receipt = pricingService.calculate(cart, UserRole.STANDARD);

        assertEquals(50.40, receipt.getSubtotal(), 0.001);
        assertEquals(7.50, receipt.getTaxAmount(), 0.001);
        assertEquals(0.0, receipt.getDiscountAmount(), 0.001);
        assertEquals(57.90, receipt.getGrandTotal(), 0.001);
    }
}