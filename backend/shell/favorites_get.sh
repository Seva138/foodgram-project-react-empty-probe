http --pretty all --ignore-stdin GET localhost:8000/api/recipes/9/favorite/ \
    "Authorization: Token $JWT_TOKEN"
