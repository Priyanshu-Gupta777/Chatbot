from brain_of_the_doctor import encoded_image, analyze_user_problem
from voice_of_patient import record_audio, tanscribe
from voice_of_doctor import text_to_speech_auto
import os
import time
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

system_prompt = """Act as a professional doctor. I know you are not, but this is for learning purposes. What's in this image? Do you find anything wrong with it medically?
                   If you make a differential, suggest some remedies for them. Do not add any numbers or special characters in your response. Your response should be in one
                   long paragraph. Also, always answer as if you are answering a real person. Do not say 'In the image I see' but say 'With what I see, I think you have ....'
                   Do not respond as an AI model in markdown, your answer should mimic that of an actual doctor, not an AI bot. Keep your answer concise (max 3 sentences). 
                   No preamble, start your answer right away, please. Use emojis accordingly to the problem, and if the problem is too serious, do not use any emoji. Do not use any special characters in the paragraph."""

def process_inputs(audio_filepath, image_filepath):
    # Transcribe audio input
    speech_to_text_output = tanscribe(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        model="whisper-large-v3"
    )

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_user_problem(
            query=system_prompt + speech_to_text_output,
            encoded_image=encoded_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        doctor_response = "No image provided for me to analyze."

    # Generate a unique file name for the audio output
    output_file = f"final_{int(time.time())}.mp3"
    voice_of_doctor = text_to_speech_auto(inptext=doctor_response, output_file=output_file)

    # Return the absolute path of the generated audio file
    audio_path = os.path.abspath(output_file)

    return speech_to_text_output, doctor_response, audio_path

# Ensure any old audio files are removed before generating a new one
def clear_old_files():
    for file in os.listdir():
        if file.startswith("final_") and file.endswith(".mp3"):
            os.remove(file)

# Clear old files at the start of the script
clear_old_files()

# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Patient Problem"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice")
    ],
    title="AI MedVoice"
)

if __name__ == "__main__":
    iface.launch(debug=True)
