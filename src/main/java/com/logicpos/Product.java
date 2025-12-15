package com.logicpos;

public class Product {
    private String id;
    private String name;
    private ProductCategory category;
    private double basePrice;

    public Product(String id, String name, ProductCategory category, double basePrice) {
        this.id = id;
        this.name = name;
        this.category = category;
        this.basePrice = basePrice;
    }

    public String getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public ProductCategory getCategory() {
        return category;
    }

    public double getBasePrice() {
        return basePrice;
    }
}
