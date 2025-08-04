# Requirements
Develop REST API server using **django-rest-framework** with pagination, sorting and filtering for two models:

## DB Models:
- **Wallet**
	- `id`
	- `label` *(is a string field)*
	- `balance` *(a summary of all transactions's amounts; balance should NEVER be negative)*

- **Transaction**
	- `id`
	- `wallet_id` *(fk)*
	- `txid` *(required unique string field)*
	- `amount` *(number with 18-digits precision; amount may be negative)*


> Where **txid** is required unique string field, **amount** is a number with 18-digits precision, **label** is a string field, **balance** is a summary of all transactions's amounts. Transaction amount may be negative. Wallet balance should NEVER be negative

## Tech Stack:
- **Python**: `3.11+`
- **Database**: `MySQL` or `Postgres`
- **Frameworks**: `django-rest-framework`
- **API specification:** [JSON:API](https://jsonapi.org/format/) *(you are free to use [this](https://django-rest-framework-json-api.readthedocs.io/en/stable/) library)*

## Will Be Your Advantage:
- [ ] Test coverage
- [ ] Any linter usage
- [ ] Quick start app guide if you create your own docker-compose or Dockerfiles
- [ ] Comments in non-standart places in code
- [ ] Use database indexes if you think it's advisable
