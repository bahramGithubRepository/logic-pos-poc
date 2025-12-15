package com.logicpos;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // 1. Initialize
        InMemoryRepository repo = new InMemoryRepository();
        repo.seed();
        PricingService service = new PricingService();

        // 2. Build Cart
        List<Product> cart = new ArrayList<>();
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Apple"));
        cart.add(repo.getProduct("Laptop"));

        // 3. Set User Role
        UserRole role = UserRole.VETERAN;

        // 4. Calculate
        Receipt receipt = service.calculate(cart, role);

        // 5. Print
        System.out.println("Processing Cart for " + role);
        System.out.println("Items: 3 x Apple, 1 x Laptop");
        System.out.println(receipt);
    }
}
