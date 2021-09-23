http --pretty all -j POST localhost:8000/api/recipes/ "Authorization: Token $JWT_TOKEN" \
< jsondata/recipes_post.json
