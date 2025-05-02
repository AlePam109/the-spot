# The Spot - Business Review Platform

A Yelp-like web application that allows users to discover, review, and manage businesses. Built with Flask and PostgreSQL.

## Features

- User Authentication
  - Business account creation and login
  - Customer account creation and login
- Business Management
  - Create and edit business profiles
  - View business details
  - Manage business information
- Search and Discovery
  - Search for businesses
  - View business details
  - Browse reviews and tips
- Review System
  - Post reviews for businesses
  - React to reviews
  - Post tips
  - Praise tips

## Project Structure

```
the-spot/
├── app.py              # Main application file
├── database/          # Database related files
├── static/            # Static assets (CSS, JS, images)
├── templates/         # HTML templates
│   ├── login/        # Login and account creation pages
│   └── manage/       # Business management pages
└── utils/            # Utility functions and helpers
```

## Setup and Installation

1. Ensure you have Python and PostgreSQL installed
2. Set up the database:
   - Create a database named "yelpDB"
   - Update the database connection settings in `app.py`
3. Install dependencies:
   ```bash
   pip install flask psycopg2
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Configuration

Before running the application, make sure to:
1. Update the `USERNAME` variable in `app.py` with your PostgreSQL username
2. Configure the database connection settings if needed:
   - Database name: "yelpDB"
   - Host: "/tmp"
   - Port: 8888

## API Endpoints

### Authentication
- `/api/login/business` - Business login
- `/api/login/customer` - Customer login
- `/api/login/create-business` - Create business account
- `/api/login/create-customer` - Create customer account

### Business Management
- `/api/businesses` - Get user's businesses
- `/api/business` - Get business details
- `/api/business/update` - Update business information
- `/api/business/create` - Create new business

### Reviews and Tips
- `/api/business/review` - Post a review
- `/api/business/tip` - Post a tip
- `/api/business/tip-praise` - Praise a tip
- `/api/business/review-reaction` - React to a review

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License.
