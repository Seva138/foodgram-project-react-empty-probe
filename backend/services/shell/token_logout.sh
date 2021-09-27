http --pretty all --ignore-stdin -f POST localhost:8000/api/auth/token/logout/ "Authorization: Token $JWT_TOKEN"
