"""
Audio Processing Namespace
"""
from flask_restx import Namespace
from saturn.resources import animate

# --- Create Namespace ---
process_audio_ns = Namespace(
    "Process Audio", description="Process provided audio files.")

# --- Setup API Endpoints ---
process_audio_ns.add_resource(
    animate.Animate, "/animate", endpoint="animate")