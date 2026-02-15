from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import json
import csv
from fuzzywuzzy import fuzz

# Create a database object, but don't initialize Flask
db = SQLAlchemy()
bcrypt = Bcrypt()


# Define the model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.Integer, unique=False, nullable=True)
    weight = db.Column(db.Integer, unique=False, nullable=True)
    age = db.Column(db.Integer, unique=False, nullable=True)
    role = db.Column(db.String(80), unique=False, nullable=False, default='client')
    avatar = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80), unique=True, nullable=False)
    coordinates = db.Column(db.String, nullable=False)  # Stored as a JSON string

    def __repr__(self):
        return f"<Area {self.type, self.coordinates}>"


class Prescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    constitute = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=False)
    indication = db.Column(db.String, nullable=False)
    constituteNumber = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Prescription {self.name, self.constitute, self.function}>"


class ChinesePrescription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    constitute = db.Column(db.String, nullable=False)
    action = db.Column(db.String, nullable=False)
    indication = db.Column(db.String, nullable=False)
    constituteNumber = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Chinese Prescription {self.name, self.constitute, self.function}>"


class Herb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    production_regions = db.Column(db.String, nullable=False)
    properties = db.Column(db.String, nullable=False)
    functions = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    relate_prescription = db.Column(db.String, nullable=False)  # Stored as a JSON string
    classification = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Herb {self.name, self.category, self.origin}>"


class ChineseHerb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    production_regions = db.Column(db.String, nullable=False)
    properties = db.Column(db.String, nullable=False)
    functions = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    relate_prescription = db.Column(db.String, nullable=False)  # Stored as a JSON string
    classification = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Chinese Herb {self.name, self.category, self.origin}>"


class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.Enum('user', 'assistant'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


# Herb Quiz score
class Rank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    accuracy = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)  # Number of times you do the question
    totalTime = db.Column(db.Integer, nullable=False)  # Time spent doing the question

    def __repr__(self):
        return f"<Rank {self.username}>"


# Prescription Quiz score
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    accuracy = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Integer, nullable=False)  # Number of times you do the question
    totalTime = db.Column(db.Integer, nullable=False)  # Time spent doing the question

    def __repr__(self):
        return f"<Score {self.username}>"


class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imageUrl_en = db.Column(db.String, nullable=False)
    imageUrl_zh = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<Image {self.imageUrl}>"


class HealthySuggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    suggestion_en = db.Column(db.String, nullable=False)
    suggestion_zh = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HealthySuggestion {self.username}>"


class StoryMode(db.Model):
    __table_args__ = (
        db.PrimaryKeyConstraint('story_number', 'id'),  # Composite primary key
    )

    story_number = db.Column(db.Integer, nullable=False)
    id = db.Column(db.Integer, nullable=False)
    scene = db.Column(db.String, nullable=False)
    character = db.Column(db.String, nullable=True)  # JSON array
    text = db.Column(db.String, nullable=False)
    option = db.Column(db.String, nullable=True)  # JSON array
    next = db.Column(db.String, nullable=True)  # JSON array
    bg_image = db.Column(db.String, nullable=False)  # path
    character_image = db.Column(db.String, nullable=True)  # path, JSON array
    audio_file = db.Column(db.String, nullable=True)  # path
    character_en = db.Column(db.String, nullable=True)
    text_en = db.Column(db.String, nullable=False)
    option_en = db.Column(db.String, nullable=True)


