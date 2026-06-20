import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import java.io.*;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

public class CartServer {
    static final double TAX_RATE = 0.08;
    static final double DISCOUNT_THRESHOLD = 200.0;
    static final double DISCOUNT_RATE = 0.10;
    static final int PORT = 8081;
    static Map<String, Cart> carts = new ConcurrentHashMap<>();

    static class CartItem {
        int id;
        String name;
        double price;
        int quantity;
        String size;
        String color;

        CartItem(int id, String name, double price, int quantity, String size, String color) {
            this.id = id;
            this.name = name;
            this.price = price;
            this.quantity = quantity;
            this.size = size != null ? size : "";
            this.color = color != null ? color : "";
        }
    }

    static class Cart {
        List<CartItem> items = Collections.synchronizedList(new ArrayList<>());
        AtomicInteger version = new AtomicInteger(0);

        synchronized void addItem(CartItem item) {
            for (CartItem existing : items) {
                if (existing.id == item.id && existing.size.equals(item.size) && existing.color.equals(item.color)) {
                    existing.quantity += item.quantity;
                    version.incrementAndGet();
                    return;
                }
            }
            items.add(item);
            version.incrementAndGet();
        }

        synchronized boolean removeItem(int productId, String size, String color, int quantity) {
            Iterator<CartItem> it = items.iterator();
            while (it.hasNext()) {
                CartItem item = it.next();
                if (item.id == productId && item.size.equals(size) && item.color.equals(color)) {
                    if (quantity >= item.quantity) {
                        it.remove();
                    } else {
                        item.quantity -= quantity;
                    }
                    version.incrementAndGet();
                    return true;
                }
            }
            return false;
        }

        synchronized void clear() {
            items.clear();
            version.incrementAndGet();
        }

        synchronized Map<String, Object> toJson() {
            double subtotal = 0;
            List<Map<String, Object>> itemsJson = new ArrayList<>();
            for (CartItem item : items) {
                Map<String, Object> i = new LinkedHashMap<>();
                i.put("id", item.id);
                i.put("name", item.name);
                i.put("price", item.price);
                i.put("quantity", item.quantity);
                i.put("size", item.size);
                i.put("color", item.color);
                itemsJson.add(i);
                subtotal += item.price * item.quantity;
            }
            double discount = subtotal >= DISCOUNT_THRESHOLD ? subtotal * DISCOUNT_RATE : 0;
            double tax = (subtotal - discount) * TAX_RATE;
            double grandTotal = subtotal - discount + tax;

            Map<String, Object> result = new LinkedHashMap<>();
            result.put("items", itemsJson);
            result.put("subtotal", Math.round(subtotal * 100.0) / 100.0);
            result.put("discount", Math.round(discount * 100.0) / 100.0);
            result.put("tax", Math.round(tax * 100.0) / 100.0);
            result.put("grand_total", Math.round(grandTotal * 100.0) / 100.0);
            result.put("item_count", items.size());
            return result;
        }
    }

    static class CartHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if ("OPTIONS".equals(exchange.getRequestMethod())) {
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
                exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            try {
                String method = exchange.getRequestMethod();
                Map<String, String> params = parseQuery(exchange.getRequestURI().getQuery());
                String sessionId = params.getOrDefault("session_id", "default");
                Cart cart = carts.computeIfAbsent(sessionId, k -> new Cart());

                String response;
                int statusCode = 200;

                switch (method) {
                    case "GET":
                        response = toJson(cart.toJson());
                        break;
                    case "POST":
                        String body = readBody(exchange);
                        Map<String, Object> data = parseJson(body);
                        int pid = ((Number) data.get("id")).intValue();
                        String name = (String) data.get("name");
                        double price = ((Number) data.get("price")).doubleValue();
                        int qty = ((Number) data.getOrDefault("quantity", 1)).intValue();
                        String size = (String) data.getOrDefault("size", "");
                        String color = (String) data.getOrDefault("color", "");
                        cart.addItem(new CartItem(pid, name, price, qty, size, color));
                        response = toJson(cart.toJson());
                        break;
                    case "DELETE":
                        String body2 = readBody(exchange);
                        if (body2 != null && !body2.isEmpty()) {
                            Map<String, Object> data2 = parseJson(body2);
                            int pid2 = ((Number) data2.get("id")).intValue();
                            String size2 = (String) data2.getOrDefault("size", "");
                            String color2 = (String) data2.getOrDefault("color", "");
                            int qty2 = ((Number) data2.getOrDefault("quantity", 1)).intValue();
                            cart.removeItem(pid2, size2, color2, qty2);
                        } else {
                            cart.clear();
                        }
                        response = toJson(cart.toJson());
                        break;
                    default:
                        response = "{\"error\":\"Method not allowed\"}";
                        statusCode = 405;
                }

                byte[] bytes = response.getBytes("UTF-8");
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.getResponseHeaders().set("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS");
                exchange.getResponseHeaders().set("Access-Control-Allow-Headers", "Content-Type");
                exchange.sendResponseHeaders(statusCode, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            } catch (Exception e) {
                String error = "{\"error\":\"" + e.getMessage().replace("\"", "'") + "\"}";
                byte[] bytes = error.getBytes("UTF-8");
                exchange.getResponseHeaders().set("Content-Type", "application/json");
                exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
                exchange.sendResponseHeaders(500, bytes.length);
                OutputStream os = exchange.getResponseBody();
                os.write(bytes);
                os.close();
            }
        }
    }

