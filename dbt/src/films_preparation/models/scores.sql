SELECT 
	TO_DATE( "Date" , 'YY-MM-DD') as rating_date,
	CAST( "rating" as INT ) as rating,
	CAST( "user_id" as INT ) as user_id,
	CAST( "movie_id" as INT ) as movie_id
	
FROM {{ source( 'source_tables', 'scores_csv' ) }}