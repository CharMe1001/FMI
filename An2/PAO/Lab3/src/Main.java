import service.ShopService;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        ShopService service = new ShopService();
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.println("Input command(1 - add product, 2 - show products, 3 - exit): ");
            int task = sc.nextInt();

            switch (task) {
                case 1: {
                    service.readProduct(sc);
                    break;
                }
                case 2: {
                    service.showProducts();
                    break;
                }
                case 3: {
                    return;
                }
                default: {
                    System.out.println("Wrong argument. Try again.");
                }
            }
        }
    }
}