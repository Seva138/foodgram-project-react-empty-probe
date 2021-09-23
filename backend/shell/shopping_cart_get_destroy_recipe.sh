http --pretty all --ignore-stdin DELETE localhost:8000/api/recipes/9/shopping_cart/ \
    "Authorization: Token $JWT_TOKEN"
