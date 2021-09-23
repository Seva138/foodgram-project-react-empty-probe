http --pretty all --ignore-stdin --raw '{"current_password": "14436vdg", "new_password": "password"}' \
    localhost:8000/api/users/set_password/ "Authorization: Token $JWT_TOKEN"
