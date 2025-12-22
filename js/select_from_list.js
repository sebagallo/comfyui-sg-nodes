import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "SGNodes.SelectFromList",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "SelectFromList") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);

                const listDataWidget = this.widgets.find((w) => w.name === "list_data");
                const inputModeWidget = this.widgets.find((w) => w.name === "input_mode");
                const delimiterWidget = this.widgets.find((w) => w.name === "delimiter");
                const selectedValueWidget = this.widgets.find((w) => w.name === "selected_value");

                if (listDataWidget && selectedValueWidget) {
                    const updateOptions = () => {
                        const listData = listDataWidget.value;
                        const inputMode = inputModeWidget ? inputModeWidget.value : "auto";
                        const delimiter = delimiterWidget ? delimiterWidget.value : "\\n";
                        let items = [];

                        if (listData) {
                            const parseJson = (data) => {
                                try {
                                    const parsed = JSON.parse(data);
                                    if (Array.isArray(parsed)) {
                                        return parsed.map(item => String(item));
                                    } else {
                                        return [String(parsed)];
                                    }
                                } catch (e) {
                                    return null;
                                }
                            };

                            const parseDelimited = (data, delim) => {
                                let d = delim;
                                if (d === "\\n") d = "\n";
                                else if (d === "\\t") d = "\t";
                                else if (d === "\\r") d = "\r";

                                if (!d) return [data];
                                return data.split(d)
                                    .map(part => part.trim())
                                    .filter(part => part.length > 0);
                            };

                            if (inputMode === "json") {
                                items = parseJson(list_data) || [];
                            } else if (inputMode === "delimiter") {
                                items = parseDelimited(listData, delimiter);
                            } else { // auto
                                items = parseJson(listData);
                                if (items === null) {
                                    items = parseDelimited(listData, delimiter);
                                }
                            }
                        }

                        if (items.length === 0) {
                            items = [""];
                        }

                        selectedValueWidget.options.values = items;

                        // Maintain selection if possible, otherwise reset to first
                        if (!items.includes(selectedValueWidget.value)) {
                            selectedValueWidget.value = items[0] || selectedValueWidget.value;
                        }

                        // Force redraw
                        app.graph.setDirtyCanvas(true, true);
                    };

                    // Initial update
                    setTimeout(updateOptions, 100);

                    // Add callback for changes
                    [listDataWidget, inputModeWidget, delimiterWidget].forEach(w => {
                        if (w) {
                            const originalCallback = w.callback;
                            w.callback = function () {
                                originalCallback?.apply(this, arguments);
                                updateOptions();
                            };
                        }
                    });
                }
            };
        }
    },
});
