from flask import Blueprint, request, jsonify
import os
import subprocess
import re
import tempfile
import logging
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

@main_bp.route('/extract-subtitles', methods=['POST'])
def extract_subtitles():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    youtube_url = data['url']
    logger.info(f"Processing YouTube URL: {youtube_url}")
    
    # Create a temporary directory for this request
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Change to the temporary directory
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            logger.info(f"Changed to temporary directory: {temp_dir}")
            
            # Use the exact command that works for you
            cmd = f'yt-dlp --write-auto-sub --sub-lang en --sub-format srv3 --skip-download -o output "{youtube_url}"'
            
            logger.info(f"Running command: {cmd}")
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Log the command output
            logger.info(f"Command stdout: {process.stdout}")
            if process.stderr:
                logger.warning(f"Command stderr: {process.stderr}")
            
            if process.returncode != 0:
                logger.error(f"Command failed with exit code {process.returncode}")
                return jsonify({'error': 'Failed to download subtitles', 'details': process.stderr}), 500
            
            # List all files in the directory to find the subtitle file
            logger.info("Files in temporary directory:")
            files = os.listdir('.')
            for file in files:
                logger.info(f"  - {file} ({os.path.getsize(file)} bytes)")
            
            # Find the subtitle file (should be output.en.srv3)
            subtitle_files = glob.glob("*.srv3") + glob.glob("*.vtt") + glob.glob("*.srt")
            
            if not subtitle_files:
                logger.error("No subtitle files found")
                return jsonify({'error': 'No subtitles found for this video'}), 404
            
            subtitle_file = subtitle_files[0]
            logger.info(f"Found subtitle file: {subtitle_file}")
            
            # Read the subtitle file content
            with open(subtitle_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Process the subtitle content to extract clean text
            # For srv3 format (XML-based)
            if subtitle_file.endswith('.srv3'):
                # Remove XML tags
                content = re.sub(r'<[^>]+>', '', content)
            else:  # For VTT or SRT formats
                # Remove WEBVTT header and metadata
                content = re.sub(r'^WEBVTT.*?$', '', content, flags=re.MULTILINE)
                # Remove timestamps
                content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*?$', '', content, flags=re.MULTILINE)
            
            # Remove blank lines and clean up
            lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().isdigit()]
            cleaned_text = ' '.join(lines)
            
            # Remove multiple spaces
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            # Change back to the original directory
            os.chdir(original_dir)
            
            logger.info(f"Successfully extracted subtitles, length: {len(cleaned_text)} characters")
            return jsonify({'subtitles': cleaned_text})
            
        except Exception as e:
            # Make sure we change back to the original directory even if an error occurs
            if os.getcwd() != original_dir:
                os.chdir(original_dir)
            
            logger.exception(f"Error processing subtitles: {str(e)}")
            return jsonify({'error': str(e)}), 500


