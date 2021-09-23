http --pretty all --ignore-stdin GET localhost:8000/api/recipes/download_shopping_cart/ \
    "Authorization: Token $JWT_TOKEN"
