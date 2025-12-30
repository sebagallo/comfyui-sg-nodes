import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

app.registerExtension({
    name: "SGNodes.SelectFileFromFolder",
    async nodeCreated(node, app) {
        if (node.comfyClass === "SelectFileFromFolder") {
            const folderWidget = node.widgets.find((w) => w.name === "folder_path");
            const extensionsWidget = node.widgets.find((w) => w.name === "extensions");
            const filterTypeWidget = node.widgets.find((w) => w.name === "filter_type");
            const filterTextWidget = node.widgets.find((w) => w.name === "filter_text");
            const fileWidget = node.widgets.find((w) => w.name === "file_name");

            if (folderWidget && fileWidget) {
                // Function to update the file list
                const updateFiles = async () => {
                    const folderPath = folderWidget.value;
                    if (!folderPath) return;

                    const extensions = extensionsWidget ? extensionsWidget.value : "";
                    const filterType = filterTypeWidget ? filterTypeWidget.value : "none";
                    const filterText = filterTextWidget ? filterTextWidget.value : "";

                    try {
                        const response = await api.fetchApi(`/sg-nodes/list_files?path=${encodeURIComponent(folderPath)}&extensions=${encodeURIComponent(extensions)}&filter_type=${encodeURIComponent(filterType)}&filter_text=${encodeURIComponent(filterText)}`);
                        if (response.status !== 200) {
                            console.error("Failed to fetch files:", response.statusText);
                            fileWidget.options.values = ["Error fetching files"];
                            return;
                        }
                        const data = await response.json();

                        // Update the file widget options
                        if (data.files && data.files.length > 0) {
                            fileWidget.options.values = data.files;
                        } else {
                            fileWidget.options.values = ["No files found"];
                        }

                        // If current value is not in new list, select first available (or keep current if possible)
                        if (!fileWidget.options.values.includes(fileWidget.value)) {
                            fileWidget.value = fileWidget.options.values[0] || fileWidget.value;
                        }

                        // Force redraw on the specific graph the node belongs to
                        const graph = node.graph || app.graph;
                        if (graph) {
                            graph.setDirtyCanvas(true, true);
                        }

                    } catch (error) {
                        console.error("Error updating files:", error);
                        fileWidget.options.values = ["Error"];
                    }
                };

                // Initial update
                setTimeout(updateFiles, 100);

                // Add callbacks for changes
                [folderWidget, extensionsWidget, filterTypeWidget, filterTextWidget].forEach(w => {
                    if (w) {
                        const originalCallback = w.callback;
                        w.callback = function () {
                            originalCallback?.apply(this, arguments);
                            updateFiles();
                        };
                    }
                });
            }
        }
    },
});
