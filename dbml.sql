// Use DBML to define your database structure
// Docs: https://dbml.dbdiagram.io/docs


Table users {
  id uuid [primary key, not null]
  external_id int [primary key, not null, note: "user identificator from firebase auth"]
  username text
  email text [not null]
  first_name text [not null]
  second_name text
  surname text [not null]
  second_surname text
  phone text [not null]
  second_phone text
  role text [not null, note: "De momento el usuario principal de una company sera creado con el rol de Owner"]
  other_role text [note: "Si se selecciona otro tipo de Rol aqui se guardará el string correspondiente"]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz

  Note: "Registro de usuarios con external ID para validar con firebase API"

}

Table company {
  id uuid [primary key, not null]
  external_id int [primary key, not null, note: "company identificator from master de clientes monthly"]
  website text
  description text
  logo_path text
  commercial_name text [not null]
  linkedin_url text [note: "Este seria de tipo optional"]
  employees_lenght int
  monthly_countries_id uuid [not null]
  annual_income numeric
  status text [note: 'Para manejar si la compañía ya finalizó su proceso de Onboarding']
  company_size text [note: "Opciones disponibles 'Xs S M L XL o XXL' se genera durante la crecion de company mediante el microservicio"]
  origin_country_id uuid
  fiscal_identifier text [not null]
  identifier_type text [note: "Las opciones serian [CSF(For MX), W9(For USA) o Manual(For LATAM)]"]
  legal_name text [not null]
  industry_id uuid
  sub_industry_id uuid
  invoices_email text
  has_business_units bool
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
  sizes_catalog_id uuid

  Note: "Registro de companies"

}

Table sizes_catalog {
  id uuid [primary key, not null]
  name text // XS, S, M, L, XL, XXL
  income_size float
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz

  Note: "Registro de catalogo de tamaños de empresa"
}

