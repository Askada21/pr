# Contains SQL commands for creating tables and relationships

-- 1. Dimension Tables

-- Products
create table products (
    product_id varchar(10) primary key
);

-- Stores
create table stores (
    store_id varchar(10) primary key
);

-- Categories
create table categories (
    category_id integer primary key,
    category_name varchar(50) not null unique
);

-- Regions
create table regions (
    region_id integer primary key,
    region_name varchar(50) not null unique
);

-- 2. Fact Table

create table daily_inventory (
    date date not null,
    product_id varchar(10) not null,
    store_id varchar(10) not null,

    inventory_level integer not null
        check (inventory_level >= 0),

    units_sold integer not null
        check (units_sold >= 0),

    units_ordered integer not null
        check (units_ordered >= 0),

    demand_forecast numeric not null,

    price numeric not null
        check (price >= 0),

    discount integer not null
        check (discount between 0 and 100),

    weather_condition varchar(50) not null,
    holiday_promotion boolean not null,

    competitor_pricing numeric not null
        check (competitor_pricing >= 0),

    seasonality varchar(50) not null,
    category_id integer not null,
    region_id integer not null,

    primary key (date, product_id, store_id),

    foreign key (product_id) references products(product_id),
    foreign key (store_id) references stores(store_id),
    foreign key (category_id) references categories(category_id),
    foreign key (region_id) references regions(region_id)
);