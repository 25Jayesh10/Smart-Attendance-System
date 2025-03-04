const express = require("express");
const multer = require("multer");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 8000;
const HOST = "192.168.150.98";

// Ensure "captured_images" directory exists
const imageDir = path.join(__dirname, "captured_images");
if (!fs.existsSync(imageDir)) {
    fs.mkdirSync(imageDir);
}

// Configure multer storage
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, imageDir); // Save files in "captured_images"
    },
    filename: (req, file, cb) => {
        cb(null, file.originalname); // Keep the original filename
    }
});

const upload = multer({ storage });

// Middleware to parse JSON form data with increased size limit
app.use(express.urlencoded({ extended: true, limit: "50mb" }));
app.use(express.json({ limit: "50mb" }));

// Image Upload Endpoint (Handles name and multiple files)
app.post("/add_person", upload.array("files", 10), (req, res) => {
    const name = req.body.name;
    
    if (!name) {
        return res.status(400).json({ message: "Name is required" });
    }

    if (!req.files || req.files.length === 0) {
        return res.status(400).json({ message: "No files uploaded" });
    }

    const uploadedFiles = req.files.map(file => file.filename);

    res.json({ 
        message: "Person added successfully", 
        name: name,
        files: uploadedFiles 
    });
});

// Default route
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "index.html"));
});

// Start server
app.listen(PORT, HOST, () => {
    console.log(`Server running at http://${HOST}:${PORT}`);
});
