<?php
require_once __DIR__ . '/../src/functions.php';

$method = $_SERVER['REQUEST_METHOD'];
$path = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

$routes = [
    'POST' => [
        '/api/login' => 'login',
        '/api/products' => 'create_product'
    ],
    'GET' => [
        '/api/products' => 'list_products',
    ]
];

if (isset($routes[$method][$path])) {
    call_user_func($routes[$method][$path]);
} else {
    json_response(['error' => 'Not Found'], 404);
}

function login() {
    $db = get_db_connection();
    $input = json_decode(file_get_contents('php://input'), true);
    $stmt = $db->prepare('SELECT * FROM users WHERE username = ?');
    $stmt->execute([$input['username']]);
    $user = $stmt->fetch();
    if ($user && verify_password($input['password'], $user['password'])) {
        // simplified token
        $token = base64_encode(json_encode(['uid' => $user['id'], 'ts' => time()]));
        json_response(['token' => $token]);
    } else {
        json_response(['error' => 'Invalid credentials'], 401);
    }
}

function create_product() {
    $db = get_db_connection();
    $input = json_decode(file_get_contents('php://input'), true);
    $stmt = $db->prepare('INSERT INTO products (name, quantity) VALUES (?, ?)');
    $stmt->execute([$input['name'], $input['quantity']]);
    json_response(['id' => $db->lastInsertId()]);
}

function list_products() {
    $db = get_db_connection();
    $stmt = $db->query('SELECT * FROM products');
    json_response($stmt->fetchAll());
}

