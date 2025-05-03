from flask import Flask, render_template, request, jsonify
import psycopg2
from psycopg2.extras import Json
import os

app = Flask(__name__)

USERNAME = "alepam" #ENTER whoami VALUE HERE

# === Database Connection ===
def get_db_connection():
    return psycopg2.connect(
        dbname="yelpDB",
        user=USERNAME,
        host="/tmp",
        port=8888,
    )


# === Page Routes (for loading HTML) ===
@app.route("/")
def page_login():
    return render_template("login/login.html")

@app.route("/create-account")
def page_create_account():
    return render_template("login/create_account.html")

@app.route("/manage")
def page_manage_businesses():
    return render_template("manage/view_businesses.html")

@app.route("/manage/details")
def page_business_detail():
    return render_template("manage/business_detail.html")

@app.route("/manage/edit")
def page_edit_business():
    return render_template("manage/edit_business.html")

@app.route("/manage/create")
def page_create_business():
    return render_template("manage/create_business.html")

@app.route("/search")
def page_search():
    return render_template("review/search.html")

@app.route("/search/details")
def page_search_details():
    return render_template("review/business_view.html")

@app.route("/account")
def page_account():
    return render_template("review/account_view.html")


# === API Routes ===

# ===== LOGIN =====
@app.route("/api/login/business", methods=["POST"])
def api_login_business():
    from utils.hash_password import hash_password
    data = request.get_json()

    required_fields = ["username", "password"]
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")

    username = data["username"]
    password = hash_password(data["password"])

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # First check if the account exists in business_account table
        with open("database/login/check_business_user_exists.sql", "r") as f:
            check_sql = f.read()
        cur.execute(check_sql, (username,))
        exists = cur.fetchone()
        
        if not exists:
            cur.close()
            conn.close()
            return jsonify(success=False, error="Invalid username or password")

        # Then verify the password
        with open("database/login/login_business.sql", "r") as f:
            sql = f.read()
        cur.execute(sql, (username, password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify(success=True, account_id=result[0], username=username, account_type="business")
        else:
            return jsonify(success=False, error="Invalid username or password")

    except Exception as e:
        print("Business login error:", e)
        return jsonify(success=False, error="Internal server error")


@app.route("/api/login/customer", methods=["POST"])
def api_login_customer():
    from utils.hash_password import hash_password
    data = request.get_json()

    required_fields = ["username", "password"]
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")

    username = data["username"]
    password = hash_password(data["password"])

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # First check if the account exists in user_account table
        with open("database/login/check_user_exists.sql", "r") as f:
            check_sql = f.read()
        cur.execute(check_sql, (username,))
        exists = cur.fetchone()
        
        if not exists:
            cur.close()
            conn.close()
            return jsonify(success=False, error="Invalid username or password")

        # Then verify the password
        with open("database/login/login_user.sql", "r") as f:
            sql = f.read()
        cur.execute(sql, (username, password))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify(success=True, user_id=result[0], username=username, account_type="customer")
        else:
            return jsonify(success=False, error="Invalid username or password")

    except Exception as e:
        print("User login error:", e)
        return jsonify(success=False, error="Internal server error")


@app.route("/api/login/create-business", methods=["POST"])
def api_create_business_account():
    from utils.hash_password import hash_password
    data = request.get_json()

    required_fields = ["username", "password", "name"]
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")

    username = data["username"]
    password = hash_password(data["password"])
    name = data["name"]

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/login/check_business_user_exists.sql", "r") as f:
            check_sql = f.read()
        cur.execute(check_sql, (username,))
        exists = cur.fetchone()
        if exists:
            cur.close()
            conn.close()
            return jsonify(success=False, error="Username already exists")

        with open("database/login/insert_business_user.sql", "r") as f:
            sql = f.read()
        cur.execute(sql, (name, username, password, username))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if result and len(result) > 0:
            return jsonify(success=True, account_id=result[0])
        else:
            return jsonify(success=False, error="Username already exists")

    except Exception as e:
        print("Create business error:", e)
        return jsonify(success=False, error="Internal server error")


@app.route("/api/login/create-customer", methods=["POST"])
def api_create_customer_account():
    from utils.hash_password import hash_password
    from utils.generate_user_id import generate_user_id
    data = request.get_json()

    required_fields = ["username", "password", "name"]
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")

    username = data["username"]
    password = hash_password(data["password"])
    name = data["name"]
    user_id = generate_user_id()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/login/check_user_exists.sql", "r") as f:
            check_sql = f.read()
        cur.execute(check_sql, (username,))
        exists = cur.fetchone()
        if exists:
            cur.close()
            conn.close()
            return jsonify(success=False, error="Username already exists")


        with open("database/login/insert_user.sql", "r") as f:
            insert_sql = f.read()
        cur.execute(insert_sql, (user_id, name, username, password, username))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        if result and len(result) > 0:
            return jsonify(success=True, user_id=result[0])
        else:
            return jsonify(success=False, error="Account creation failure")
        

    except Exception as e:
        print("Create user error:", e)
        return jsonify(success=False, error="Internal server error")


# ===== BUSINESS ACCOUNT =====
@app.route("/api/businesses", methods=["GET"])
def api_get_my_businesses():
    account_id = request.args.get("accountId")

    if not account_id:
        return jsonify(success=False, error="Missing account ID")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/business/get_my_businesses.sql", "r") as f:
            sql = f.read()

        cur.execute(sql, (account_id,))
        rows = cur.fetchall()

        businesses = []
        for row in rows:
            businesses.append({
                "business_id": row[0],
                "name": row[1],
                "address": row[2],
                "is_open": row[3],
                "stars": row[4]
            })

        cur.close()
        conn.close()

        return jsonify(success=True, businesses=businesses)

    except Exception as e:
        print("Error in get_my_businesses:", e)
        return jsonify(success=False, error="Internal server error")


@app.route("/api/business", methods=["GET"])
def api_get_business():
    account_id = request.args.get("accountId")
    business_id = request.args.get("businessId")

    if not account_id or not business_id:
        return jsonify(success=False, error="Missing parameters")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/business/get_business_by_id.sql", "r") as f:
            sql = f.read()

        cur.execute(sql, (business_id, account_id))
        row = cur.fetchone()

        if not row:
            return jsonify(success=False, error="Business not found")

        colnames = [desc[0] for desc in cur.description]
        details = dict(zip(colnames, row))

        cur.close()
        conn.close()

        return jsonify(success=True, details=details)

    except Exception as e:
        print("Error in get_business:", e)
        return jsonify(success=False, error="Internal server error")



@app.route("/api/business/update", methods=["POST"])
def api_update_business():
    data = request.get_json()
    required_fields = [
        "business_id", "account_id", "name", "address", "city", "state",
        "postal_code", "latitude", "longitude", "stars", "review_count",
        "is_open", "attributes", "categories", "hours"
    ]

    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing fields")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/business/update_business.sql", "r") as f:
            sql = f.read()

        cur.execute(sql, (
            data["name"], data["address"], data["city"], data["state"],
            data["postal_code"], data["latitude"], data["longitude"],
            data["stars"], data["review_count"], data["is_open"],
            Json(data["attributes"]), data["categories"], Json(data["hours"]),
            data["business_id"], data["account_id"]
        ))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(success=True)

    except Exception as e:
        print("Error in update_business:", e)
        return jsonify(success=False, error="Internal server error")


@app.route("/api/business/create", methods=["POST"])
def api_create_business():
    from utils.generate_user_id import generate_user_id as gen_biz_id  # reuse for business_id

    data = request.get_json()
    required_fields = [
        "account_id", "name", "address", "city", "state", "postal_code",
        "latitude", "longitude", "is_open",
        "attributes", "categories", "hours"
    ]

    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing fields")

    business_id = gen_biz_id()

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/business/create_business.sql", "r") as f:
            insert_sql = f.read()

        cur.execute(insert_sql, (
            business_id, data["name"], data["address"], data["city"], data["state"],
            data["postal_code"], data["latitude"], data["longitude"],
            data["is_open"],Json(data["attributes"]), data["categories"], 
            Json(data["hours"]), data["account_id"]
        ))

        with open("database/business/update_num_businesses.sql", "r") as f:
            update_sql = f.read()

        cur.execute(update_sql, (data["account_id"],))

        conn.commit()
        cur.close()
        conn.close()

        return jsonify(success=True, business_id=business_id)

    except Exception as e:
        print("Error in create_business:", e)
        return jsonify(success=False, error="Internal server error")


# ===== USER ACCOUNT =====
@app.route("/api/search", methods=["POST"])
def api_search_businesses():
    return jsonify({"results": []})

@app.route("/api/business/review", methods=["POST"])
def api_post_review():
    from utils.generate_user_id import generate_user_id
    data = request.get_json()
    required_fields = ["user_id", "business_id", "stars", "text"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    if not (1 <= data["stars"] <= 5):
        return jsonify(success=False, error="Stars must be between 1 and 5")
    
    review_id = generate_user_id()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/review/review_queries.sql", "r") as f:
            sql = f.read().split(';')[0]  # Get the first query (insert review)
        
        cur.execute(sql, (
            review_id, data["user_id"], data["business_id"],
            data["stars"], data["text"]
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(success=True, review_id=review_id)
        
    except Exception as e:
        print("Error in post_review:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/business/tip", methods=["POST"])
def api_post_tip():
    from utils.generate_user_id import generate_user_id
    data = request.get_json()
    required_fields = ["user_id", "business_id", "text"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    tip_id = generate_user_id()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/review/review_queries.sql", "r") as f:
            sql = f.read().split(';')[4]  # Get the insert tip query
        
        cur.execute(sql, (
            tip_id, data["user_id"], data["business_id"], data["text"]
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(success=True, tip_id=tip_id)
        
    except Exception as e:
        print("Error in post_tip:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/business/tip-praise", methods=["POST"])
def api_praise_tip():
    data = request.get_json()
    required_fields = ["user_id", "tip_id"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/review/review_queries.sql", "r") as f:
            sql = f.read().split(';')[6]  # Get the add praise query
        
        cur.execute(sql, (data["user_id"], data["tip_id"]))
        
        # Update compliment count
        update_sql = f.read().split(';')[7]  # Get the update compliment count query
        cur.execute(update_sql, (data["tip_id"], data["tip_id"]))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(success=True)
        
    except Exception as e:
        print("Error in praise_tip:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/business/review-reaction", methods=["POST"])
def api_review_reaction():
    data = request.get_json()
    required_fields = ["user_id", "review_id", "reaction_type"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    if data["reaction_type"] not in ["useful", "funny", "cool"]:
        return jsonify(success=False, error="Invalid reaction type")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/review/review_queries.sql", "r") as f:
            sql = f.read().split(';')[2]  # Get the add reaction query
        
        cur.execute(sql, (
            data["user_id"], data["review_id"], data["reaction_type"]
        ))
        
        # Update reaction counts
        update_sql = f.read().split(';')[3]  # Get the update reaction counts query
        cur.execute(update_sql, (
            data["review_id"], data["review_id"], data["review_id"], data["review_id"]
        ))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify(success=True)
        
    except Exception as e:
        print("Error in review_reaction:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/account", methods=["GET"])
def api_get_account():
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify(success=False, error="Missing user ID")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        with open("database/account/account_queries.sql", "r") as f:
            sql = f.read()
        cur.execute(sql, (user_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return jsonify(success=True, 
                         user_id=result[0],
                         username=result[1],
                         name=result[2],
                         yelping_since=result[3].strftime("%Y-%m-%d"))
        else:
            return jsonify(success=False, error="User not found")

    except Exception as e:
        print("Get account error:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/account/update", methods=["POST"])
def api_update_account():
    data = request.get_json()
    required_fields = ["user_id", "name", "email"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/account/account_queries.sql", "r") as f:
            sql = f.read().split(';')[1]  # Get the update profile query
        
        cur.execute(sql, (data["name"], data["email"], data["user_id"]))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="User not found")
            
    except Exception as e:
        print("Error in update_account:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/account/password", methods=["POST"])
def api_change_password():
    from utils.hash_password import hash_password
    data = request.get_json()
    required_fields = ["user_id", "current_password", "new_password"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/account/account_queries.sql", "r") as f:
            sql = f.read().split(';')[2]  # Get the change password query
        
        cur.execute(sql, (
            hash_password(data["new_password"]),
            data["user_id"],
            hash_password(data["current_password"])
        ))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="Invalid current password")
            
    except Exception as e:
        print("Error in change_password:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/account/delete", methods=["POST"])
def api_delete_account():
    data = request.get_json()
    required_fields = ["user_id"]
    
    if not all(field in data for field in required_fields):
        return jsonify(success=False, error="Missing required fields")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/account/account_queries.sql", "r") as f:
            sql = f.read().split(';')[3]  # Get the delete account query
        
        cur.execute(sql, (data["user_id"],))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if result:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error="User not found")
            
    except Exception as e:
        print("Error in delete_account:", e)
        return jsonify(success=False, error="Internal server error")

@app.route("/api/account/activity", methods=["GET"])
def api_get_activity():
    user_id = request.args.get("userId")
    
    if not user_id:
        return jsonify(success=False, error="Missing user ID")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        with open("database/account/account_queries.sql", "r") as f:
            queries = f.read().split(';')
            reviews_sql = queries[4]  # Get user reviews query
            tips_sql = queries[5]     # Get user tips query
        
        # Get reviews
        cur.execute(reviews_sql, (user_id,))
        reviews = []
        for row in cur.fetchall():
            colnames = [desc[0] for desc in cur.description]
            reviews.append(dict(zip(colnames, row)))
        
        # Get tips
        cur.execute(tips_sql, (user_id,))
        tips = []
        for row in cur.fetchall():
            colnames = [desc[0] for desc in cur.description]
            tips.append(dict(zip(colnames, row)))
        
        cur.close()
        conn.close()
        
        return jsonify(success=True, reviews=reviews, tips=tips)
            
    except Exception as e:
        print("Error in get_activity:", e)
        return jsonify(success=False, error="Internal server error")


# === Run the app ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
