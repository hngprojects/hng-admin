from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/deactivate', methods=['POST'])
def deactivate():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    text = request.form.get('text')

    if not text:
        return jsonify({"response_type": "ephemeral", "text": "Please specify the user(s) to deactivate."})

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    users = text.split()
    print(users)
    response_message = f"Deactivating users: {', '.join(users)}"

    for user in users:
        deactivate_payload = {
            "user_id": user
        }
        # Uncomment this section to actually send the request to Slack API
        # response = requests.post('https://slack.com/api/admin.users.remove', headers=headers, json=deactivate_payload)
        # if not response.ok:
        #     return jsonify({"error": response.text})

    return jsonify({"response_type": "in_channel", "text": response_message})

@app.route('/deactivate_all', methods=['POST'])
def deactivate_all():
    token = request.form.get('token')
    channel_id = request.form.get('channel_id')
    text = request.form.get('text')
    print(text)

    exclude_channels = []
    if text and text.startswith('exclude:'):
        exclude_channels = text[len('exclude:'):].split(',')

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

    response_message = "Deactivating all users in the channel except in the excluded channels."

    for member in members:
        deactivate_payload = {
            "user_id": member,
            "channel_id": channel_id
        }
        # Uncomment this section to actually send the request to Slack API
        # response = requests.post('https://slack.com/api/admin.users.remove', headers=headers, json=deactivate_payload)
        # if not response.ok:
        #     return jsonify({"error": response.text})

    return jsonify({"response_type": "in_channel", "text": response_message})

if __name__ == '__main__':
    app.run(debug=True)
