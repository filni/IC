DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	titolo TEXT, 
	info TEXT
);

INSERT INTO posts (titolo, info) VALUES (
	'Esposizione in derivati',
	'Calcolo esposizione corta in derivati'
);


INSERT INTO posts (titolo, info) VALUES (
	'Global exposure Netting-Hedging',
	'Calcolo esposizione in derivati net and hedge'
);


INSERT INTO posts (titolo, info) VALUES (
	'Esposizione valutaria ex-EUR',
	'Calcolo esposizione valutaria ex-EUR'
);

