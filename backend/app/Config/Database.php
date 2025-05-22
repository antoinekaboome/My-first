<?php
return [
    'default' => [
        'DSN'      => '',
        'hostname' => getenv('DB_HOST') ?: 'db',
        'username' => getenv('DB_USER') ?: 'root',
        'password' => getenv('DB_PASS') ?: 'secret',
        'database' => getenv('DB_NAME') ?: 'stockapp',
        'DBDriver' => 'MySQLi',
        'charset'  => 'utf8mb4',
        'DBPrefix' => '',
    ],
];
