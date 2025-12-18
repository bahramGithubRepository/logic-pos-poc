package com.logicpos;

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
    void Standard_PureFood_NoVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("11", "Item1", ProductCategory.FOOD, 10.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(10.00, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(10.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Standard_PureElectronics_NoVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("12", "Item2", ProductCategory.ELECTRONICS, 100.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(100.00, receipt.getSubtotal(), 0.001);
        assertEquals(10.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(110.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Standard_PureLuxury_NoVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("13", "Item3", ProductCategory.LUXURY, 200.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(200.00, receipt.getSubtotal(), 0.001);
        assertEquals(40.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(240.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Veteran_PureElectronics_NoVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("14", "Item4", ProductCategory.ELECTRONICS, 100.00));
        UserRole userRole = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(100.00, receipt.getSubtotal(), 0.001);
        assertEquals(10.00, receipt.getTaxAmount(), 0.001);
        assertEquals(10.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(100.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Employee_PureLuxury_NoVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("15", "Item5", ProductCategory.LUXURY, 200.00));
        UserRole userRole = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(200.00, receipt.getSubtotal(), 0.001);
        assertEquals(40.00, receipt.getTaxAmount(), 0.001);
        assertEquals(40.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(200.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Standard_MixedCart_5Items_NoVolumeDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("16", "Item6", ProductCategory.FOOD, 10.00));
        items.add(new Product("17", "Item7", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("18", "Item8", ProductCategory.LUXURY, 100.00));
        items.add(new Product("19", "Item9", ProductCategory.FOOD, 5.00));
        items.add(new Product("20", "Item10", ProductCategory.ELECTRONICS, 20.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(185.00, receipt.getSubtotal(), 0.001);
        assertEquals(27.00, receipt.getTaxAmount(), 0.001);
        assertEquals(0.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(212.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Standard_MixedCart_6Items_WithVolumeDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("21", "Item11", ProductCategory.FOOD, 10.00));
        items.add(new Product("22", "Item12", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("23", "Item13", ProductCategory.LUXURY, 100.00));
        items.add(new Product("24", "Item14", ProductCategory.FOOD, 5.00));
        items.add(new Product("25", "Item15", ProductCategory.ELECTRONICS, 20.00));
        items.add(new Product("26", "Item16", ProductCategory.LUXURY, 30.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(215.00, receipt.getSubtotal(), 0.001);
        assertEquals(33.00, receipt.getTaxAmount(), 0.001);
        assertEquals(10.75, receipt.getDiscountAmount(), 0.001);
        assertEquals(237.25, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Veteran_MixedCart_5Items_NoVolumeDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("27", "Item17", ProductCategory.FOOD, 10.00));
        items.add(new Product("28", "Item18", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("29", "Item19", ProductCategory.LUXURY, 100.00));
        items.add(new Product("30", "Item20", ProductCategory.FOOD, 5.00));
        items.add(new Product("31", "Item21", ProductCategory.ELECTRONICS, 20.00));
        UserRole userRole = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(185.00, receipt.getSubtotal(), 0.001);
        assertEquals(27.00, receipt.getTaxAmount(), 0.001);
        assertEquals(18.50, receipt.getDiscountAmount(), 0.001);
        assertEquals(193.50, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Veteran_MixedCart_6Items_Verify15PercentTotalDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("32", "Item22", ProductCategory.FOOD, 10.00));
        items.add(new Product("33", "Item23", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("34", "Item24", ProductCategory.LUXURY, 100.00));
        items.add(new Product("35", "Item25", ProductCategory.FOOD, 5.00));
        items.add(new Product("36", "Item26", ProductCategory.ELECTRONICS, 20.00));
        items.add(new Product("37", "Item27", ProductCategory.LUXURY, 30.00));
        UserRole userRole = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(215.00, receipt.getSubtotal(), 0.001);
        assertEquals(33.00, receipt.getTaxAmount(), 0.001);
        assertEquals(32.25, receipt.getDiscountAmount(), 0.001);
        assertEquals(215.75, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Employee_MixedCart_5Items_NoVolumeDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("38", "Item28", ProductCategory.FOOD, 10.00));
        items.add(new Product("39", "Item29", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("40", "Item30", ProductCategory.LUXURY, 100.00));
        items.add(new Product("41", "Item31", ProductCategory.FOOD, 5.00));
        items.add(new Product("42", "Item32", ProductCategory.ELECTRONICS, 20.00));
        UserRole userRole = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(185.00, receipt.getSubtotal(), 0.001);
        assertEquals(27.00, receipt.getTaxAmount(), 0.001);
        assertEquals(37.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(175.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Employee_MixedCart_6Items_Verify20PercentTotalDiscount_OverrideVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("43", "Item33", ProductCategory.FOOD, 10.00));
        items.add(new Product("44", "Item34", ProductCategory.ELECTRONICS, 50.00));
        items.add(new Product("45", "Item35", ProductCategory.LUXURY, 100.00));
        items.add(new Product("46", "Item36", ProductCategory.FOOD, 5.00));
        items.add(new Product("47", "Item37", ProductCategory.ELECTRONICS, 20.00));
        items.add(new Product("48", "Item38", ProductCategory.LUXURY, 30.00));
        UserRole userRole = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(215.00, receipt.getSubtotal(), 0.001);
        assertEquals(33.00, receipt.getTaxAmount(), 0.001);
        assertEquals(43.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(205.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Standard_PureFood_6Items_WithVolumeDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("49", "Item39", ProductCategory.FOOD, 10.00));
        items.add(new Product("50", "Item40", ProductCategory.FOOD, 10.00));
        items.add(new Product("51", "Item41", ProductCategory.FOOD, 10.00));
        items.add(new Product("52", "Item42", ProductCategory.FOOD, 10.00));
        items.add(new Product("53", "Item43", ProductCategory.FOOD, 10.00));
        items.add(new Product("54", "Item44", ProductCategory.FOOD, 10.00));
        UserRole userRole = UserRole.STANDARD;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(60.00, receipt.getSubtotal(), 0.001);
        assertEquals(0.00, receipt.getTaxAmount(), 0.001);
        assertEquals(3.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(57.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Veteran_PureLuxury_6Items_Verify15PercentTotalDiscount() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("55", "Item45", ProductCategory.LUXURY, 100.00));
        items.add(new Product("56", "Item46", ProductCategory.LUXURY, 100.00));
        items.add(new Product("57", "Item47", ProductCategory.LUXURY, 100.00));
        items.add(new Product("58", "Item48", ProductCategory.LUXURY, 100.00));
        items.add(new Product("59", "Item49", ProductCategory.LUXURY, 100.00));
        items.add(new Product("60", "Item50", ProductCategory.LUXURY, 100.00));
        UserRole userRole = UserRole.VETERAN;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(600.00, receipt.getSubtotal(), 0.001);
        assertEquals(120.00, receipt.getTaxAmount(), 0.001);
        assertEquals(90.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(630.00, receipt.getGrandTotal(), 0.001);
    }

    @Test
    void Employee_PureElectronics_6Items_Verify20PercentTotalDiscount_OverrideVolume() {
        List<Product> items = new ArrayList<>();
        items.add(new Product("61", "Item51", ProductCategory.ELECTRONICS, 100.00));
        items.add(new Product("62", "Item52", ProductCategory.ELECTRONICS, 100.00));
        items.add(new Product("63", "Item53", ProductCategory.ELECTRONICS, 100.00));
        items.add(new Product("64", "Item54", ProductCategory.ELECTRONICS, 100.00));
        items.add(new Product("65", "Item55", ProductCategory.ELECTRONICS, 100.00));
        items.add(new Product("66", "Item56", ProductCategory.ELECTRONICS, 100.00));
        UserRole userRole = UserRole.EMPLOYEE;

        Receipt receipt = pricingService.calculate(items, userRole);

        assertEquals(600.00, receipt.getSubtotal(), 0.001);
        assertEquals(60.00, receipt.getTaxAmount(), 0.001);
        assertEquals(120.00, receipt.getDiscountAmount(), 0.001);
        assertEquals(540.00, receipt.getGrandTotal(), 0.001);
    }
}