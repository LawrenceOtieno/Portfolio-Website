const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql');

const app = express();
const port = 3000;

// MySQL database connection
const connection = mysql.createConnection({
    host: 'your_mysql_host',
    user: 'your_mysql_user',
    password: 'your_mysql_password',
    database: 'your_database_name'
});

connection.connect();

// Middleware to parse form data
app.use(bodyParser.urlencoded({ extended: true }));

// Route to handle form submissions
app.post('/submit_contact', (req, res) => {
    const { name, email, phone, message } = req.body;

    const sql = 'INSERT INTO ContactDetails (name, email, phone, message) VALUES (?, ?, ?, ?)';
    connection.query(sql, [name, email, phone, message], (err, result) => {
        if (err) throw err;
        console.log('Record inserted:', result);
        res.send('Form submitted successfully!');
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