# Initialize the database and insert the default data
def init_db(app):
    with app.app_context():
        db.create_all()

        # Avoid repeated insertions
        if not User.query.first():
            default_users = [
                User(username="Admin", password="$2b$12$FeqB4xc26Krjgis.11iVy./elyAnsTHsXmmAFK.QRDlU9JsxzVDfq",
                     role='admin', avatar='/static/assets/BlankAvatar-Cl_LpKw_.png'),
                User(username="Client", password="$2b$12$FeqB4xc26Krjgis.11iVy./elyAnsTHsXmmAFK.QRDlU9JsxzVDfq",
                     avatar='/static/assets/BlankAvatar-Cl_LpKw_.png'),
            ]
            db.session.add_all(default_users)
            db.session.commit()
            print("Default user data has been inserted!")


        if not Area.query.first():
            default_areas = [
                Area(type="polygon", coordinates=json.dumps([[39.8704, 116.4716], [39.8781, 116.4715],
                                                             [39.8781, 116.4772], [39.8749, 116.4797],
                                                             [39.8745, 116.4831], [39.8728, 116.4828],
                                                             [39.8702, 116.4797]])),
            ]
            db.session.add_all(default_areas)
            db.session.commit()
            print("Default region data has been inserted!")

        if not Image.query.first():
            default_images = [
                Image(imageUrl_en='https://pic4.zhimg.com/v2-000f1c1ae3e7ae215e216912aa81e647_720w.jpg?source=172ae18b',
                      imageUrl_zh='https://pic4.zhimg.com/v2-000f1c1ae3e7ae215e216912aa81e647_720w.jpg?source=172ae18b'),
                Image(imageUrl_en='https://bpic.588ku.com/back_list_pic/20/08/04/42586bb0e728cda777e35e774986df52.jpg!/fh/300/quality/90/unsharp/true/compress/true',
                      imageUrl_zh='https://bpic.588ku.com/back_list_pic/20/08/04/42586bb0e728cda777e35e774986df52.jpg!/fh/300/quality/90/unsharp/true/compress/true'),
                Image(imageUrl_en='https://oss.cyzone.cn/2022/0104/f39b42dfe92daac729eb9d2d28ec6d48.jpg',
                      imageUrl_zh='https://oss.cyzone.cn/2022/0104/f39b42dfe92daac729eb9d2d28ec6d48.jpg')
            ]
            db.session.add_all(default_images)
            db.session.commit()
            print("The default homepage image is inserted")

        if not Prescription.query.first():
            # Open the CSV file
            with open('herbs_data.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Go through each row
                for row in reader:
                    constituteNumber = len(row[1].split(';'))
                    pre = Prescription(name=row[0], constitute=row[1], action=row[2], indication=row[3],
                                       constituteNumber=constituteNumber)
                    db.session.add(pre)
                    db.session.commit()
            print("The default EN prescription data is inserted")

        if not ChinesePrescription.query.first():
            # Open the CSV file
            with open('chinese_herbs_data.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Go through each row
                for row in reader:
                    constituteNumber = len(row[1].split(';'))
                    pre = ChinesePrescription(name=row[0], constitute=row[1], action=row[2], indication=row[3],
                                              constituteNumber=constituteNumber)
                    db.session.add(pre)
                    db.session.commit()
            print("The default CH prescription data is inserted")

        if not Herb.query.first():
            with open('Updated_Constitutes_Data.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    prescriptions = Prescription.query.all()
                    relate = []
                    for prescription in prescriptions:
                        cons = prescription.constitute
                        result = cons.split(';')
                        stander_result = [item.strip().lower() for item in result]
                        stander_name = row[0].strip().lower()
                        if stander_name in stander_result:
                            relate.append(prescription.id)
                    relate_json = json.dumps(relate)
                    herb = Herb(name=row[0], category=row[1], origin=row[2], production_regions=row[3],
                                properties=row[4], functions=row[5], image=row[6], relate_prescription=relate_json,
                                classification=row[7])
                    db.session.add(herb)
                    db.session.commit()
                print("By default, EN drugs are inserted")

        if not ChineseHerb.query.first():
            with open('chinese_constitutes_data_updated.csv', mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    prescriptions = ChinesePrescription.query.all()
                    relate = []
                    for prescription in prescriptions:
                        cons = prescription.constitute
                        result = cons.split(';')
                        stander_result = [item.strip().lower() for item in result]
                        stander_name = row[0].strip().lower()
                        # Fuzzy matching
                        for item in stander_result:
                            # Use fuzz.ratio to calculate similarity
                            similarity = fuzz.ratio(stander_name, item)
                            if similarity >= 80:  # Set a similarity threshold
                                relate.append(prescription.id)
                                break  # If the match is successful, the loop is jumped
                    relate_json = json.dumps(relate)
                    herb = ChineseHerb(name=row[0], category=row[1], origin=row[2], production_regions=row[3],
                                       properties=row[4], functions=row[5], image=row[6],
                                       relate_prescription=relate_json, classification=row[7])
                    db.session.add(herb)
                    db.session.commit()
                print("The default CH drug is inserted")

        # Quotation mark repair function
        def fix_json_array(raw):
            if not raw or str(raw).strip() in ("", "[]"):
                return []
            try:
                s = str(raw).strip()
                if s.startswith('"') and s.endswith('"'):
                    s = s[1:-1]
                s = s.replace('""', '"')
                return json.loads(s)
            except Exception as e:
                print(f"Field repair failed: {raw} → {e}")
                return []

        # Data insertion logic
        if not StoryMode.query.first():
            with open('visual_novel_huoxiang_tree converted_file_utf8.csv', mode='r', newline='',
                      encoding='utf-8') as file:
                reader = csv.reader(file)

                def get_image_url(image_filename):
                    return f"/static/Story/{image_filename}"

                for row in reader:
                    try:
                        # Fix options, redirects, and English options fields
                        option = json.dumps(fix_json_array(row[5]))
                        next_ids = json.dumps(fix_json_array(row[6]))
                        option_en = json.dumps(fix_json_array(row[12]))

                        # Background image URL stitching
                        bg_image_url = get_image_url(row[7])

                        # Fixed the character portrait field as a path array
                        raw_image_json = row[8].strip()
                        image_filenames = fix_json_array(raw_image_json)
                        image_urls = [
                            f"/static/Story/character_image/{name.strip()}"
                            for name in image_filenames if name.strip()
                        ]
                        character_image_json = json.dumps(image_urls)

                        story = StoryMode(
                            story_number=row[0],
                            id=row[1],
                            scene=row[2],
                            character=row[3],
                            text=row[4],
                            option=option,
                            next=next_ids,
                            bg_image=bg_image_url,
                            character_image=character_image_json,
                            audio_file=row[9],
                            character_en=row[10],
                            text_en=row[11],
                            option_en=option_en
                        )

                        db.session.add(story)
                        db.session.commit()
                    except Exception as e:
                        print(f"Failed to insert a record")

            print('Story insert successfully')