    static Map<String, String> parseQuery(String query) {
        Map<String, String> params = new LinkedHashMap<>();
        if (query == null || query.isEmpty()) return params;
        for (String pair : query.split("&")) {
            String[] kv = pair.split("=", 2);
            if (kv.length == 2) {
                try {
                    params.put(URLDecoder.decode(kv[0], "UTF-8"), URLDecoder.decode(kv[1], "UTF-8"));
                } catch (Exception e) {
                    params.put(kv[0], kv[1]);
                }
            }
        }
        return params;
    }

    static String readBody(HttpExchange exchange) throws IOException {
        InputStream is = exchange.getRequestBody();
        BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"));
        StringBuilder sb = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) {
            sb.append(line);
        }
        br.close();
        return sb.toString();
    }

    static Map<String, Object> parseJson(String json) {
        Map<String, Object> map = new LinkedHashMap<>();
        if (json == null || json.trim().isEmpty()) return map;
        json = json.trim();
        if (!json.startsWith("{") || !json.endsWith("}")) return map;
        json = json.substring(1, json.length() - 1).trim();
        if (json.isEmpty()) return map;
        boolean inString = false;
        StringBuilder key = new StringBuilder();
        StringBuilder value = new StringBuilder();
        boolean parsingKey = true;
        for (int i = 0; i < json.length(); i++) {
            char c = json.charAt(i);
            if (c == '"') {
                inString = !inString;
                continue;
            }
            if (!inString) {
                if (c == ':') {
                    parsingKey = false;
                    continue;
                }
                if (c == ',' || c == '}') {
                    if (key.length() > 0) {
                        map.put(key.toString().trim(), parseJsonValue(value.toString().trim()));
                    }
                    key = new StringBuilder();
                    value = new StringBuilder();
                    parsingKey = true;
                    continue;
                }
                if (c == '{' || c == '}' || c == '[' || c == ']') continue;
            }
            if (parsingKey) key.append(c);
            else value.append(c);
        }
        if (key.length() > 0) {
            map.put(key.toString().trim(), parseJsonValue(value.toString().trim()));
        }
        return map;
    }

    static Object parseJsonValue(String val) {
        val = val.trim();
        if (val.isEmpty()) return "";
        if (val.equals("null")) return null;
        if (val.equals("true")) return true;
        if (val.equals("false")) return false;
        if (val.startsWith("\"") && val.endsWith("\"")) return val.substring(1, val.length() - 1);
        try {
            if (val.contains(".")) return Double.parseDouble(val);
            else return Integer.parseInt(val);
        } catch (NumberFormatException e) {
            return val;
        }
    }

    static String toJson(Object obj) {
        if (obj == null) return "null";
        if (obj instanceof String) return "\"" + ((String) obj).replace("\\", "\\\\").replace("\"", "\\\"") + "\"";
        if (obj instanceof Number || obj instanceof Boolean) return obj.toString();
        if (obj instanceof Map) {
            StringBuilder sb = new StringBuilder("{");
            for (Map.Entry<String, Object> e : ((Map<String, Object>) obj).entrySet()) {
                if (sb.length() > 1) sb.append(",");
                sb.append("\"").append(e.getKey()).append("\":").append(toJson(e.getValue()));
            }
            sb.append("}");
            return sb.toString();
        }
        if (obj instanceof List) {
            StringBuilder sb = new StringBuilder("[");
            for (Object e : (List<?>) obj) {
                if (sb.length() > 1) sb.append(",");
                sb.append(toJson(e));
            }
            sb.append("]");
            return sb.toString();
        }
        return "\"" + obj.toString() + "\"";
    }

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);
        server.createContext("/cart", new CartHandler());
        server.setExecutor(java.util.concurrent.Executors.newFixedThreadPool(4));
        server.start();
        System.out.println("Java Cart Service running on http://localhost:" + PORT);
        System.out.println("Tax rate: " + (TAX_RATE * 100) + "%");
        System.out.println("Discount: " + (DISCOUNT_RATE * 100) + "% off orders over $" + DISCOUNT_THRESHOLD);
    }
}
