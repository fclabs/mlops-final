SELECT 
	movie_id,  user_id, name, war, crime, drama, "action", comedy,
	horror, sci_fi, fantasy, musical, mystery, romance,
	western, "unknown", thriller, adventure, animation,
	film_noir, childrens, documentary, release_date,
    u.occupation, u.active_since,
    s.rating_date, s.rating
FROM {{ ref('peliculas') }} as p
INNER JOIN {{ ref('scores') }} as s USING(movie_id)
INNER JOIN {{ ref('usuarios') }} as u USING(user_id)