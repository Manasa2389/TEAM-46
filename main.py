<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Audio-to-Text & Speaker</title>
    <!-- Load Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Use Inter font family -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Custom CSS for the recording indicator */
        .recording-pulse {
            animation: pulse-red 1.5s infinite;
        }
        @keyframes pulse-red {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">

    <div id="app" class="w-full max-w-2xl bg-gray-800 rounded-xl shadow-2xl p-6 md:p-10">
        <h1 class="text-3xl font-bold mb-6 text-center text-indigo-400">Live Transcription & Text-to-Speech</h1>
        
        <!-- Status and Feedback Area -->
        <div class="mb-6 flex items-center justify-between p-3 bg-gray-700 rounded-lg">
            <span id="status-message" class="text-sm text-gray-300 font-medium">Ready to start listening.</span>
            <div id="recording-indicator" class="w-3 h-3 rounded-full bg-red-500 hidden"></div>
        </div>

        <!-- Transcription Output Area -->
        <div class="bg-gray-700 p-4 rounded-lg h-64 overflow-y-auto mb-6 border border-gray-600">
            <p id="final-transcript" class="text-lg leading-relaxed text-gray-100"></p>
            <span id="interim-transcript" class="text-sm text-gray-400 italic"></span>
        </div>

        <!-- Controls -->
        <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
            
            <button id="start-btn" 
                    class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 transform hover:scale-105 disabled:bg-gray-500"
                    onclick="toggleRecognition()">
                Start Listening
            </button>
            
            <button id="speak-btn" 
                    class="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg shadow-md transition duration-300 transform hover:scale-105 disabled:bg-gray-500"
                    onclick="speakText()">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 inline mr-2 -mt-0.5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 5.343a1 1 0 010 1.414 5 5 0 000 7.072 1 1 0 01-1.414 1.414 7 7 0 010-9.9 1 1 0 011.414 0zM16.07 3.929a1 1 0 010 1.414 7 7 0 000 9.9 1 1 0 01-1.414 1.414 9 9 0 010-12.728 1 1 0 011.414 0z" clip-rule="evenodd" />
                </svg>
                Read Text
            </button>
            
        </div>
        
        <p class="mt-4 text-xs text-center text-gray-500">
            Note: Speech recognition quality and language support vary by browser.
        </p>

        <!-- Custom Modal for Alerts (replacing alert()) -->
        <div id="modal-container" class="fixed inset-0 bg-black bg-opacity-50 hidden items-center justify-center p-4 z-50">
            <div class="bg-white p-6 rounded-lg shadow-2xl max-w-sm w-full">
                <h3 class="text-xl font-semibold mb-3 text-gray-800">Browser Warning </h3>
                <p id="modal-message" class="text-gray-600 mb-4"></p>
                <button onclick="document.getElementById('modal-container').classList.add('hidden')" 
                        class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-md w-full transition duration-150">
                    OK
                </button>
            </div>
        </div>
    </div>

    <script>
        // --- DOM Elements ---
        const finalTranscriptEl = document.getElementById('final-transcript');
        const interimTranscriptEl = document.getElementById('interim-transcript');
        const startBtn = document.getElementById('start-btn');
        const speakBtn = document.getElementById('speak-btn');
        const statusMessageEl = document.getElementById('status-message');
        const recordingIndicator = document.getElementById('recording-indicator');
        const modalContainer = document.getElementById('modal-container');
        const modalMessageEl = document.getElementById('modal-message');

        // --- Speech Recognition Setup ---
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognition = null;
        let isListening = false;
        let manualStop = false; // Flag to differentiate between user-stop and automatic stop (like 'no-speech')
        
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = true; // Keep listening after a pause
            recognition.interimResults = true; // Show results as they are being spoken
            recognition.lang = 'en-US'; // Set default language
            
            statusMessageEl.textContent = 'Speech Recognition Initialized.';
        } else {
            // Show a warning if the API is not supported
            showModal('Your browser does not fully support the Web Speech API (Speech Recognition). Please try Chrome or Edge.');
            startBtn.disabled = true;
            statusMessageEl.textContent = 'Speech Recognition Not Supported.';
        }

        // --- Utility Functions ---

        /**
         * Custom modal function to replace alert()
         * @param {string} message 
         */
        function showModal(message) {
            modalMessageEl.textContent = message;
            modalContainer.classList.remove('hidden');
            modalContainer.classList.add('flex');
        }

        function updateUI(listening) {
            isListening = listening;
            startBtn.textContent = isListening ? 'Stop Listening' : 'Start Listening';
            startBtn.classList.toggle('bg-red-600', isListening);
            startBtn.classList.toggle('bg-indigo-600', !isListening);
            recordingIndicator.classList.toggle('hidden', !isListening);
            recordingIndicator.classList.toggle('recording-pulse', isListening);
            statusMessageEl.textContent = isListening ? 'Listening... Speak clearly into your microphone.' : 'Listening stopped.';
        }

        // --- Recognition Event Handlers ---

        if (recognition) {
            recognition.onresult = (event) => {
                let interimTranscript = '';
                let newFinalHtml = ''; // Accumulator for final results with line breaks

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    const transcript = event.results[i][0].transcript;
                    
                    if (event.results[i].isFinal) {
                        // For final results, format the text and add a line break for readability
                        let formattedText = transcript.trim();
                        
                        // Add a period only if the final character isn't already a common terminal punctuation
                        if (!/[.!?]$/.test(formattedText)) {
                            formattedText += '.';
                        }
                        
                        // Use innerHTML to inject the text and the <br> tag
                        newFinalHtml += formattedText + '<br>';

                    } else {
                        interimTranscript += transcript;
                    }
                }
                
                // Append new final text (with line breaks) to the main display
                if (newFinalHtml) {
                    finalTranscriptEl.innerHTML += newFinalHtml;
                    // Scroll the parent container to the bottom
                    finalTranscriptEl.parentElement.scrollTop = finalTranscriptEl.parentElement.scrollHeight;
                }
                
                // Update interim display
                interimTranscriptEl.textContent = interimTranscript;
            };

            recognition.onerror = (event) => {
                console.error('Speech Recognition Error:', event.error);
                let errorMessage = `Recognition Error: ${event.error}`;
                
                if (event.error === 'not-allowed') {
                    errorMessage = "Microphone access denied. Please enable it for this site.";
                    showModal(errorMessage);
                } else if (event.error === 'no-speech') {
                    // This error causes an 'onend' event, where the restart logic resides.
                    errorMessage = "No speech detected. Auto-restarting if you are actively listening...";
                }

                statusMessageEl.textContent = errorMessage;
            };

            recognition.onend = () => {
                // Check if the stop was unexpected (not initiated by the user)
                if (manualStop) {
                    // This was a manual stop. Finalize UI.
                    updateUI(false);
                    manualStop = false; // Reset the flag
                    statusMessageEl.textContent = 'Listening stopped by user.';
                } else if (isListening) {
                    // This was an automatic stop (e.g., due to 'no-speech' or timeout). We restart.
                    statusMessageEl.textContent = 'Auto-restarting recognition...';
                    
                    // Use a small delay to prevent rapid failed restarts
                    setTimeout(() => {
                        try {
                            recognition.start();
                        } catch (e) {
                            console.error('Failed to restart recognition:', e);
                            // If restart fails, then officially stop
                            updateUI(false); 
                            showModal("Recognition failed to restart automatically. Please press 'Start Listening' manually.");
                        }
                    }, 500);
                } else {
                    // Clean up UI state if needed (e.g., if it was already stopped)
                    updateUI(false);
                }
            };

            recognition.onstart = () => {
                updateUI(true);
            };
        }

        // --- Recognition Control ---

        function toggleRecognition() {
            if (!recognition) return;

            if (isListening) {
                manualStop = true; // Signal intent to stop
                recognition.stop();
                // Wait for recognition.onend to fire and update the UI
            } else {
                manualStop = false; // Clear flag on start
                // Clear the display before starting a new session
                finalTranscriptEl.textContent = '';
                interimTranscriptEl.textContent = '';
                try {
                    recognition.start();
                } catch (e) {
                    // Catch error if recognition is already active (shouldn't happen with proper logic, but good for robustness)
                    console.warn("Recognition already started or failed to start:", e);
                    showModal("Failed to start listening. Check your microphone and try again.");
                    updateUI(false);
                }
            }
        }
        
        // --- Text-to-Speech (Speaker) Setup ---
        
        const synth = window.speechSynthesis;
        if (!synth) {
            speakBtn.disabled = true;
            console.warn("Speech Synthesis Not Supported in this browser.");
            speakBtn.textContent = 'Speaker Not Supported';
        }

        function speakText() {
            if (!synth || synth.speaking) {
                if (synth && synth.speaking) {
                    showModal("The speaker is already reading. Please wait for the current sentence to finish.");
                }
                return;
            }

            // IMPORTANT: Use textContent to get only the visible text for reading, stripping the <br> tags
            const textToSpeak = finalTranscriptEl.textContent.trim();

            if (textToSpeak.length === 0) {
                showModal("Please speak into the microphone first to generate text before trying to read it.");
                return;
            }

            // A typical maximum length is around 32,000 characters, but we'll cap it lower for reliability
            const maxLen = 500; 
            const utteranceText = textToSpeak.length > maxLen ? textToSpeak.substring(0, maxLen) + " (Text truncated for reliable reading)" : textToSpeak;

            const utterance = new SpeechSynthesisUtterance(utteranceText);
            utterance.lang = 'en-US'; // Use the same language as recognition
            
            // Optionally, you can set voice, pitch, and rate
            // utterance.rate = 1; 
            // utterance.pitch = 1;

            utterance.onstart = () => {
                speakBtn.disabled = true;
                speakBtn.textContent = 'Reading...';
            };

            utterance.onend = () => {
                speakBtn.disabled = false;
                speakBtn.textContent = 'Read Text';
            };

            utterance.onerror = (event) => {
                console.error('SpeechSynthesis Utterance Error:', event.error);
                speakBtn.disabled = false;
                speakBtn.textContent = 'Read Text';
                showModal(`An error occurred while reading the text: ${event.error}`);
            };

            synth.speak(utterance);
        }
    </script>
</body>
</html>
