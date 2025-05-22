FROM php:8-fpm
WORKDIR /var/www/html
COPY . /var/www/html
RUN docker-php-ext-install pdo_mysql
CMD ["php", "-S", "0.0.0.0:80", "-t", "public"]

