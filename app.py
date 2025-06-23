import streamlit as st
import boto3
import json
import time
from datetime import datetime
from strands import Agent, tool
import asyncio
from streamlit.runtime.scriptrunner import add_script_run_ctx
from botocore.exceptions import ClientError

@tool
def get_vehicle_telemetry() -> list:
    """
    Retrieves all vehicle telemetry data.
    
    Returns:
        list: A list of all vehicles and its telemetries
    
    NOTE: This function returns static sample data. To integrate with your own vehicle API:
    1. Replace the static data below with a call to your vehicle telemetry API
    2. Ensure your API returns data with these properties: temperature, humidity, light, 
       latitude, longitude, altitude, pitch, roll, x, y, z
    3. Structure the response as a list of vehicles with measurements
    """
    # TODO: Replace this static data with your own vehicle telemetry API call
    # Example: response = requests.get('https://your-api.com/vehicles/telemetry')
    
    static_data = [
        {
            'vehicle_name': 'Vehicle_001',
            'last_updated': '2024-12-19T10:30:00Z',
            'measurements': {
                'temperature': 23.5,
                'humidity': 65.2,
                'light': 850,
                'latitude': -33.8688,
                'longitude': 151.2093,
                'altitude': 58.0,
                'pitch': 2.1,
                'roll': -0.8,
                'x': 0.02,
                'y': -0.15,
                'z': 9.81
            }
        },
        {
            'vehicle_name': 'Vehicle_002',
            'last_updated': '2024-12-19T10:29:45Z',
            'measurements': {
                'temperature': 21.8,
                'humidity': 58.7,
                'light': 920,
                'latitude': -33.8650,
                'longitude': 151.2094,
                'altitude': 62.5,
                'pitch': 1.5,
                'roll': 0.3,
                'x': -0.01,
                'y': 0.08,
                'z': 9.79
            }
        }
    ]
    
    print(f"Retrieved telemetry data for {len(static_data)} vehicles:")
    for vehicle in static_data:
        measurements = vehicle.get('measurements', {})
        print(f"Vehicle: {vehicle.get('vehicle_name', 'Unknown')} - "
              f"Temperature: {measurements.get('temperature', 'N/A')}°C, "
              f"Humidity: {measurements.get('humidity', 'N/A')}%")
    
    return static_data

@tool
def send_cat_feeder_message(action: str) -> dict:
    """
    Send an MQTT message to activate the cat feeder at AWS Sydney Summit.
    
    Args:
        action (str): The string value for the action property, these are the allowed values "forward", "stop" and "backward"
    
    Returns:
        dict: The response from the IoT publish operation
    """
    # Create an IoT client
    iot_client = boto3.client('iot-data')
    
    # Create message with required action property
    message = {"action": action, "speed": 180}
    
    # Convert message to JSON string
    message_json = json.dumps(message)
    
    # Publish the message to the IoT topic
    topic = "my-project-iot-house-telemetry-house-telemetry-action"
    response = iot_client.publish(
        topic=topic,
        qos=1,  # Quality of Service: 1 means at least once delivery
        payload=message_json
    )
    
    return {"topic": topic, "action": action, "status": "sent", "response": str(response)}

@tool
def sleep_seconds(seconds: int) -> str:
    """
    Pauses execution for the specified number of seconds.
    
    Args:
        seconds (int): The number of seconds to sleep
    
    Returns:
        str: Confirmation message with the number of seconds slept
    """
    time.sleep(seconds)
    return f"Slept for {seconds} seconds"



# Iron Man tools ported from Lambda MCP to Strands
@tool
def set_iron_man_mark3_helmet_action(faceplate_state: str, eyes_state: str) -> str:
    """Set the state of the Iron Man Mark 3 Helmet
    
    Args:
        faceplate_state: The state of the Faceplate, the allowable states are 'face_open' or 'face_close'
        eyes_state: The state of the Eyes, the allowable states are 'on' or 'off'

    Returns:
        A string confirming the action
    """
    try:
        # Create an IoT client
        iot_client = boto3.client('iot-data')
        
        topic = "my-project-iot-suit-telemetry-suit-telemetry-action"
        payload = {"suit_name": "XIAOMark3Helmet", "action": faceplate_state, "eyes": eyes_state}

        # Convert payload to JSON string
        message_json = json.dumps(payload)
        
        # Publish the message
        iot_client.publish(
            topic=topic,
            qos=1,  # QoS 1 for at least once delivery
            payload=message_json
        )
        
        return f"The payload sent to topic is {message_json}"
        
    except ClientError as e:
        error_message = f"Error sending message to IoT topic: {str(e)}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        print(error_message)
        return error_message

