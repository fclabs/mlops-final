SELECT 
	CAST("id" as INT) as user_id,
	"Occupation" as occupation ,
	TO_DATE("Active_Since", 'YY-MM-DD') as active_since
FROM {{ source( 'source_tables', 'usuarios_csv' ) }}