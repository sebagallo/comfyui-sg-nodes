import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "SGNodes.SoundPlayer",
    async setup() {
        let audioCtx = null;

        api.addEventListener("sg-nodes:play_sound", ({ detail }) => {
            const { waveform, sample_rate, volume } = detail;
            if (!waveform || !sample_rate) return;

            try {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }

                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }

                const numChannels = waveform.length;
                const length = waveform[0].length;
                const buffer = audioCtx.createBuffer(numChannels, length, sample_rate);

                for (let channel = 0; channel < numChannels; channel++) {
                    const channelData = buffer.getChannelData(channel);
                    // waveform[channel] is a regular array, we need to copy it to the Float32Array
                    for (let i = 0; i < length; i++) {
                        channelData[i] = waveform[channel][i];
                    }
                }

                const source = audioCtx.createBufferSource();
                source.buffer = buffer;

                const gainNode = audioCtx.createGain();
                gainNode.gain.value = volume;

                source.connect(gainNode);
                gainNode.connect(audioCtx.destination);

                source.start();
            } catch (e) {
                console.error("Failed to play sound from waveform:", e);
            }
        });
    }
});
