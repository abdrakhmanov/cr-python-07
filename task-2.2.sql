/*
запрос, который выдаст 3 пользователей, 
с лучшими результатами по любому из предметов 
и отсортировать по результату по убыванию.
*/
SELECT
    u.name,
    r.result,
    s.name
FROM User u
INNER JOIN Result r ON r.user_id = u.id
LEFT JOIN "Subject" s ON s.id = r.subject
ORDER BY r.result DESC
LIMIT 3

/*
Получить пользователей, которые сдавали по 3 предмета 
и у которых результат больше 200 по всем предметам 
и отсортировать по результату по убыванию.
*/
-- синтаксис PostgreSQL
WITH users_3_200 AS (
    WITH users_200 AS (
        SELECT 
            u.id,
            r.subject
        FROM User u
        INNER JOIN Result r ON r.user_id = u.id
        WHERE r.result > 200
        GROUP BY u.id, r.subject
    )
    SELECT 
        u.id as user_id,
        count(1) 
    FROM users_200 u
    GROUP BY u.id
    HAVING count(1) = 3
)
SELECT
    u.name,
    r.result
FROM User u
INNER JOIN users_3_200 mu ON mu.user_id = u.id
INNER JOIN Result r ON r.user_id = u.id
ORDER BY r.result
