http --pretty all --ignore-stdin DELETE localhost:8000/api/recipes/9/favorite/ \
    "Authorization: Token $JWT_TOKEN"
