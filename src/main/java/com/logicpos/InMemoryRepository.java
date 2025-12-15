package com.logicpos;

import java.util.HashMap;
import java.util.Map;

public class InMemoryRepository {
    private Map<String, Product> products = new HashMap<>();

    public void seed() {
        // Food
        products.put("Apple", new Product("1", "Apple", ProductCategory.FOOD, 0.50));
        products.put("Banana", new Product("2", "Banana", ProductCategory.FOOD, 0.40));
        products.put("Bread", new Product("3", "Bread", ProductCategory.FOOD, 2.50));
        
        // Electronics
        products.put("Laptop", new Product("4", "Laptop", ProductCategory.ELECTRONICS, 1000.00));
        products.put("Mouse", new Product("5", "Mouse", ProductCategory.ELECTRONICS, 25.00));
        products.put("Keyboard", new Product("6", "Keyboard", ProductCategory.ELECTRONICS, 50.00));
        products.put("Monitor", new Product("7", "Monitor", ProductCategory.ELECTRONICS, 200.00));

        // Luxury
        products.put("Diamond Ring", new Product("8", "Diamond Ring", ProductCategory.LUXURY, 5000.00));
        products.put("Gold Watch", new Product("9", "Gold Watch", ProductCategory.LUXURY, 2500.00));
        products.put("Perfume", new Product("10", "Perfume", ProductCategory.LUXURY, 100.00));
    }

    public Product getProduct(String name) {
        return products.get(name);
    }
}
