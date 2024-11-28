from fastapi import FastAPI
from app.database import engine, Base, get_db
from app.routes import (auth, user, post, message, pictures, transaction,
                        watchlist_post, watchlist_user)
from app.models.parent_category import ParentCat
from app.models.sub_category import SubCat
from app.core.settings import OPENAPI_SCHEMA

app = FastAPI(openapi_schema=OPENAPI_SCHEMA,
              docs_url="/")


def init_db():
    """
    Initialize the database with predefined categories if not already populated.
    """
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    category_mapping = {
        "Car, Bike & Boat": [
            "Cars", "Auto Parts & Tires", "Boats & Boat Accessories", "Bicycles & Accessories",
            "Motorcycles & Scooters", "Motorcycle Parts & Accessories",
            "Commercial Vehicles & Trailers", "Repairs & Services", "Caravans & Mobile Homes",
            "Other Car, Bike & Boat"
        ],
        "Electronics": [
            "Audio & Hi-Fi", "Electronics Services", "Photo", "Mobile & Telephone",
            "Household Appliances", "Consoles", "Laptops", "PCs", "PC Accessories & Software",
            "Tablets & Readers", "TV & Video", "Video Games", "Other Electronics"
        ],
        "Home & Garden": [
            "Bathrooms", "Office", "Decoration", "Home & Garden Services",
            "Garden Accessories & Plants", "Home Textiles", "DIY", "Kitchen & Dining Room",
            "Lamps & Lights", "Bedrooms", "Living Room", "Other Home & Garden"
        ],
        "Jobs": [
            "Training", "Construction, Crafts & Production", "Office Work & Administration",
            "Gastronomy & Tourism", "Customer Service & Call Center", "Mini & Part-Time Jobs",
            "Internships", "Social Sector & Care", "Transport, Logistics & Traffic",
            "Sales, Purchasing & Sales", "More Jobs"
        ],
        "Neighbourhood Help": [
            "Neighbourhood Help"
        ],
        "Services": [
            "Elder Care", "Car, Bike & Boat", "Babysitter & Nanny", "Musician & Artist",
            "Travel & Event", "Animal Care & Training", "Transport & Moving", "Other Services"
        ],
        "Family, Child & Baby": [
            "Elderly Care", "Baby & Children's Clothing", "Baby & Children's Shoes", "Toys",
            "Baby Equipment", "Baby Carriers & Child Seats", "Babysitter & Child Care",
            "Strollers & Buggies", "Children's Room Furniture", "Other Family, Child & Baby"
        ],
        "Pets": [
            "Fish", "Dogs", "Cats", "Small Animals", "Livestock", "Horses",
            "Animal Training & Care", "Missing Animals", "Birds", "Accessories"
        ],
        "Fashion & Beauty": [
            "Beauty & Health", "Women's Clothing", "Women's Shoes", "Men's Clothing",
            "Men's Shoes", "Bags & Accessories", "Watches & Jewelry", "Other Fashion & Beauty"
        ],
        "Lessons & Courses": [
            "Health & Beauty", "Computer Courses", "Esoteric & Spiritual", "Cooking & Baking",
            "Art & Design", "Music & Singing", "Tutoring", "Sports Courses",
            "Language Courses", "Dance Courses", "Further Education", "Other Lessons & Courses"
        ],
        "Admission tickets & tickets": [
            "Rail & Public Transport", "Comedy & Cabaret", "Vouchers", "Children",
            "Concerts", "Sports", "Theatre & Musicals", "More Tickets"
        ],
        "Leisure, hobbies & neighbourhood": [
            "Esotericism & Spirituality", "Food & Drink", "Leisure Activities",
            "Handicrafts, Crafts & Arts and Crafts", "Art & Antiques",
            "Artist & Musician", "Model Making", "Travel & Event Services",
            "Collect", "Sports & Camping", "Junk", "Lost & Found",
            "Other Leisure, Hobby & Neighborhood"
        ],
        "Real Estate": [
            "Temporary & Shared Accommodation", "Condominiums", "Holiday & Foreign Properties",
            "Garages & Parking Spaces", "Commercial Real Estate", "Land & Gardens",
            "Houses for Sale", "Houses for Rent", "Rental Apartments", "Moving & Transport",
            "Other Properties"
        ],
        "Music, Movies & Books": [
            "Books & Magazines", "Office & Stationery", "Comics",
            "Technical Books, School & Study", "Movies & DVDs",
            "Music & CDs", "Musical Instruments", "More Music, Movies & Books"
        ],
        "Give away & Swap": [
            "Exchange", "Lending", "Give Away"
        ],
        "Undefined": ["Undefined"]
    }
    if not db.query(ParentCat).first():
        for parent_cat, sub_cats in category_mapping.items():
            db_parent_cat = ParentCat(title=parent_cat)
            db.add(db_parent_cat)
            db.commit()
            for sub_cat in sub_cats:
                db.add(SubCat(title=sub_cat, parent_id=db_parent_cat.id))
        db.commit()
    db.close()


init_db()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(message.router)
app.include_router(pictures.router)
app.include_router(transaction.router)
app.include_router(watchlist_post.router)
app.include_router(watchlist_user.router)
