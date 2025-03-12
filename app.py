from brain_of_the_doctor import encoded_image, analyze_user_problem
from voice_of_patient import record_audio, tanscribe
from voice_of_doctor import text_to_speech_auto
import os
import time
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath):
    speech_to_text_output = tanscribe(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
                                                 audio_filepath=audio_filepath,
                                                 model="whisper-large-v3")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_user_problem(query=system_prompt+speech_to_text_output, encoded_image=encoded_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_auto(inptext=doctor_response, output_file="final.mp3") 

    time.sleep(1)  # Ensure file is written before returning
    audio_path = os.path.abspath("final.mp3")  # Get absolute path
    print("Audio file generated:", audio_path)  # Debugging

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
       
    ],
    title="AI Doctor with Vision and Voice"
)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", "8080"))
    iface.launch(debug=True, server_name="0.0.0.0", server_port=PORT)
