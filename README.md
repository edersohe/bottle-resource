## Bottle Resource

### Resource Handler based on actions

| url                 | method | action  |
|:--------------------|:-------|:--------|
| {prefix}            | GET    | index   |
| {prefix}/:pk        | GET    | show    |
| {prefix}/:pk/edit   | GET    | edit    |
| {prefix}/new        | GET    | new     |
| {prefix}            | POST   | create  |
| {prefix}/:pk        | PUT    | update  |
| {prefix}/:pk        | PATCH  | patch   |
| {prefix}/:pk        | DELETE | destroy |

> {prefix} should be "/animal", "/person", "/job" or any prefix that describe your resource route

> pk means primary key

### Example

after install bottle-resource

`pip install -U git+git://github.com/edersohe/bottle-resource.git`

into examples directory

`python rest_class.py`

try the follow routes in the browser and something like postman with header `Accept: application/json`

* http://localhost:8080/with_class
* http://localhost:8080/with_class/other_route
* http://localhost:8080/with_class/01

Or

`python rest_class.py`

try the follow routes in the browser and something like postman with header `Accept: application/json`

* http://localhost:8080/with_class
* http://localhost:8080/with_class/other_route
* http://localhost:8080/with_class/01

Or

`python mix.py`

and try all routes mention before with and without header `Accept: application/json`

### TODO

* test
* continuous integration
* improve documentation
* improve examples
