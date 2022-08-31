from flask import current_app as app
import boto3

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

def upload_file_to_s3(file, bucket_name, file_name, content_type, acl="public-read"):
    """
    Docs: http://boto3.readthedocs.io/en/latest/guide/s3.html
    """
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file_name,
            ExtraArgs={
                "ACL": acl,
                "ContentType": content_type    #Set appropriate content type as per the file
            }
        )
    except Exception as e:
        print("Something Happened: ", e)
        app.logger.critical("Uploading file to s3" + str(e))
        return ""
    return "{}{}".format(app.config["S3_LOCATION"], file_name)

def resize_image_size(width, height):
    if width < 320:
        height *= (320 / width)
        width = 320
    if width > 1080:
        height *= (width / 1080)
        width = 1080
    if height < 566:
        height = 566
    if height > 1350:
        height = 1350
    return (width, height)