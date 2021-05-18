DROP TABLE IF EXISTS todo;

CREATE TABLE todo (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	task TEXT
);

INSERT INTO 
	todo (task)
VALUES 
	("First todo"),
	("Last todo");