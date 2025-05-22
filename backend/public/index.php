<?php
// Path to the front controller
define('FCPATH', __DIR__ . DIRECTORY_SEPARATOR);

// Ensure the current directory is pointing to the front controller's directory
chdir(__DIR__);

// Load Composer autoload if available
if (file_exists(__DIR__ . '/../vendor/autoload.php')) {
    require __DIR__ . '/../vendor/autoload.php';
}

// Bootstrap the CodeIgniter framework
$pathsPath = realpath(FCPATH . '../app/Config/Paths.php');
if ($pathsPath === false) {
    header('HTTP/1.1 503 Service Unavailable.', true, 503);
    echo 'Paths configuration not found.';
    exit(1);
}

require $pathsPath;
$paths = new Config\Paths();

require rtrim($paths->systemDirectory, '/\\') . '/bootstrap.php';

$app = Config\Services::codeigniter();
$app->run();
