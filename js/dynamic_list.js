
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "SGNodes.MakeJsonList",
    async nodeCreated(node, app) {
        if (node.comfyClass === "MakeJsonList") {
            // Initialize with one input if none exist
            if (!node.inputs || node.inputs.length === 0) {
                node.addInput("input_1", "*");
            }

            const onConnectionsChange = node.onConnectionsChange;
            node.onConnectionsChange = function (type, index, connected, link_info) {
                onConnectionsChange?.apply(this, arguments);

                // Only care about input connections
                if (type !== 1) return; // 1 = input, 2 = output

                // Logic to maintain exactly one empty input at the end

                // 1. Check if the last input has a connection. If so, add a new one.
                const lastInputIndex = this.inputs.length - 1;
                const lastInput = this.inputs[lastInputIndex];

                if (lastInput.link !== null) {
                    const nextIndex = this.inputs.length + 1;
                    this.addInput(`input_${nextIndex}`, "*");
                }

                // 2. Check for trailing empty inputs. We want to remove extras, keeping one.
                // We assume inputs are sequential input_1, input_2...
                // We start checking from the end.

                let lastIndex = this.inputs.length - 1;

                // While we have more than 1 input, and the last one is empty...
                while (lastIndex > 0) {
                    const currentInput = this.inputs[lastIndex];
                    const prevInput = this.inputs[lastIndex - 1];

                    // If current is empty AND previous is empty, remove current.
                    // This ensures we don't have two empty inputs at the end.
                    if (currentInput.link === null && prevInput.link === null) {
                        this.removeInput(lastIndex);
                        lastIndex--;
                    } else {
                        break;
                    }
                }
            };
        }
    },
});
