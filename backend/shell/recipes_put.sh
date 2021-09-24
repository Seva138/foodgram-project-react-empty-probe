http --pretty all -j PUT localhost:8000/api/recipes/9/ < jsondata/recipes_put.json "Authorization: Token $JWT_TOKEN"