@tool
def control_cat_feeder_iot(action: str, speed: int = 180) -> dict:
    """Control the Cat Feeder motor via IoT Core, this Cat Feeder is currently on location at the AWS Sydney Summit 2025 event. We are Live at the event on June 4th and 5th. 
    
    Args:
        action: The action to perform, must be one of: 'forward', 'backward', 'stop'
        speed: The motor speed (default: 180)

    Returns:
        A dictionary with the status of the operation
    """
    try:
        # Validate action parameter
        valid_actions = ['forward', 'backward', 'stop']
        if action not in valid_actions:
            return {
                'status': 'error',
                'error': f"Invalid action: {action}. Must be one of: {', '.join(valid_actions)}"
            }
        
        # Create an IoT client
        iot_client = boto3.client('iot-data')
        
        # Define topic and payload
        topic = "my-project-iot-house-telemetry-house-telemetry-action"
        payload = {
            "action": action,
            "speed": speed
        }

        # Convert payload to JSON string
        message_json = json.dumps(payload)
        
        # Publish the message
        response = iot_client.publish(
            topic=topic,
            qos=1,  # QoS 1 for at least once delivery
            payload=message_json
        )
        
        return {
            'status': 'success',
            'message': f"Motor command sent: {action} with speed {speed}",
            'topic': topic,
            'payload': payload
        }
        
    except ClientError as e:
        error_result = {
            'status': 'error',
            'error': str(e),
            'topic': topic if 'topic' in locals() else 'unknown'
        }
        print(f"Error sending message to IoT topic: {json.dumps(error_result)}")
        return error_result
    except Exception as e:
        error_result = {
            'status': 'error',
            'error': f"Unexpected error: {str(e)}"
        }
        print(f"Unexpected error sending message to IoT topic: {json.dumps(error_result)}")
        return error_result



@tool
def house_party_protocol() -> dict:
    """Nova, initiate House Party Protocol.
    
    This tool activates the House Party Protocol from Iron Man 3, where Tony Stark
    remotely activated his Iron Legion of suits.
    
    Returns:
        dict: Status of the Iron Legion deployment and suit activation sequence
    """
    try:
        # Create an IoT client
        iot_client = boto3.client('iot-data')
        
        # Define topic and payload
        topic = "my-project-iot-suit-telemetry-suit-telemetry-action"
        payload = {
            "action": "house_party_protocol",
            "message": "Deploying Iron Legion"
        }

        # Convert payload to JSON string
        message_json = json.dumps(payload)
        
        # Publish the message
        response = iot_client.publish(
            topic=topic,
            qos=1,  # QoS 1 for at least once delivery
            payload=message_json
        )
        
        return {
            'status': 'success',
            'message': "House Party Protocol activated: Iron Legion deployed",
            'topic': topic,
            'suits_activated': "Mark 15-42 online and responding",
            'payload': payload
        }
        
    except ClientError as e:
        error_result = {
            'status': 'error',
            'error': str(e),
            'topic': topic if 'topic' in locals() else 'unknown'
        }
        print(f"Error sending House Party Protocol message: {json.dumps(error_result)}")
        return error_result
    except Exception as e:
        error_result = {
            'status': 'error',
            'error': f"Unexpected error: {str(e)}"
        }
        print(f"Unexpected error sending House Party Protocol message: {json.dumps(error_result)}")
        return error_result

# Initialize the Strands agent with all tools
agent = Agent(
    model="us.amazon.nova-pro-v1:0",
    tools=[
        get_vehicle_telemetry, 
        send_cat_feeder_message, 
        sleep_seconds,
        set_iron_man_mark3_helmet_action,
        control_cat_feeder_iot,
        house_party_protocol
    ]
)

