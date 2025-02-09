# Phish-Trap

# How to Run a Browser Extension and Load manifest.json

This guide will walk you through the steps to run your browser extension by loading the `manifest.json` file in a Chromium-based browser like Google Chrome or Microsoft Edge.

## Prerequisites
- Google Chrome or any Chromium-based browser installed.
- A folder containing your extension files (`manifest.json`, HTML, CSS, JavaScript, etc.).

## Steps to Load the Extension

### 1. Prepare Your Extension Files
Ensure all necessary files for your extension are placed in a single folder. This should include:
- `manifest.json`
- Any HTML, CSS, and JavaScript files required for the extension
- Any icons or images needed

### 2. Open Chrome Extensions Page
1. Open Google Chrome.
2. In the address bar, type `chrome://extensions/` and press **Enter**.

### 3. Enable Developer Mode
1. On the Extensions page, locate the **Developer mode** toggle in the top right corner.
2. Click the toggle to enable Developer mode.

### 4. Load the Unpacked Extension
1. Click on the **Load unpacked** button.
2. Navigate to the folder containing your extension files.
3. Select the folder and click **Open**.

### 5. Verify the Extension is Loaded
- Your extension should now appear in the list of installed extensions.
- If there are errors, review the error messages and check the `manifest.json` file.

### 6. Test Your Extension
- If your extension includes a browser action or page action, click the extension icon in the browser toolbar.
- If it modifies web pages, navigate to a relevant website and check for changes.
- Use the **Inspect views** link under the extension’s listing in `chrome://extensions/` for debugging.

### 7. Updating Your Extension
- If you make changes to your extension files, return to `chrome://extensions/`.
- Click **Reload** under your extension’s listing.

## Troubleshooting
- If the extension fails to load, open the **Developer Console** (F12) and check for errors.
- Make sure `manifest.json` is correctly formatted. Use a JSON validator if necessary.
- Check for missing files or incorrect file paths in `manifest.json`.

Now, your browser extension should be running successfully! 🎉
