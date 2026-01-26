import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "SGNodes.SoundPlayer",
    async setup() {
        api.addEventListener("sg-nodes:play_sound", ({ detail }) => {
            const { sound_name, volume } = detail;
            if (!sound_name) return;

            const url = api.api_base + `/sg-nodes/get_sound?name=${encodeURIComponent(sound_name)}`;
            const audio = new Audio(url);
            audio.volume = volume;
            audio.play().catch(e => {
                console.error("Failed to play sound:", e);
                // Note: Most browsers require user interaction before playing sound.
                // However, since this is triggered by a node execution (which is usually user-initiated),
                // it might work if the session is active.
            });
        });
    }
});
