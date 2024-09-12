from pydantic import BaseModel, model_validator, ConfigDict
from app.database import get_db
from app.crud.parent_category import get_parent_cat_by_title

db = get_db()


category_mapping = {
        get_parent_cat_by_title(db=db, title="Car, Bike & Boat").id: [
            "Cars", "Auto Parts & Tires", "Boats & Boat Accessories", "Bicycles & Accessories",
            "Motorcycles & Scooters", "Motorcycle Parts & Accessories",
            "Commercial Vehicles & Trailers", "Repairs & Services", "Caravans & Mobile Homes",
            "Other Car, Bike & Boat"
        ],
        get_parent_cat_by_title(db=db, title="Electronics").id: [
            "Audio & Hi-Fi", "Electronics Services", "Photo", "Mobile & Telephone",
            "Household Appliances", "Consoles", "Laptops", "PCs", "PC Accessories & Software",
            "Tablets & Readers", "TV & Video", "Video Games", "Other Electronics"
        ],
        get_parent_cat_by_title(db=db, title="Home & Garden").id: [
            "Bathrooms", "Office", "Decoration", "Home & Garden Services",
            "Garden Accessories & Plants", "Home Textiles", "DIY", "Kitchen & Dining Room",
            "Lamps & Lights", "Bedrooms", "Living Room", "Other Home & Garden"
        ],
        get_parent_cat_by_title(db=db, title="Jobs").id: [
            "Training", "Construction, Crafts & Production", "Office Work & Administration",
            "Gastronomy & Tourism", "Customer Service & Call Center", "Mini & Part-Time Jobs",
            "Internships", "Social Sector & Care", "Transport, Logistics & Traffic",
            "Sales, Purchasing & Sales", "More Jobs"
        ],
        get_parent_cat_by_title(db=db, title="Neighbourhood Help").id: [
            "Neighbourhood Help"
        ],
        get_parent_cat_by_title(db=db, title="Services").id: [
            "Elder Care", "Car, Bike & Boat", "Babysitter & Nanny", "Musician & Artist",
            "Travel & Event", "Animal Care & Training", "Transport & Moving", "Other Services"
        ],
        get_parent_cat_by_title(db=db, title="Family, Child & Baby").id: [
            "Elderly Care", "Baby & Children's Clothing", "Baby & Children's Shoes",
            "Baby Equipment", "Baby Carriers & Child Seats", "Babysitter & Child Care",
            "Strollers & Buggies", "Children's Room Furniture", "Toys", "Other Family, Child & Baby"
        ],
        get_parent_cat_by_title(db=db, title="Pets").id: [
            "Fish", "Dogs", "Cats", "Small Animals", "Livestock", "Horses",
            "Animal Training & Care", "Missing Animals", "Birds", "Accessories"
        ],
        get_parent_cat_by_title(db=db, title="Fashion & Beauty").id: [
            "Beauty & Health", "Women's Clothing", "Women's Shoes", "Men's Clothing",
            "Men's Shoes", "Bags & Accessories", "Watches & Jewelry", "Other Fashion & Beauty"
        ],
        get_parent_cat_by_title(db=db, title="Lessons & Courses").id: [
            "Health & Beauty", "Computer Courses", "Esoteric & Spiritual", "Cooking & Baking",
            "Art & Design", "Music & Singing", "Tutoring", "Sports Courses",
            "Language Courses", "Dance Courses", "Further Education", "Other Lessons & Courses"
        ],
        get_parent_cat_by_title(db=db, title="Admission tickets & tickets").id: [
            "Rail & Public Transport", "Comedy & Cabaret", "Vouchers", "Children",
            "Concerts", "Sports", "Theatre & Musicals", "More Tickets"
        ],
        get_parent_cat_by_title(db=db, title="Leisure, hobbies & neighbourhood").id: [
            "Esotericism & Spirituality", "Food & Drink", "Leisure Activities",
            "Handicrafts, Crafts & Arts and Crafts", "Art & Antiques",
            "Artist & Musician", "Model Making", "Travel & Event Services",
            "Collect", "Sports & Camping", "Junk", "Lost & Found",
            "Other Leisure, Hobby & Neighborhood"
        ],
        get_parent_cat_by_title(db=db, title="Real Estate").id: [
            "Temporary & Shared Accommodation", "Condominiums", "Holiday & Foreign Properties",
            "Garages & Parking Spaces", "Commercial Real Estate", "Land & Gardens",
            "Houses for Sale", "Houses for Rent", "Rental Apartments", "Moving & Transport",
            "Other Properties"
        ],
        get_parent_cat_by_title(db=db, title="Music, Movies & Books").id: [
            "Books & Magazines", "Office & Stationery", "Comics",
            "Technical Books, School & Study", "Movies & DVDs",
            "Music & CDs", "Musical Instruments", "More Music, Movies & Books"
        ],
        get_parent_cat_by_title(db=db, title="Give away & Swap").id: [
            "Exchange", "Lending", "Give Away"
        ],
        get_parent_cat_by_title(db=db, title="Undefined").id: ["Undefined"]
    }


def get_valid_titles():
    """
    Returns a set of all valid sub-category titles based on the category mapping.
    """
    valid_titles = set()
    for sub_cat_list in category_mapping.values():
        for title in sub_cat_list:
            valid_titles.add(title)
    return valid_titles


def validate_title(sub_cat_title):
    """
    Validates the given sub-category title against the set of valid titles.
    """
    valid_titles = get_valid_titles()
    if sub_cat_title not in valid_titles:
        raise ValueError(f"Invalid title '{sub_cat_title}'. Must be one of {valid_titles}")
    return sub_cat_title


def validate_parent_id(sub_cat_title, parent_id):
    """
    Validates the parent category ID for the given sub-category title.
    """
    for parent, sub_cat_list in category_mapping.items():
        for sub_cat in sub_cat_list:
            if sub_cat_title == sub_cat:
                if parent_id != parent:
                    raise ValueError("Invalid parent_id.")
                return parent_id


class SubCatBase(BaseModel):
    """
    Base schema for sub-categories containing common fields.
    """
    title: str | None = "Undefined"

    @model_validator(mode='before')
    def check_valid_title(cls, values):
        """
        Validator to check if the provided title is valid.
        """
        title = values.get('title')
        return validate_title(title)


class SubCatUpdate(BaseModel):
    """
    Schema for updating a sub-category.
    """
    title: str

    @model_validator(mode='before')
    def check_valid_title(cls, values):
        """
        Validator to check if the provided title is valid.
        """
        title = values.get('title')
        return validate_title(title)


class SubCatCreate(SubCatBase):
    """
    Schema for creating a new sub-category.
    """
    parent_id: int

    @model_validator(mode='before')
    def check_valid_parent_id(cls, values):
        """
        Validator to check if the parent ID is valid for the provided title.
        """
        parent_id = values.get('parent_id')
        sub_cat_title = values.get('title')
        return validate_parent_id(sub_cat_title, parent_id)


class SubCatInDB(SubCatBase):
    """
    Schema representing a sub-category stored in the database.
    """
    id: int
    parent_id: int

    @model_validator(mode='before')
    def check_valid_parent_id(cls, values):
        """
        Validator to check if the parent ID is valid for the provided title.
        """
        parent_id = values.get('parent_id')
        sub_cat_title = values.get('title')
        return validate_parent_id(sub_cat_title, parent_id)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SubCat(SubCatInDB):
    """
    Schema for returning sub-category data in API responses.
    """
    pass
