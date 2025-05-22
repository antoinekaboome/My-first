<?php
return [
    'host' => getenv('DB_HOST') ?: 'db',
    'database' => getenv('DB_NAME') ?: 'stockapp',
    'user' => getenv('DB_USER') ?: 'root',
    'password' => getenv('DB_PASS') ?: 'secret',
];

