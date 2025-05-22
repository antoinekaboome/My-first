<?php
namespace App\Controllers;

use CodeIgniter\RESTful\ResourceController;

class Auth extends ResourceController
{
    protected $format = 'json';

    public function login()
    {
        $input = $this->request->getJSON(true);
        // TODO: integrate real authentication logic
        if ($input['username'] === 'admin' && $input['password'] === 'admin') {
            return $this->respond(['token' => base64_encode('dummy-token')]);
        }
        return $this->failUnauthorized('Invalid credentials');
    }
}
