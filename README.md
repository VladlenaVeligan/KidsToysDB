# KidsToysDB
Task №1 Write down MySQL requests to create `toys`, `games` and `toys_games` tables
(`toys_games` is a relation table to connect `toys` and `games`) containing all
information from above &quot;toys&quot; API (host kids.example.com).

Task №2 Write down MySQL request to create `toys_repair` table to contain information on
toys being repaired. Table should contain fields `id` (MySQL internal primary key),
`toy_id` (toy `id`), `issue_description` (here you will find the `note` field values for each
`toy_id` field (one `toy_id` contains many `note`)).

Task №3 Create configuration for the script to retrieve the following: see points a-c below.
  a. All available data about games for the last week (current date included).
     Should fill in table from Task 1.
     
  b.All available data about toys for the last week (current date included). Should
    fill in tables from Task 1.
    
  c.All data about toys containing &quot;repair&quot; or &quot;break&quot; or &quot;broken&quot; substring in
    `note` field. Should fill in table from Task 2.
    
Task №4 Create MySQL request to get all available data about toys and their status updates
during last year: `toy_id`, `toys.name`, `status`, `status_updated`, `games.name`,
`date`, `note`.

Task №5 Create MySQL request to get list of toys never been repaired.
