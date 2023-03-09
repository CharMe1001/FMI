package model;

import java.util.*;

public class Shop {
    private List<Produs> produse;

    public Shop() {
        this.produse = new ArrayList<>();
    }

    public void addProduct(Produs produs) {
        this.produse.add(produs);
    }

    public List<Produs> getProduse() {
        return new ArrayList<>(this.produse);
    }

}
