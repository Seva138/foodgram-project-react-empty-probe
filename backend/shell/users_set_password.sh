http --pretty all --ignore-stdin --raw '{"current_password": "password", "new_password": "14436vdg"}' \
    localhost:8000/api/users/set_password/ "Authorization: Token $JWT_TOKEN"
