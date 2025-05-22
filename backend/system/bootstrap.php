<?php
use CodeIgniter\CodeIgniter;
use CodeIgniter\Config\Services;

require_once __DIR__ . '/../vendor/autoload.php';

// Basic bootstrap for a minimal CodeIgniter-like setup
function app(): CodeIgniter
{
    return Services::codeigniter();
}
