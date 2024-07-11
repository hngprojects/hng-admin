from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/deactivate', methods=['POST'])
def deactivate():
    token = request.form.get('token')
    user_id = request.form.get('user_id')
    text = request.form.get('text')

    if not text:
        return jsonify({"response_type": "ephemeral", "text": "Please specify the user(s) to deactivate."})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    users = text.split()
    response_message = f"User <@{user_id}> is deactivating users: {', '.join(users)}"

    # Print the text to the console
    print(f"Deactivate command triggered by user <@{user_id}> with users: {text}")

    for user in users:
        # Extract the user ID from the escaped user format <@U1234|user>
        user_id_to_deactivate = user.split('|')[0][2:]
        deactivate_payload = {
            "user_id": user_id_to_deactivate
        }
        # Uncomment this section to actually send the request to Slack API
        # response = requests.post('https://slack.com/api/admin.users.remove', headers=headers, json=deactivate_payload)
        # if not response.ok:
        #     return jsonify({"error": response.text})

    # Return a public message
    return jsonify({
        "response_type": "in_channel",
        "text": response_message,
        "delete_original": True
    })

@app.route('/deactivate_all', methods=['POST'])
def deactivate_all():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    user_id = request.form.get('user_id')
    text = request.form.get('text')

    exclude_channels = []
    if text and text.startswith('exclude='):
        exclude_channels = text[len('exclude='):].split(',')

    if channel_id in exclude_channels:
        return jsonify({"response_type": "ephemeral", "text": "This channel is excluded from deactivation."})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Uncomment this section to actually send the request to Slack API
    # response = requests.get('https://slack.com/api/conversations.members', headers=headers, params={"channel": channel_id})
    # if not response.ok:
    #     return jsonify({"error": response.text})

    # members = response.json().get('members', [])
    
    # Simulated members for testing
    members = ['U12345678', 'U87654321']  # Remove this line and uncomment above section to fetch actual members

    if exclude_channels:
        response_message = f"User <@{user_id}> is deactivating all users in the channel except in the excluded channels: {', '.join(exclude_channels)}."
    else:
        response_message = f"User <@{user_id}> is deactivating all users in the channel."

    # Print the text to the console
    print(f"Deactivate all command triggered by user <@{user_id}> with exclusions: {text}")

    for member in members:
        deactivate_payload = {
            "user_id": member,
            "channel_id": channel_id
        }
        # Uncomment this section to actually send the request to Slack API
        # response = requests.post('https://slack.com/api/admin.users.remove', headers=headers, json=deactivate_payload)
        # if not response.ok:
        #     return jsonify({"error": response.text})

    # Return a public message
    return jsonify({
        "response_type": "in_channel",
        "text": response_message,
        "delete_original": True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
