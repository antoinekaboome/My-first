FROM php:8-fpm

# Include Composer for installing CodeIgniter
COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY . /var/www/html
RUN docker-php-ext-install pdo_mysql \
    && composer install --no-dev --optimize-autoloader || true

CMD ["php", "-S", "0.0.0.0:80", "-t", "public"]

