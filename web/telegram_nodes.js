// ComfyUI Web UI for Telegram Bot Nodes

import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

// Register the Telegram Listener node
app.registerExtension({
    name: "telegram.TelegramListener",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "TelegramListener") {
            // Add custom styling or behavior if needed
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Add a status indicator
                this.addWidget("text", "status", "Ready", () => {}, {
                    serialize: false
                });
                
                // Color the node to indicate it's a Telegram node
                this.color = "#2196F3"; // Telegram blue
                this.bgcolor = "#1976D2";
                
                return r;
            };
        }
    }
});

// Register the Save to Telegram node
app.registerExtension({
    name: "telegram.SaveToTelegram",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "SaveToTelegram") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Add a status indicator
                this.addWidget("text", "status", "Ready", () => {}, {
                    serialize: false
                });
                
                // Color the node to indicate it's a Telegram node
                this.color = "#4CAF50"; // Green for send
                this.bgcolor = "#388E3C";
                
                return r;
            };
        }
    }
});

// Add some utility functions for better UX
app.registerExtension({
    name: "telegram.utils",
    async setup() {
        // Add telegram category to the node menu
        const origGetNodeMenuOptions = app.getNodeMenuOptions;
        app.getNodeMenuOptions = function(node) {
            const options = origGetNodeMenuOptions.apply(this, arguments);
            
            if (node.type === "TelegramListener" || node.type === "SaveToTelegram") {
                options.push({
                    content: "View Telegram Docs",
                    callback: () => {
                        window.open("https://core.telegram.org/bots/api", "_blank");
                    }
                });
            }
            
            return options;
        };
    }
});
