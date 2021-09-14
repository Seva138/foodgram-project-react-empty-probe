http --pretty all -j POST localhost:8000/api/users/ "Authorization: Token $JWT_TOKEN" \
< jsondata/users_post.json