Table suppliers {
  id uuid [primary key, not null]
  name text
  fiscal_identifier text
  need_clean bool [default: false]
  clean_type json [note: "none, dispersed_amount..."]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table clean_types {
  id uuid [primary key, not null]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}


Table company_address {
  id uuid [primary key, not null]
  company_id uuid [ref: > company.id] // Relación con la tabla company
  is_main bool
  countries_id uuid [note: "Pais que se selecciona en si es MX, USA o LATAM va vinculado al catalogo countries"]
  country text [note: "Pais - Se puede extraer de la seleccion del pais a nivel catalogo (Solo informativo)"]
  zip_code int [note: "Código postal", not null]
  state text [note: "Estado", not null]
  city text [note: "Ciudad", not null]
  municipality text [note: "Municipio"]
  suburb text [note: "Colonia"]
  street text [note: "Del extrator CSF se extraen y concatenan los parametro 'Entre calle y calle' para complementar info 'SOLO aplica en MX'", not null]
  external_number text [not null]
  internal_number text
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz

  Note: "Direcciones de companies"

}


Table industry {
  id uuid [primary key]
  name text
  code int [not null]
  description text
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table sub_industry {
  id uuid [primary key]
  name text
  code int [not null]
  description text
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}


Table countries {
  id uuid [primary key]
  name text [note: "Select (México, Argentina, Panamá, Peru, Chile, Colombia, Estados Unidos)"]
  code_iso_alpha_2 int [not null]
  code_iso_alpha_3 int [not null]
  phone_code text
  monthly_use bool [note: "Identifica si en ese país opera o puede operar Monthly"]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}


Table business_units {
  id uuid [primary key, not null]
  name text [not null]
  company_id uuid [not null]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table user_company {
  user_id uuid [ref: > users.id]
  company_id uuid [ref: > company.id]
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
  primary key (user_id, company_id)
}

Table providers_properties {
  id uuid [primary key]
  name text
  metadata_ json [note: 'Este podria ser encriptado para no tener acceso directo desde la BD.']
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table providers_tokens {
  id uuid [primary key]
  company_id uuid
  tokens json [note: 'Este seria para almacenar los tokens por cliente(company) encriptados.']
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table trial_balances_raw_format {
  id uuid [primary key]
  company_id uuid
  period_month text
  period_year text
  source_file_name text
  upload_date timestampz
  provider_id uuid
  account_number text
  account_name text
  initial_debit_balance numeric
  initial_credit_balance numeric
  debit_movements numeric
  credit_movements numeric
  current_debit_balance numeric
  current_credit_balance numeric
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table trial_balances_monthly_format {
  id uuid [primary key]
  company_id uuid
  period_month text
  period_year text
  source_file_name text
  upload_date timestampz
  provider_id uuid
  account_number text
  account_name text
  initial_debit_balance numeric
  initial_credit_balance numeric
  debit_movements numeric
  credit_movements numeric
  current_debit_balance numeric
  current_credit_balance numeric
  is_active bool [default: true]
  is_deleted bool [default: false]
  created_at timestampz
  updated_at timestampz
  deleted_at timestampz
}

Table company_payment_suscription {
  id uuid [primary key, default: `uuid_generate_v4()`]
  email varchar [not null]
  first_name varchar [not null]
  second_name varchar
  phone varchar [not null]
  aux_phone varchar
  init_date timestamp [not null]
  end_date timestamp [not null]
  is_trial boolean // Nos indica si la suscription es del periodo de prueba
  suscription_upgrade boolean // Nos indica si el cliente ya pago durante su periodo de prueba
  suscription_type_id uuid [ref: > suscriptions_type.id]
  external_id varchar // Referencia al metodo de pago registrado en Quentli
  company_id uuid [ref: > company.id]
  is_active boolean [default: true]
  is_deleted boolean [default: false]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp

  Note: 'Suscripciones de pago de las empresas'
}


Table suscriptions_type {
  id uuid [primary key, default: `uuid_generate_v4()`]
  name text [note: "small, medium, large"]
  is_active boolean [default: true]
  is_deleted boolean [default: false]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp

  Note: 'Tipos de suscripciones disponibles'
}

Table company_cards {
  id uuid [primary key, default: `uuid_generate_v4()`]
  company_id uuid [ref: > company_payment_suscription.id]
  external_id varchar // Referencia al metodo de pago registrado en Quentli
  is_active boolean [default: true]
  is_deleted boolean [default: false]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  deleted_at timestamp

  Note: 'Tarjetas de pago de las empresas'
}

Table user_payment_info {
  id uuid [primary key, default: `uuid_generate_v4()`]
  external_id text [ref: > users.external_id]
  is_stripe boolean [default: false]
  is_quentli boolean [default: false] 
  customer_id text [unique]
  company_size text

  Note: 'Información de pago de usuarios'
}

Table products {
  id uuid [primary key, default: `uuid_generate_v4()`]
  product_id text [not null, unique]
  name text [not null]
  description text
  created_at timestamp
  updated_at timestamp
  is_stripe boolean [default: false]
  is_quentli boolean [default: false]
  size text

  Note: 'Catálogo de productos disponibles'
}


Table product_price {
  id uuid [primary key, default: `uuid_generate_v4()`]
  price_id text
  product_id text [ref: > products.product_id, not null]
  is_active boolean [default: true]
  unit_amount integer
  currency text
  interval text
  trial_period_days integer
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Precios de los productos'
}

Table user_products {
  id uuid [primary key, default: `uuid_generate_v4()`]
  external_id text [ref: > users.external_id]
  product_id text [ref: > products.product_id]
  // Agregar más campos según necesidad

  Note: 'Relación entre usuarios y productos'
}

Table payment_methods {
  id uuid [primary key, default: `uuid_generate_v4()`]
  payment_method_id text [not null, unique]
  external_id text [ref: > users.external_id, not null]
  billing_name text
  exp_month text
  exp_year text
  funding text
  last4 text
  brand text
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Métodos de pago de los usuarios'
}

Table subscriptions {
  id uuid [primary key, default: `uuid_generate_v4()`]
  external_id text [ref: > users.external_id, not null]
  subscription_id text [not null, unique]
  product_id text [ref: > products.product_id, not null]
  price_id text [ref: > product_price.price_id, not null]
  payment_method_id text [ref: > payment_methods.payment_method_id]
  is_quentli boolean [default: false]
  is_stripe boolean [default: false]
  is_active boolean [default: false]
  is_trial boolean [default: false]
  is_paused boolean [default: false]
  is_canceled boolean [default: false]
  period_end timestamp
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Suscripciones de usuarios'
}

Table subscription_invoice {
  id uuid [primary key, default: `uuid_generate_v4()`]
  external_id text [ref: > users.external_id, not null]
  invoice_id text [not null, unique]
  subscription_id text [ref: > subscriptions.subscription_id, not null]
  payment_method_id text [ref: > payment_methods.payment_method_id]
  amount_paid integer [not null]
  currency text [not null]
  is_paid boolean [default: false]
  attempt_count text [not null]
  period_end timestamp
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Facturas de suscripciones'
}

Table checkout_sessions {
  id uuid [primary key, default: `uuid_generate_v4()`]
  session_id text [not null, unique]
  order_id text [note: 'ancla lógica']
  subscription_id text [ref: > subscriptions.subscription_id]
  customer_id text
  external_id text
  url text
  mode text
  status text
  payment_status text
  amount_total integer
  currency text
  success_url text
  cancel_url text
  checkout_metadata json
  expires_at timestamp
  is_expired boolean [default: false]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Sesiones de checkout para pagos'
}

Table pending_actions {
  id uuid [primary key, default: `uuid_generate_v4()`]
  external_id text [ref: > users.external_id, not null]
  action_type text [not null]
  status text
  is_closed boolean [default: false]
  meta json
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]

  Note: 'Acciones pendientes del sistema'
}

Table users_access_log {
  id uuid [primary key, default: `uuid_generate_v4()`]
  user_id uuid [ref: > users.id]
  created_at timestamp [default: `now()`]
  updated_at timestamp [default: `now()`]
  latitude text
  longitude text
  accuracy text
  altitude_accuracy text
  heading text
  speed text
  is_deleted boolean [default: false]
  deleted_at timestamp

  Note: 'Registro de accesos de usuarios'
}

Ref: "company"."id" < "providers_tokens"."id"

Ref: "trial_balances_raw_format"."company_id" < "company"."id"

Ref: "company"."industry_id" < "industry"."id"

Ref: "company_cards"."company_id" < "company"."id"

Ref: "countries"."id" < "company"."origin_country_id"