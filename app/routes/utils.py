import os
import openai
import uuid_utils as uuid
from datetime import datetime, date
import boto3
from pydantic import EmailStr
from dotenv import load_dotenv
from typing import Annotated
from fastapi import HTTPException, status, File, Form, UploadFile
from app.schemas import user as s_user


load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

MEGABYTE = 1024 * 1024


def generate_description(keywords, parameters):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a post description using these keywords: {keywords} "
                                            f"and parameters: {parameters}."}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def generate_download_link(image_name):
    return f"https://buysellusers.s3.amazonaws.com/{image_name}"


def upload_file(local_file: Annotated[UploadFile, File()], bucket_name,
                pic_name=None):
    s3_client = boto3.client(
        service_name='s3',
        region_name='eu-north-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
    if not pic_name:
        pic_name = os.path.basename(local_file.filename).replace(" ", "_")
    image_name = f"{uuid.uuid7()}_{dt_string}_{pic_name}"
    file_size = local_file.size
    file_content = local_file.content_type
    if file_size > MEGABYTE or "image" not in file_content:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Size to big or file not image.")
    try:
        s3_client.upload_fileobj(local_file.file, bucket_name, image_name)
        print(f'File {image_name} uploaded successfully.')
        download_link = generate_download_link(image_name)
        return download_link
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_image_from_s3(object_name, bucket_name):
    s3_client = boto3.client(
        service_name='s3',
        region_name='eu-north-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
        print(f'File {object_name} deleted successfully.')
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def parse_user_create_base(
    first_name: str = Form(...),
    last_name: str = Form(...),
    birthday: date = Form(...),
    username: str = Form(...),
    email: EmailStr = Form(...),
    tel_number: str = Form(...),
    street: str = Form(...),
    house_number: str = Form(...),
    zip_code: str = Form(...),
    city_town_village: str = Form(...),
    country: str = Form(...),
    commercial_account: bool | None = Form(False),
    notification: bool | None = Form(True),
    account_status: bool | None = Form(True),
    password: str = Form(...)
) -> s_user.UserCreateBase:
    return s_user.UserCreateBase(**locals())


def parse_user_update_base(
    first_name: str | None = Form(None),
    last_name: str | None = Form(None),
    birthday: date | None = Form(None),
    username: str | None = Form(None),
    email: EmailStr | None = Form(None),
    tel_number: str | None = Form(None),
    street: str | None = Form(None),
    house_number: str | None = Form(None),
    zip_code: str | None = Form(None),
    city_town_village: str | None = Form(None),
    country: str | None = Form(None),
    commercial_account: bool | None = Form(None),
    notification: bool | None = Form(None),
    account_status: bool | None = Form(None),
    password: str | None = Form(None)
) -> s_user.UserUpdateBase:
    update_data = {key: value for key, value in locals().items() if value is not None}
    return s_user.UserUpdateBase(**update_data)
