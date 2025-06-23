# AWS Sydney Summit 2025 - IoT Demo Application

A fun Streamlit app that lets you control IoT devices using AWS services, Amazon Nova Pro, and the **AWS open-sourced Strands Agents** framework.

## Features

- 🤖 **AWS Strands Agents** - Open-source framework that makes AI agents super easy to build
- 🧠 **Amazon Nova Pro** - AWS's smart AI model that understands what you're asking
- 🐱 Cat feeder remote control via AWS IoT Core
- 🚗 Vehicle telemetry monitoring
- 🦾 Iron Man helmet control (Mark 3)
- 📊 Real-time data visualization

## About AWS Strands Agents

This demo shows off **AWS Strands Agents**, an open-source framework that makes it easy to build AI agents that can actually do stuff. Here's what makes it cool:

- 🔧 **Tool Integration** - Connect your own tools and functions easily
- 🔄 **Streaming Support** - Get responses in real-time as they're generated
- 🎯 **Model Flexibility** - Works with different AI models, including Amazon Nova Pro
- 📦 **Open Source** - Free to use and contribute to on GitHub

Learn more: [AWS Strands Agents on GitHub](https://github.com/strands-agents/sdk-python)

## Prerequisites

- Python 3.8 or higher
- AWS Account with appropriate permissions
- Git (optional, for cloning)

## Quick Start Guide

### Step 1: Download the Code

**Option A: Download ZIP**
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file to your desired location

**Option B: Clone with Git**
```bash
git clone https://github.com/chiwaichan/AWSSydneySummit2025Demo
cd AWSSydneySummit2025Demo
```

### Step 2: Set Up Python Virtual Environment

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### Step 3: Install Required Packages

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

### Step 4: Configure AWS Credentials

**Option A: AWS CLI (Recommended)**
1. Install AWS CLI: https://aws.amazon.com/cli/
2. Configure credentials:
```bash
aws configure
```
Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format: `json`

**Option B: Environment Variables**
```bash
# On Windows (Command Prompt)
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1

# On macOS/Linux
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### Step 5: Enable Amazon Nova Pro

1. **Log into AWS Console**
2. **Navigate to Amazon Bedrock**
   - Search for "Bedrock" in the AWS Console
   - Click on "Amazon Bedrock"

3. **Request Model Access**
   - In the left sidebar, click "Model access"
   - Click "Request model access" or "Manage model access"
   - Find "Amazon Nova Pro" in the list
   - Click "Request access" next to it
   - Fill out the form if required
   - Wait for approval (usually instant for Nova models)

4. **Verify Access**
   - Ensure "Amazon Nova Pro" shows "Access granted" status

### Step 6: Set Up AWS IoT Core (Optional)

*Note: The app works with sample data without IoT setup*

For full IoT functionality:
1. Go to AWS IoT Core console
2. Create IoT policies with publish permissions
3. Create IoT things for your devices
4. Update topic names in `app.py` if needed

### Step 7: Run the Application

```bash
# Make sure your virtual environment is activated
# Run the Streamlit app
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Usage Guide

### AI Agent Tab (Powered by AWS Strands Agents)
- Type "tools" to see available commands
- Ask natural language questions like:
  - "Show me vehicle telemetry"
  - "Feed the cat for 3 seconds"
  - "Open the Iron Man helmet"
- Watch how Strands Agents figures out which tools to use and runs them for you

### Cat Feeder Control
- Use Forward/Stop/Backward buttons
- Set timed feeding sessions

### Vehicle Telemetry
- View real-time vehicle data
- Monitor temperature, humidity, GPS location

### Iron Man Helmet
- Control faceplate (open/close)
- Control eye lights (on/off)

## Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
```bash
# Ensure virtual environment is activated
# Reinstall packages
pip install -r requirements.txt
```

**"AWS credentials not found"**
- Verify AWS credentials are configured
- Check AWS CLI with: `aws sts get-caller-identity`

**"Access denied for Nova Pro"**
- Ensure model access is granted in Bedrock console
- Wait a few minutes after approval

**"Streamlit command not found"**
```bash
# Reinstall streamlit
pip install streamlit --upgrade
```

### Getting Help

1. Check AWS CloudWatch logs for IoT errors
2. Verify your AWS region supports Nova Pro
3. Ensure IAM permissions for Bedrock and IoT Core

## Project Structure

```
AWSSydneySummit2025Demo/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
└── README.md          # This file
```

## Technologies Used

- **AWS Strands Agents** - Open-source agentic framework (GitHub: awslabs/strands)
- **Amazon Bedrock** - Nova Pro AI model
- **AWS IoT Core** - Device messaging
- **IAM** - Access management
- **Streamlit** - Web application framework

## Security Notes

- Never commit AWS credentials to code
- Use IAM roles when possible
- Regularly rotate access keys
- Follow AWS security best practices

## Next Steps

1. Customize vehicle telemetry with real API
2. Add more IoT devices
3. Implement data persistence
4. Add user authentication
5. Deploy to AWS (ECS, Lambda, etc.)

## Support

For issues during AWS Sydney Summit 2025:
- Visit the AWS booth
- Ask the demo team for assistance

---

**Happy coding! 🚀**