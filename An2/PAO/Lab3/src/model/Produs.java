package model;

public class Produs {
    private String nume;
    private double pret;

    Produs() {
        this.nume = "";
        this.pret = 0.0;
    }

    public Produs(String nume, double pret) {
        this.nume = nume;
        this.pret = pret;
    }

    public void show() {
        System.out.println("Nume: " + this.nume + ", Pret: " + this.pret);
    }
}
