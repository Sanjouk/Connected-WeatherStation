from flask import Blueprint, request, jsonify
from data.models import ValidationError, SettingsModel
from data.db import get_collection
from datetime import datetime




settings_api = Blueprint('settings_api', __name__)


@settings_api.route('/api/settings', methods=['POST', 'GET'])
def settings():
    SETTINGS_COLLECTION = get_collection('settings')
    if request.method == 'POST':
        if SETTINGS_COLLECTION is None:
            return jsonify({"status": "error", "message": "Database not connected"}), 503

        try:
            data = request.get_json()
            try:
                SettingsModel(**data)
            except ValidationError as e:
                return jsonify({"status": "error", "message": e.message}), 400

            existing = SETTINGS_COLLECTION.find_one()
            if not existing:
                result = SETTINGS_COLLECTION.insert_one(data.dict)
                print(f"Saved settings with ID: {result.inserted_id}")
                return jsonify({"status": "ok"}), 200
            else:
                return jsonify({"status": "error", "message": "Settings already exists"}), 400
        except Exception as e:
            print(f"Error while saving settings: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    elif request.method == 'GET':
        if SETTINGS_COLLECTION is None:
            return jsonify({"status": "error", "message": "Database not connected"}), 503
        try:
            settings = SETTINGS_COLLECTION.find_one()
            if settings:
                # Remove MongoDB's default _id field before sending
                settings.pop('_id', None)
                return jsonify(settings), 200
            else:
                return jsonify({"status": "error", "message": "Settings not found"}), 404

        except Exception as e:
            print(f"Error while fetching settings: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500


@settings_api.route('/api/settings', methods=['PUT'])
def setting():
    SETTINGS_COLLECTION = get_collection('settings')
    if SETTINGS_COLLECTION is None:
        return jsonify({"status": "error", "message": "Database not connected"}), 503

    try:
        data = request.get_json()
        # path = data['path']
        # value = data['value']
        # if not path or value is None:
        #     return jsonify({"status": "error", "message": "Missing 'path' or 'value' in request body"}), 400

        if 'changes' in data and isinstance(data['changes'], dict):
            changes = data['changes']
            is_single_change = False

        # Check for the single-change format
        elif 'path' in data and 'value' in data:
            # Format: {"path": "...", "value": ...}
            path = data['path']
            value = data['value']
            changes = {path: value}
            is_single_change = True

        else:
            return jsonify({
                "status": "error",
                "message": "Invalid request body. Must contain either {'path', 'value'} for single change or {'changes': {path: value, ...}} for bulk change."
            }), 400

        if not changes:
            return jsonify({"status": "error", "message": "No changes specified."}), 400

        changes["updatedAt"] = datetime.now()
        # update_query = {"$set": {path:value, "updatedAt": datetime.now()}}
        update_query = {"$set": changes}
        # existence_filter = {path: {"$exists": True}}
        existence_filters = [{path: {"$exists": True}} for path in changes.keys()]
        final_query = {"$and": existence_filters} if existence_filters else {}
        result = SETTINGS_COLLECTION.update_one(final_query, update_query)
        # result = SETTINGS_COLLECTION.update_one(existence_filter, update_query)

    #     if result.matched_count == 0:
    #         if not SETTINGS_COLLECTION.find_one():
    #             return jsonify({"status": "error", "message": "Settings document not found"}), 404
    #         else:
    #             return jsonify({"status": "error",
    #                             "message": f"Field not found at path: '{path}'. Update rejected to prevent adding a new field."}), 400
    #
    #     if result.modified_count > 0:
    #         return jsonify({"status": "ok", "message": f"Successfully updated {path} to {value}"}), 200
    #     else:
    #          # Matched count > 0 but modified count is 0 means value was already set
    #         return jsonify({"status": "ok", "message": f"Settings for {path} was already {value}. No change made."}), 200
    #
    # except Exception as e:
    #     print(f"Error while updating settings: {e}")
    #     return jsonify({"status": "error", "message": str(e)}), 500
        if result.matched_count == 0:
            # Check if settings document exists at all
            if not SETTINGS_COLLECTION.find_one():
                return jsonify({"status": "error", "message": "Settings document not found"}), 404
            else:
                # Document exists, so one or more paths were missing/invalid
                missing_path_msg = "One or more specified fields (paths) were not found." if not is_single_change else f"Field not found at path: '{path}'."
                return jsonify({
                    "status": "error",
                    "message": f"Update rejected. {missing_path_msg} Update rejected to prevent adding a new field."
                }), 400

        if result.modified_count == 0:
            # Matched count > 0 but modified count is 0
            return jsonify(
                {"status": "ok", "message": "Settings were already set to the requested values. No change made."}), 200
        else:
            return jsonify({"status": "ok", "message": "Settings were successfully updated"}), 200
    except Exception as e:
        print(f"Error while updating settings: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500