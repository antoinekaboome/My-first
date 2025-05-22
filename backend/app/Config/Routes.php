<?php
$routes->post('api/login', 'Auth::login');
$routes->resource('api/products', ['controller' => 'Products']);
