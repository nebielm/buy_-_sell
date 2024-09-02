# Buy and Sell

## Description
The "Buy and Sell" project is a web application built with FastAPI that allows users to create listings for items they want to sell and browse listings posted by others. The platform facilitates the buying and selling of various goods, offering a user-friendly interface for managing listings, contacting sellers, and processing transactions. Additionally, users can follow items and other users to receive updates and notifications.

## Live Demo

You can view the live version of the application at: [https://buy-and-sell-uyoh.onrender.com](https://buy-and-sell-uyoh.onrender.com)

## Installation

To run the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/nebielm/buy_-_sell.git
    cd buy_-_sell
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database** (if applicable):
    ```bash
    alembic upgrade head  # Run migrations if using Alembic for database migrations
    ```

5. **Start the application**:
    ```bash
    uvicorn app.main:app --reload
    ```

6. **Access the application**:
    - Open your web browser and go to `http://127.0.0.1:8000`.
    - To visit the FastAPI build-in documentation go to `http://127.0.0.1:8000/docs`

## Usage

### Creating a Listing
1. **Sign up** or **Log in** to your account.
2. Navigate to the "Create Listing" page.
3. Fill in the item details, upload images, and set a price.
4. Submit the form to post your listing.

### Browsing and Purchasing Items
1. Browse the listings on the homepage or use the search function to find specific items.
2. Click on an item to view details.
3. If interested, contact the seller or proceed to purchase directly through the platform.

### Following Items and Users
1. **Follow Items**:
   - While viewing an item, click the "Follow" button to receive notifications about updates to that item (e.g., price changes or new information).
   
2. **Follow Users**:
   - Visit a user's profile and click the "Follow" button to receive updates about their new listings and activities.

## Features

- User authentication (Sign up, Log in, Log out)
- Create, edit, and delete listings
- Browse and search for items
- Follow items to receive updates on changes
- Follow users to stay informed about their new listings and activities
- Contact sellers via messaging
- Secure payment processing
- Save, update, and delete profile pictures and post images using AWS S3 buckets.

## AWS S3 Integration

The application utilizes AWS S3 for managing image files:

- **Profile Pictures**: Users can upload, update, and delete their profile pictures. These images are stored in AWS S3 buckets for scalability and reliability.
- **Post Pictures**: Images associated with posts are also stored in AWS S3 buckets. This allows for efficient image management and retrieval.

## Project Directory Structure

Here is a high-level overview of the project directory structure:


    buy_and_sell/
    │
    ├── app/
    │   ├── core/              # Core functionality and settings
    │   │   ├── __init__.py 
    │   │   ├── security.py
    │   │   └── settings.py
    │   │
    │   ├── crud/              # CRUD functions
    │   │   ├── __init__.py
    │   │   ├── message.py
    │   │   ├── parent_category.py
    │   │   ├── pictures.py
    │   │   ├── post.py
    │   │   ├── sub_category.py
    │   │   ├── transaction.py
    │   │   ├── user.py
    │   │   ├── watchlist_post.py
    │   │   └── watchlist_user.py
    │   │ 
    │   ├── default_pictures/  # Default Pictures
    │   │   ├── default_post_pic.jpg
    │   │   └── default_profile_pic.jpg
    │   │ 
    │   ├── models/            # Database models
    │   │   ├── __init__.py
    │   │   ├── message.py
    │   │   ├── parent_category.py
    │   │   ├── pictures.py
    │   │   ├── post.py
    │   │   ├── sub_category.py
    │   │   ├── transaction.py
    │   │   ├── user.py
    │   │   ├── watchlist_post.py
    │   │   └── watchlist_user.py 
    │   │    
    │   ├── routes/           # Route definitions for API endpoints
    │   │   ├── __init__.py
    │   │   ├── auth.py
    │   │   ├── message.py
    │   │   ├── pictures.py
    │   │   ├── post.py
    │   │   ├── transaction.py
    │   │   ├── user.py
    │   │   ├── utils.py     # Utility functions for Picture Handeling with AWS used in pictures.py, users.py and post.py
    │   │   ├── watchlist_post.py
    │   │   └── watchlist_user.py
    │   │
    │   ├── schemas/           # Pydantic schemas for validation
    │   │   ├── __init__.py
    │   │   ├── message.py
    │   │   ├── parent_category.py
    │   │   ├── pictures.py
    │   │   ├── post.py
    │   │   ├── sub_category.py
    │   │   ├── transaction.py
    │   │   ├── user.py
    │   │   ├── watchlist_post.py
    │   │   └── watchlist_user.py
    │   │   
    │   ├── tests/           # Pydantic schemas for validation
    │   │   ├── __init__.py
    │   │   ├── test_message.py
    │   │   ├── test_parent_category.py
    │   │   ├── test_pictures.py
    │   │   ├── test_post.py
    │   │   ├── test_sub_category.py
    │   │   ├── test_transaction.py
    │   │   ├── test_user.py
    │   │   ├── test_watchlist_post.py
    │   │   └── test_watchlist_user.py
    │   │   
    │   ├── __init__.py  
    │   ├── database.py 
    │   └── main.py        
    │
    ├── requirements.txt       # Project dependencies
    ├── .env                   # Environment variables
    ├── .gitignore              # Git ignore file
    └── README.md              # Project overview


<!--## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact Information

For any inquiries or feedback, please contact:

- **Name:** Nebiel M
- **Email:** [nebielm@gmail.com](mailto:nebielmohammed@gmail.com)
- **GitHub:** [nebielm](https://github.com/nebielm) -->

## Acknowledgments

Special thanks to everyone who contributed to the development of this project.