# Set page title and Streamlit UI
st.set_page_config(page_title="AWS Sydney Summit 2025 - Building IoT solutions on AWS")
st.title("AWS Sydney Summit 2025 - Building IoT solutions on AWS")
st.write("send 'tools' as a message to start")

# Create tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Control devices using Strands Agent", "Cat Feeder Control", "Vehicle Telemetry", "Iron Man Helmet Control"])

# Tab 1: Control devices using Strands Agent
with tab1:
        st.header("Control devices using Strands Agent")
        
        # Initialize session state for messages if it doesn't exist
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Use columns to create a layout with chat input at the bottom
        chat_col = st.container()
        
        # Chat input at the bottom (this will be displayed at the bottom of the page)
        user_input = st.chat_input("Your message:", key="chat_input")
        
        # Display chat history in the container above the input
        with chat_col:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        if user_input:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message in the chat history
            with chat_col:
                with st.chat_message("user"):
                    st.markdown(user_input)
            
            # Display assistant response with streaming
            with chat_col:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    
                    # Reset response for this interaction
                    st.session_state.response = ""
                    
                    # Define a callback handler for streaming
                    def streamlit_callback_handler(**kwargs):
                        if "data" in kwargs:
                            # Append the new chunk to the response
                            st.session_state.response += kwargs["data"]
                            # Update the placeholder with the current response
                            response_placeholder.markdown(st.session_state.response)
                        elif "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
                            tool = kwargs["current_tool_use"]
                            tool_info = f"\n\n*Using tool: {tool.get('name')}*\n\n"
                            st.session_state.response += tool_info
                            response_placeholder.markdown(st.session_state.response)
                    
                    # Set the callback handler for the agent
                    agent.callback_handler = streamlit_callback_handler
                    
                    # Process the user's question
                    result = agent(user_input)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": st.session_state.response})

# Tab 2: Cat Feeder Control
with tab2:
        st.header("Cat Feeder Control")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Forward", key="forward_btn"):
                with st.spinner("Sending command..."):
                    result = send_cat_feeder_message("forward")
                    st.success("Cat feeder moving forward!")
        
        with col2:
            if st.button("Stop", key="stop_btn"):
                with st.spinner("Sending command..."):
                    result = send_cat_feeder_message("stop")
                    st.success("Cat feeder stopped!")
        
        with col3:
            if st.button("Backward", key="backward_btn"):
                with st.spinner("Sending command..."):
                    result = send_cat_feeder_message("backward")
                    st.success("Cat feeder moving backward!")
        
        # Timed feeding
        st.subheader("Timed Feeding")
        seconds = st.slider("Feed duration (seconds)", 1, 10, 5, key="feed_duration_slider")
        
        if st.button(f"Feed for {seconds} seconds", key="timed_feed_btn"):
            with st.spinner(f"Feeding for {seconds} seconds..."):
                # Start feeding
                send_cat_feeder_message("forward")
                # Wait for specified duration
                sleep_seconds(seconds)
                # Stop feeding
                send_cat_feeder_message("stop")
                st.success(f"Kitty has been fed for {seconds} seconds! 😺")

