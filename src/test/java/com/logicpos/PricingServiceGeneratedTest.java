import com.logicpos.*;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class PricingServiceGeneratedTest {

    @Test
    void testNo_Discount_Food_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(30.00, receipt.getGrandTotal());
    }

    @Test
    void testNo_Discount_Electronics_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(345.00, receipt.getGrandTotal());
    }

    @Test
    void testNo_Discount_Mixed() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        for (int i = 0; i < 2; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(250.00, receipt.getGrandTotal());
    }

    @Test
    void testVeteran_Discount_Food_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(27.00, receipt.getGrandTotal());
    }

    @Test
    void testVeteran_Discount_Electronics_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(315.00, receipt.getGrandTotal());
    }

    @Test
    void testVeteran_Discount_Mixed() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 2; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        for (int i = 0; i < 2; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(228.00, receipt.getGrandTotal());
    }

    @Test
    void testVolume_Discount_Food_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(57.00, receipt.getGrandTotal());
    }

    @Test
    void testVolume_Discount_Electronics_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(660.00, receipt.getGrandTotal());
    }

    @Test
    void testVolume_Discount_Mixed() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.STANDARD;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(358.50, receipt.getGrandTotal());
    }

    @Test
    void testStacking_Discount_Food_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(51.00, receipt.getGrandTotal());
    }

    @Test
    void testStacking_Discount_Electronics_Only() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 6; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(600.00, receipt.getGrandTotal());
    }

    @Test
    void testStacking_Discount_Mixed() {
        PricingService service = new PricingService();
        List<Product> cart = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Food", ProductCategory.FOOD, 10.00));
        }
        for (int i = 0; i < 3; i++) {
            cart.add(new Product(String.valueOf(i), "Electronics", ProductCategory.ELECTRONICS, 100.00));
        }
        UserRole role = UserRole.VETERAN;
        Receipt receipt = service.calculate(cart, role);
        assertEquals(325.50, receipt.getGrandTotal());
    }
}