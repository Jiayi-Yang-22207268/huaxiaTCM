from flask import Blueprint, jsonify
from database import StoryMode
import json

story_bp = Blueprint('story_bp', __name__, url_prefix='/api/story')

def to_dict(story):
    return {
        "story_number": story.story_number,
        "id": story.id,
        "label": story.scene,
        "speaker": story.character,
        "dialog": story.text,
        "choices": json.loads(story.option or "[]"),
        "next_id": json.loads(story.next or "[]"),
        "background": story.bg_image,
        "character_image": json.loads(story.character_image or "[]"),
        "audio": story.audio_file,
        "speaker_en": story.character_en,
        "dialog_en": story.text_en,
        "choices_en": json.loads(story.option_en or "[]"),

    }

@story_bp.route('/begin', methods=['GET'])
def beginStory():
    story = StoryMode.query.first()
    return jsonify(to_dict(story))


# Get a specific plot node
@story_bp.route('/<int:story_id>', methods=['GET'])
def get_story(story_id):
    story = StoryMode.query.filter_by(id=story_id).first()
    if story:
        print(story)
        print(story.id)
        return jsonify(to_dict(story))
    else:
        return jsonify({"message": "Story not found"}), 404


# Get the next story node
@story_bp.route('/next/<int:story_id>', methods=['GET'])
def get_next_story(story_id):
    # Get the current episode
    current_story = StoryMode.query.filter_by(id=story_id).first()
    if current_story:
        next_id = current_story.next
        next_story_ids = eval(next_id)  # Get the IDs of the two possible next options
        stories = []
        for next_story_id in next_story_ids:
            next_story = StoryMode.query.filter_by(id=next_story_id).first()
            if next_story:
                stories.append(to_dict(next_story))
        return jsonify(stories)
    else:
        return jsonify({"message": "Story not found"}), 404