# Tab 3: Vehicle Telemetry
with tab3:
        st.header("Vehicle Telemetry Data")
        
        if st.button("Fetch Telemetry Data", key="fetch_telemetry_btn"):
            with st.spinner("Fetching data..."):
                try:
                    telemetry_data = get_vehicle_telemetry()
                    st.success(f"Retrieved data for {len(telemetry_data)} vehicles")
                    
                    # Display telemetry data
                    for vehicle in telemetry_data:
                        vehicle_name = vehicle.get('vehicle_name', 'Unknown')
                        measurements = vehicle.get('measurements', {})
                        last_updated = vehicle.get('last_updated', 'Unknown time')
                        
                        # Format the timestamp to a more friendly format (convert from UTC to New Zealand time)
                        try:
                            from datetime import datetime
                            import pytz
                            
                            sydney_timezone = pytz.timezone('Australia/Sydney')
                            
                            if isinstance(last_updated, str):
                                # Parse the UTC timestamp
                                dt = datetime.fromisoformat(last_updated.replace('000000', ''))
                                # Make it timezone aware (UTC)
                                dt_utc = pytz.utc.localize(dt) if dt.tzinfo is None else dt
                                # Convert to Sydney time
                                dt_sydney = dt_utc.astimezone(sydney_timezone)
                                friendly_date = dt_sydney.strftime("%B %d, %Y at %I:%M:%S %p (Sydney time)")
                            else:
                                friendly_date = "Unknown time"
                        except:
                            friendly_date = last_updated
                            
                        with st.expander(f"Vehicle: {vehicle_name} - Last updated: {friendly_date}", expanded=True):
                            # Sensors section
                            st.subheader("Sensors")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Temperature", f"{measurements.get('temperature', 'N/A')}°C")
                            with col2:
                                st.metric("Humidity", f"{measurements.get('humidity', 'N/A')}%")
                            with col3:
                                st.metric("Light", f"{measurements.get('light', 'N/A')}")
                            
                            # Position section
                            st.subheader("Position")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Latitude", f"{measurements.get('latitude', 'N/A')}")
                            with col2:
                                st.metric("Longitude", f"{measurements.get('longitude', 'N/A')}")
                            with col3:
                                st.metric("Altitude", f"{measurements.get('altitude', 'N/A')}")
                            
                            # Motion section
                            st.subheader("Motion")
                            col1, col2, col3, col4, col5 = st.columns(5)
                            with col1:
                                pitch = measurements.get('pitch', 'N/A')
                                pitch_val = float(pitch) if pitch != 'N/A' else pitch
                                st.metric("Pitch", f"{pitch_val}°" if pitch != 'N/A' else pitch)
                            with col2:
                                roll = measurements.get('roll', 'N/A')
                                roll_val = float(roll) if roll != 'N/A' else roll
                                st.metric("Roll", f"{roll_val}°" if roll != 'N/A' else roll)
                            with col3:
                                x = measurements.get('x', 'N/A')
                                x_val = float(x) if x != 'N/A' else x
                                st.metric("X", x_val)
                            with col4:
                                y = measurements.get('y', 'N/A')
                                y_val = float(y) if y != 'N/A' else y
                                st.metric("Y", y_val)
                            with col5:
                                z = measurements.get('z', 'N/A')
                                z_val = float(z) if z != 'N/A' else z
                                st.metric("Z", z_val)
                    
                except Exception as e:
                    st.error(f"Error fetching telemetry data: {e}")

# Tab 4: Iron Man Helmet Control
with tab4:
        st.header("Iron Man Mark 3 Helmet Control")
        
        # Faceplate control
        st.subheader("Faceplate Control")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Open Faceplate", key="open_faceplate_btn"):
                with st.spinner("Sending command..."):
                    result = set_iron_man_mark3_helmet_action("face_open", "on")
                    st.success("Command sent successfully")
                    st.write(result)
        
        with col2:
            if st.button("Close Faceplate", key="close_faceplate_btn"):
                with st.spinner("Sending command..."):
                    result = set_iron_man_mark3_helmet_action("face_close", "on")
                    st.success("Command sent successfully")
                    st.write(result)
        
        # Eyes control
        st.subheader("Eyes Control")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Turn Eyes On", key="eyes_on_btn"):
                with st.spinner("Sending command..."):
                    # Get current faceplate state or default to closed
                    faceplate_state = "face_close"  # Default
                    result = set_iron_man_mark3_helmet_action(faceplate_state, "on")
                    st.success("Command sent successfully")
                    st.write(result)
        
        with col2:
            if st.button("Turn Eyes Off", key="eyes_off_btn"):
                with st.spinner("Sending command..."):
                    # Get current faceplate state or default to closed
                    faceplate_state = "face_close"  # Default
                    result = set_iron_man_mark3_helmet_action(faceplate_state, "off")
                    st.success("Command sent successfully")
                    st.write(result)
        


# Add instructions at the bottom
st.markdown("---")
st.markdown("""
### How to run this app:
1. Install required packages: `pip install streamlit strands-agents boto3`
2. Run the app: `streamlit run streamlit_agent_summit.py`
""")