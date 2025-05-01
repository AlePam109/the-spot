# Create folder structure
New-Item -ItemType Directory -Path static
New-Item -ItemType Directory -Path templates\login
New-Item -ItemType Directory -Path templates\manage
New-Item -ItemType Directory -Path templates\review
New-Item -ItemType Directory -Path database\login
New-Item -ItemType Directory -Path database\user
New-Item -ItemType Directory -Path database\business
New-Item -ItemType Directory -Path utils

# Create core files
New-Item app.py -ItemType File
New-Item utils\hash_password.py -ItemType File

# Static JS
@("app.js", "login.js", "user.js", "business.js") | ForEach-Object {
    New-Item -ItemType File -Path "static\$_"
}

# Login HTML
@("login.html", "create_account.html") | ForEach-Object {
    New-Item -ItemType File -Path "templates\login\$_"
}

# Manage HTML
@("view_businesses.html", "business_detail.html", "edit_business.html", "create_business.html") | ForEach-Object {
    New-Item -ItemType File -Path "templates\manage\$_"
}

# Review HTML
@("search.html", "business_view.html", "account_view.html") | ForEach-Object {
    New-Item -ItemType File -Path "templates\review\$_"
}

# Login SQL
@("create_user.sql", "create_business.sql", "login_user.sql", "login_business.sql") | ForEach-Object {
    New-Item -ItemType File -Path "database\login\$_"
}