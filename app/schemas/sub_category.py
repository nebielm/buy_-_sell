from pydantic import BaseModel, model_validator, Field
from typing import Annotated


category_mapping = {
        "Car, Bike & Boat": [
            "Cars", "Auto Parts & Tires", "Boats & Boat Accessories", "Bicycles & Accessories",
            "Motorcycles & Scooters", "Motorcycle Parts & Accessories", "Commercial Vehicles & Trailers",
            "Repairs & Services", "Caravans & Mobile Homes", "Other Car, Bike & Boat"
        ],
        "Electronics": [
            "Audio & Hi-Fi", "Electronics Services", "Photo", "Mobile & Telephone",
            "Household Appliances", "Consoles", "Laptops", "PCs", "PC Accessories & Software",
            "Tablets & Readers", "TV & Video", "Video Games", "Other Electronics"
        ],
        "Home & Garden": [
            "Bathrooms", "Office", "Decoration", "Home & Garden Services", "Garden Accessories & Plants",
            "Home Textiles", "DIY", "Kitchen & Dining Room", "Lamps & Lights", "Bedrooms", "Living Room",
            "Other Home & Garden"
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
            "Elderly Care", "Car, Bike & Boat", "Babysitter & Child Care", "Artist & Musician",
            "Travel & Event", "Animal Care & Training", "Moving & Transport", "Other Services"
        ],
        "Family, Child & Baby": [
            "Elderly Care", "Baby & Children's Clothing", "Baby & Children's Shoes",
            "Baby Equipment", "Baby Carriers & Child Seats", "Babysitter & Child Care",
            "Strollers & Buggies", "Children's Room Furniture", "Toys", "Other Family, Child & Baby"
        ],
        "Pets": [
            "Fish", "Dogs", "Cats", "Small Animals", "Livestock", "Horses",
            "Animal Care & Training", "Missing Animals", "Birds", "Accessories"
        ],
        "Fashion & Beauty": [
            "Beauty & Health", "Women's Clothing", "Women's Shoes", "Men's Clothing",
            "Men's Shoes", "Bags & Accessories", "Watches & Jewelry", "Other Fashion & Beauty"
        ],
        "Lessons & Courses": [
            "Beauty & Health", "Computer Courses", "Esoteric & Spiritual", "Cooking & Baking",
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


def validate_title(title):
    valid_titles = set()
    for sub_cat_list in category_mapping.values():
        for title in sub_cat_list:
            valid_titles.add(title)
    if title not in valid_titles:
        raise ValueError(f"Invalid title '{title}'. Must be one of {valid_titles}")
    return title


class SubCatBase(BaseModel):
    title: str | None = "Undefined"

    @model_validator(mode='before')
    def check_valid_title(cls, values):
        title = values.get('title')
        return validate_title(title)


class SubCatUpdate(BaseModel):
    title: str
    parent_id: Annotated[int, Field(gt=0)]

    @model_validator(mode='before')
    def check_valid_title(cls, values):
        title = values.get('title')
        return validate_title(title)


class SubCatCreate(SubCatBase):
    parent_id: Annotated[int, Field(gt=0)]


class SubCatInDB(SubCatBase):
    id: int
    parent_id: Annotated[int, Field(gt=0)]

    class Config:
        orm_mode = True


class SubCat(SubCatInDB):
    pass
