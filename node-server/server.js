const express = require('express');
const cors = require('cors');
const app = express();
const port = process.env.PORT || 3998;

app.use(cors());
app.use(express.json());

app.post('/api/seo-data', (req, res) => {
    const data = req.body;
    console.log('Received SEO data:', data);
    // Here you can add your own logic to handle the data
    // For example, save to a database
    
    res.json({ success: true, message: 'Data received successfully' });
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});
