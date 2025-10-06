from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3, uuid, json

app = Flask(__name__)
CORS(app)

# -------------------------------
# AWS Clients Initialization
# -------------------------------
region = "ap-south-1"  # Mumbai region
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('CustomerEnquiries')
ses = boto3.client('ses', region_name=region)
bedrock = boto3.client('bedrock-runtime', region_name=region)

# -------------------------------
# Routes
# -------------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to Shyam's Customer Enquiry Manager Backend!",
        "status": "running"
    })

@app.route('/submit', methods=['POST'])
def submit_enquiry():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        if not (name and email and message):
            return jsonify({"error": "Missing name, email or message"}), 400

        enquiry_id = str(uuid.uuid4())

        # --- Step 1: Store enquiry in DynamoDB ---
        table.put_item(Item={
            'id': enquiry_id,
            'name': name,
            'email': email,
            'message': message
        })

        # --- Step 2: Use Amazon Bedrock for classification ---
        prompt = f"Classify this customer enquiry into Billing, Technical, or General: {message}"

        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 256,
                "temperature": 0.7,
                "topP": 0.9
            }
        }

        response = bedrock.invoke_model(
            modelId="amazon.titan-text-lite-v1",
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        # Parse the Bedrock JSON response
        response_body = json.loads(response["body"].read())
        category = response_body["results"][0]["outputText"].strip()

        # Safety fallback
        if not category:
            category = "Uncategorized"



        # --- Step 3: Send confirmation email using SES ---
        sender_email = "gmail"        # replace with your verified sender
        receiver_email = "your@gmail.com"     # replace with your verified receiver

        ses.send_email(
            Source=sender_email,
            Destination={'ToAddresses': [receiver_email]},
            Message={
                'Subject': {'Data': 'Your Enquiry Has Been Received!'},
                'Body': {
                    'Text': {'Data': f"Hello {name},\n\nYour enquiry has been categorized as: {category}\n\nMessage: {message}\n\nThank you,\nTeam Shyam"}
                }
            }
        )

        # --- Step 4: Return success response ---
        return jsonify({
            "status": "success",
            "id": enquiry_id,
            "category": category
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Main entry
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
