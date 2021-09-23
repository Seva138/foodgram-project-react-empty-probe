http --pretty all -j PUT localhost:8000/api/recipes/8/ < jsondata/recipes_put.json "Authorization: Token $JWT_TOKEN"
