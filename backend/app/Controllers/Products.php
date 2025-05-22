<?php
namespace App\Controllers;

use CodeIgniter\RESTful\ResourceController;

class Products extends ResourceController
{
    protected $format = 'json';

    public function index()
    {
        // TODO: retrieve products from database
        $products = [
            ['id' => 1, 'name' => 'Sample', 'quantity' => 10]
        ];
        return $this->respond($products);
    }

    public function create()
    {
        $data = $this->request->getJSON(true);
        // TODO: save $data to database
        return $this->respondCreated(['id' => 1]);
    }
}
