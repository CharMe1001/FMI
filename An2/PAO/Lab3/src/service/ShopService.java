package service;

import model.Produs;
import model.Shop;

import java.util.Scanner;

public class ShopService {
    private Shop shop;

    public ShopService() {
        this.shop = new Shop();
    }

    public void readProduct(Scanner sc) {
        System.out.println("Input name: ");
        String nume = sc.next();

        System.out.println("Input price: ");
        double pret = sc.nextDouble();

        this.shop.addProduct(new Produs(nume, pret));
    }

    public void showProducts() {
        System.out.println("Products:");
        for (Produs produs: this.shop.getProduse()) {
            produs.show();
        }
    }
}
