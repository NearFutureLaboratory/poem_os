import json
import requests
from datetime import datetime
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play
import os

def create_poem(prompt):
    
    response = client.chat.completions.create(
      messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-4-turbo-preview",
    )
    
    result = response.choices[0].message.content.strip()
    return result

from datetime import datetime, timedelta

def find_next_or_current_weekday(weekday_name):
    # Map weekday names to their corresponding weekday numbers (Monday is 0, Sunday is 6)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    # Get the current date and its weekday number
    today = datetime.now()
    today_weekday = today.weekday()
    # Find the target weekday number
    target_weekday = days.index(weekday_name.lower())
    
    # Calculate the number of days to add to the current date to reach the target weekday
    days_until_target = (target_weekday - today_weekday + 7) % 7
    
    # If the target day is today, do not add any days
    if days_until_target == 0:
        next_target_date = today
    else:
        next_target_date = today + timedelta(days=days_until_target)
        
    return next_target_date  # Return the date

# Example usage: Find today's date or the next occurrence of a given weekday
# weekday_name = "Tuesday"  # Specify the target weekday name here
# next_weekday_date = find_next_or_current_weekday(weekday_name)
# print(f"The date for {weekday_name} is {next_weekday_date}.")

# Test with today's day name to return today's date
# current_day_name = datetime.now().strftime("%A")
# current_day_date = find_next_or_current_weekday(current_day_name)
# print(f"The date for {current_day_name} is {current_day_date}.")


# Example usage: Find the next occurrence of a given weekday
# weekday_name = "Wednesday"  # Specify the target weekday name here
# next_weekday_date = find_next_weekday(weekday_name)
# print(f"The next {weekday_name} will be on {next_weekday_date}.")


def get_all_voices():
    
    # An API key is defined here. You'd normally get this from the service you're accessing. It's a form of authentication.
    XI_API_KEY = elevenlabs_api_key

    # This is the URL for the API endpoint we'll be making a GET request to.
    url = "https://api.elevenlabs.io/v1/voices"

    # Here, headers for the HTTP request are being set up. 
    # Headers provide metadata about the request. In this case, we're specifying the content type and including our API key for authentication.
    headers = {
    "Accept": "application/json",
    "xi-api-key": elevenlabs_api_key,
    "Content-Type": "application/json"
    }

    # A GET request is sent to the API endpoint. The URL and the headers are passed into the request.
    response = requests.get(url, headers=headers)

    # The JSON response from the API is parsed using the built-in .json() method from the 'requests' library. 
    # This transforms the JSON data into a Python dictionary for further processing.
    data = response.json()
    with open('./voices.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)
    # A loop is created to iterate over each 'voice' in the 'voices' list from the parsed data. 
    # The 'voices' list consists of dictionaries, each representing a unique voice provided by the API.
    for voice in data['voices']:
    # For each 'voice', the 'name' and 'voice_id' are printed out. 
    # These keys in the voice dictionary contain values that provide information about the specific voice.
        print(f"{voice['name']}; {voice['voice_id']}")
    
    return data['voices']
# Load configuration, API keys, and prompts from the configuration file

with open("config.json", "r") as file:
    config = json.load(file)

openai_api_key = config["api_keys"]["openai"]
elevenlabs_api_key = config["api_keys"]["elevenlabs"]
data_root = config["data_root"]

with open("prompts.json", "r") as file:
    p = json.load(file)

prompts = p["prompts"]

# Configure your OpenAI API key
OpenAI.api_key = openai_api_key
client = OpenAI(
    api_key=OpenAI.api_key,
)

voices = get_all_voices()

# Determine today's day and select a prompt
#today = datetime.now().strftime("%A")
poem_day = config.get("day", datetime.now().strftime("%A"))

prompt = prompts[poem_day]["prompts"][0]# Choosing the first prompt for simplicity

poem = create_poem(prompt)
# # Generate a poem using OpenAI's API
# response = openai.Completion.create(
#   engine="gpt-4",  # Updated to use a newer model version
#   prompt=f"Write a short, pithy poem about {prompt}.",
#   max_tokens=100,
#   temperature=0.7
# )

print("Generated Poem:\n", poem)

CHUNK_SIZE = 1024
voice_id = prompts[poem_day]["voice_id"]

# Generate audio of the poem using ElevenLabs API
elevenlabs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
print(elevenlabs_url)

data = {
  "text": f"{poem}",
  "model_id": "eleven_monolingual_v1",
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.5
  }
}

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": elevenlabs_api_key
}

response = requests.post(elevenlabs_url, json=data, headers=headers)
if response.status_code != 200:
    print(f"Failed to generate audio. Status code: {response.status_code}")
else:
# Assuming `prompt` is the selected prompt for today
    poem_date = find_next_or_current_weekday(poem_day)
    poem_date_str = poem_date.strftime("%d%m%Y")
    #poem_date = poem_day.strftime("%d%m%Y")
    poem_day = poem_date.strftime("%A").lower()

    
    right_now = datetime.now().strftime("%H%M%S")
    prompt_index = prompts[poem_date.strftime("%A")]["prompts"].index(prompt)  # Assuming `prompts[today]` returns the list of prompts for today

    directory = f"{data_root}{poem_day}/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Format the filename
    filename_root = f"{poem_day}_{poem_date_str}_{right_now}_{prompt_index}"
    filename_audio = f"{poem_day}_{poem_date_str}_{right_now}_{prompt_index}.mp3"
    filename_path = f"{directory}/{filename_audio}"
    with open(filename_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    target_voice_id = voice_id
    voice_name = ''
    # Find the voice with the specified voice_id
    for voice in voices:
        try:
            print(voice)
            voice_id = voice['voice_id']
            print(voice_id)
            if voice_id == target_voice_id:
                voice_name = voice['name']
                print(voice_name)
                break
        except TypeError as e:
            print(f"Error: {e}, with element: {voice}")

    audio = AudioSegment.from_mp3(filename_path)
    duration_seconds = len(audio) / 1000.0  # Pydub uses milliseconds

    target_duration = 59  # Target duration in seconds
    timed_filename = filename_root
    if duration_seconds > target_duration:
        speed_up_factor = duration_seconds / target_duration
        # Speed up the audio
        audio = audio.speedup(playback_speed=speed_up_factor)
        # To save the modified audio
        timed_filename_path = f"{directory}/{filename_root}_59.mp3"
        timed_filename_actual = f"{filename_root}_59.mp3"
        audio.export(timed_filename_path, format="mp3")
        
        # Collect the data
    poem_data = {
        "day": poem_day,
        "prompt": prompt,
        "poem": poem,
        "voice_name": voice_name,
        "voice_id": voice_id,
        "date": poem_date_str,
        "audio": {"filename" : filename_audio, "duration" : duration_seconds, "timed_filename" : timed_filename}
    }

    # Determine the JSON filename (replace .mp3 with .json in the audio filename)
    json_filename = filename_audio.replace('.mp3', '.json')

    print(directory)
    # Save to JSON file
    with open(f"{directory}{json_filename}", 'w') as json_file:
        json.dump(poem_data, json_file, indent=4)

    print(f"Data saved to {json_filename}.")
    
    # audio = AudioSegment.from_mp3(file_path)
