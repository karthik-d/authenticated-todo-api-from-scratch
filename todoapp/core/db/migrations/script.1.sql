ALTER TABLE todo
ADD COLUMN due_by DATE;

ALTER TABLE todo 
ADD COLUMN status TEXT;

INSERT INTO 
	todo (task, due_by, status)
VALUES 
	("First todo", '2021-05-20', 'Not STarted'),
	("Last todo", '2021-05-22', 'In prOGress');