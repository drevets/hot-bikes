station_list = ['2112 W Peterson Ave', '63rd St Beach', '900 W Harrison St', 'Aberdeen St & Jackson Blvd', 'Aberdeen St & Monroe St', 'Aberdeen St & Randolph St', 'Ada St & Washington Blvd', 'Adler Planetarium', 'Albany Ave & 26th St', 'Albany Ave & Bloomingdale Ave', 'Albany Ave & Montrose Ave', 'Artesian Ave & Hubbard St', 'Ashland Ave & 13th St', 'Ashland Ave & 21st St', 'Ashland Ave & 50th St', 'Ashland Ave & 63rd St', 'Ashland Ave & 66th St', 'Ashland Ave & 69th St', 'Ashland Ave & Archer Ave', 'Ashland Ave & Augusta Blvd', 'Ashland Ave & Belle Plaine Ave', 'Ashland Ave & Blackhawk St', 'Ashland Ave & Chicago Ave', 'Ashland Ave & Division St', 'Ashland Ave & Garfield Blvd', 'Ashland Ave & Grace St', 'Ashland Ave & Grand Ave', 'Ashland Ave & Harrison St', 'Ashland Ave & Lake St (Temp)', 'Ashland Ave & McDowell Ave', 'Ashland Ave & Pershing Rd', 'Ashland Ave & Wellington Ave', 'Ashland Ave & Wrightwood Ave', 'Austin Blvd & Chicago Ave', 'Austin Blvd & Lake St', 'Austin Blvd & Madison St', 'Avers Ave & Belmont Ave', 'Avondale Ave & Irving Park Rd', 'Bennett Ave & 79th St', 'Benson Ave & Church St', 'Bernard St & Elston Ave', 'Bissell St & Armitage Ave', 'Blackstone Ave & Hyde Park Blvd', 'Blue Island Ave & 18th St', 'Bosworth Ave & Howard St', 'Broadway & Argyle St', 'Broadway & Barry Ave', 'Broadway & Belmont Ave', 'Broadway & Berwyn Ave', 'Broadway & Cornelia Ave', 'Broadway & Granville Ave', 'Broadway & Ridge Ave', 'Broadway & Sheridan Rd', 'Broadway & Thorndale Ave', 'Broadway & Waveland Ave', 'Broadway & Wilson Ave', 'Buckingham Fountain', 'Budlong Woods Library', 'Burling St (Halsted) & Diversey Pkwy (Temp)', 'Burnham Harbor', 'California Ave & 21st St', 'California Ave & 23rd Pl', 'California Ave & 26th St', 'California Ave & Altgeld St', 'California Ave & Byron St', 'California Ave & Cortez St', 'California Ave & Division St', 'California Ave & Fletcher St', 'California Ave & Francis Pl', 'California Ave & Lake St', 'California Ave & Milwaukee Ave', 'California Ave & Montrose Ave', 'California Ave & North Ave', 'Calumet Ave & 18th St', 'Calumet Ave & 21st St', 'Calumet Ave & 33rd St', 'Calumet Ave & 35th St', 'Calumet Ave & 51st St', 'Calumet Ave & 71st St', 'Campbell Ave & Fullerton Ave', 'Campbell Ave & Montrose Ave', 'Campbell Ave & North Ave', 'Canal St & Adams St', 'Canal St & Harrison St', 'Canal St & Jackson Blvd', 'Canal St & Madison St', 'Canal St & Monroe St (*)', 'Canal St & Taylor St', 'Cannon Dr & Fullerton Ave', 'Carpenter St & 63rd St', 'Carpenter St & Huron St', 'Central Ave & Chicago Ave', 'Central Ave & Harrison St', 'Central Ave & Lake St', 'Central Ave & Madison St', 'Central Park Ave & 24th St', 'Central Park Ave & Bloomingdale Ave', 'Central Park Ave & Elbridge Ave', 'Central Park Ave & North Ave', 'Central Park Ave & Ogden Ave', 'Central Park Blvd & 5th Ave', 'Central St & Girard Ave', 'Central St Metra', 'Chicago Ave & Dempster St', 'Chicago Ave & Sheridan Rd', 'Chicago Ave & Washington St', 'Christiana Ave & Lawrence Ave', 'Cicero Ave & Flournoy St', 'Cicero Ave & Lake St', 'Cicero Ave & Quincy St', 'Cityfront Plaza Dr & Pioneer Ct', 'Claremont Ave & Hirsch St', 'Clarendon Ave & Gordon Ter', 'Clarendon Ave & Junior Ter', 'Clarendon Ave & Leland Ave', 'Clark St & 9th St (AMLI)', 'Clark St & Armitage Ave', 'Clark St & Berwyn Ave', 'Clark St & Bryn Mawr Ave', 'Clark St & Chicago Ave', 'Clark St & Columbia Ave', 'Clark St & Congress Pkwy', 'Clark St & Drummond Pl', 'Clark St & Elm St', 'Clark St & Elmdale Ave', 'Clark St & Grace St', 'Clark St & Jarvis Ave', 'Clark St & Lake St', 'Clark St & Leland Ave', 'Clark St & Lincoln Ave', 'Clark St & Lunt Ave', 'Clark St & Montrose Ave', 'Clark St & Newport St', 'Clark St & North Ave', 'Clark St & Randolph St', 'Clark St & Schiller St', 'Clark St & Schreiber Ave', 'Clark St & Touhy Ave', 'Clark St & Wellington Ave', 'Clark St & Winnemac Ave (Temp)', 'Clark St & Wrightwood Ave', 'Clifton Ave & Armitage Ave', 'Clinton St & 18th St', 'Clinton St & Jackson Blvd (*)', 'Clinton St & Lake St', 'Clinton St & Madison St', 'Clinton St & Polk St (*)', 'Clinton St & Roosevelt Rd', 'Clinton St & Tilden St', 'Clinton St & Washington Blvd', 'Clybourn Ave & Division St', 'Columbus Dr & Randolph St', 'Commercial Ave & 83rd St', 'Conservatory Dr & Lake St', 'Cornell Ave & Hyde Park Blvd', 'Cottage Grove Ave & 43rd St', 'Cottage Grove Ave & 47th St', 'Cottage Grove Ave & 51st St', 'Cottage Grove Ave & 63rd St', 'Cottage Grove Ave & 67th St', 'Cottage Grove Ave & 71st St', 'Cottage Grove Ave & 78th St', 'Cottage Grove Ave & 83rd St', 'Cottage Grove Ave & Oakwood Blvd', 'Daley Center Plaza', 'Damen Ave & 51st St', 'Damen Ave & 59th St', 'Damen Ave & Charleston St', 'Damen Ave & Chicago Ave', 'Damen Ave & Clybourn Ave', 'Damen Ave & Cortland St', 'Damen Ave & Coulter St', 'Damen Ave & Cullerton St', 'Damen Ave & Division St', 'Damen Ave & Foster Ave', 'Damen Ave & Grand Ave', 'Damen Ave & Leland Ave', 'Damen Ave & Madison St', 'Damen Ave & Melrose Ave', 'Damen Ave & Pershing Rd', 'Damen Ave & Pierce Ave', 'Damen Ave & Sunnyside Ave', 'Damen Ave & Thomas St (Augusta Blvd)', 'Damen Ave & Walnut (Lake) St (*)', 'Damen Ave & Wellington Ave', 'Dayton St & North Ave', 'Dearborn Pkwy & Delaware Pl', 'Dearborn St & Adams St', 'Dearborn St & Erie St', 'Dearborn St & Monroe St', 'Dearborn St & Van Buren St (*)', 'Delano Ct & Roosevelt Rd', 'Desplaines St & Jackson Blvd', 'Desplaines St & Kinzie St', 'Desplaines St & Randolph St', 'Dodge Ave & Church St', 'Dodge Ave & Mulford St', 'Dorchester Ave & 49th St', 'Dorchester Ave & 63rd St', 'Drake Ave & Addison St', 'Drake Ave & Fullerton Ave', 'Drake Ave & Montrose Ave', 'DuSable Museum', 'Dusable Harbor', 'Eastlake Ter & Rogers Ave', 'Eberhart (Vernon) Ave & 79th St', 'Eberhart Ave & 61st St', 'Eckhart Park', 'Eggleston Ave & 69th St (*)', 'Elizabeth St & 47th St', 'Elizabeth St & 59th St', 'Ellis Ave & 53rd St', 'Ellis Ave & 55th St', 'Ellis Ave & 58th St', 'Ellis Ave & 60th St', 'Ellis Ave & 83rd St', 'Elmwood Ave & Austin St', 'Elston Ave & Wabansia Ave', 'Emerald Ave & 28th St', 'Emerald Ave & 31st St', 'Evans Ave & 75th St', 'Evanston Civic Center', 'Exchange Ave & 79th St', 'Fairbanks Ct & Grand Ave', 'Fairbanks St & Superior St (*)', 'Fairfield Ave & Roosevelt Rd', 'Federal St & Polk St', 'Field Blvd & South Water St', 'Field Museum', 'Financial Pl & Congress Pkwy (Temp)', 'Fort Dearborn Dr & 31st St', 'Francisco Ave & Foster Ave', 'Franklin St & Chicago Ave', 'Franklin St & Jackson Blvd', 'Franklin St & Lake St', 'Franklin St & Monroe St', 'Franklin St & Quincy St', 'Glenwood Ave & Morse Ave', 'Glenwood Ave & Touhy Ave', 'Green St & Madison St', 'Green St & Randolph St', 'Greenview Ave & Diversey Pkwy', 'Greenview Ave & Fullerton Ave', 'Greenview Ave & Jarvis Ave', 'Greenwood Ave & 47th St', 'Greenwood Ave & 79th St', 'Halsted St & 18th St', 'Halsted St & 21st St', 'Halsted St & 35th St (*)', 'Halsted St & 37th St', 'Halsted St & 47th Pl', 'Halsted St & 51st St', 'Halsted St & 56th St', 'Halsted St & 59th St', 'Halsted St & 63rd St', 'Halsted St & 69th St', 'Halsted St & Archer Ave', 'Halsted St & Clybourn Ave (*)', 'Halsted St & Dickens Ave', 'Halsted St & Maxwell St', 'Halsted St & North Branch St', 'Halsted St & Polk St', 'Halsted St & Roosevelt Rd', 'Halsted St & Roscoe St', 'Halsted St & Willow St', 'Halsted St & Wrightwood Ave', 'Harper Ave & 59th St', 'Hermitage Ave & Polk St', 'Honore St & Division St', 'Hoyne Ave & 47th St', 'Hoyne Ave & Balmoral Ave', 'Humboldt Blvd & Armitage Ave', 'Indiana Ave & 26th St', 'Indiana Ave & 31st St', 'Indiana Ave & 40th St', 'Indiana Ave & Roosevelt Rd', 'Jefferson St & Monroe St', 'Jeffery Blvd & 67th St', 'Jeffery Blvd & 71st St', 'Jeffery Blvd & 76th St', 'Karlov Ave & Madison St', 'Kedzie Ave & 21st St', 'Kedzie Ave & 24th St', 'Kedzie Ave & Bryn Mawr Ave', 'Kedzie Ave & Chicago Ave', 'Kedzie Ave & Foster Ave', 'Kedzie Ave & Harrison St', 'Kedzie Ave & Lake St', 'Kedzie Ave & Leland Ave', 'Kedzie Ave & Milwaukee Ave', 'Kedzie Ave & Palmer Ct', 'Kedzie Ave & Roosevelt Rd', 'Kenton Ave & Madison St', 'Keystone Ave & Fullerton Ave', 'Keystone Ave & Montrose Ave', 'Kilbourn Ave & Irving Park Rd', 'Kilbourn Ave & Milwaukee Ave', 'Kildare Ave & Montrose Ave', 'Kimball Ave & Belmont Ave', 'Kimbark Ave & 53rd St', 'Kingsbury St & Erie St', 'Kingsbury St & Kinzie St', 'Knox Ave & Montrose Ave', 'Kosciuszko Park', 'Kostner Ave & Adams St', 'Kostner Ave & Lake St', 'LaSalle Dr & Huron St (*)', 'LaSalle St & Adams St', 'LaSalle St & Illinois St', 'LaSalle St & Jackson Blvd', 'LaSalle St & Washington St', 'Lake Park Ave & 35th St', 'Lake Park Ave & 47th St', 'Lake Park Ave & 53rd St', 'Lake Park Ave & 56th St', 'Lake Shore Dr & Belmont Ave', 'Lake Shore Dr & Diversey Pkwy', 'Lake Shore Dr & Monroe St', 'Lake Shore Dr & North Blvd', 'Lake Shore Dr & Ohio St', 'Lake Shore Dr & Wellington Ave', 'Lakefront Trail & Bryn Mawr Ave', 'Lakefront Trail & Wilson Ave', 'Lakeview Ave & Fullerton Pkwy', 'Laramie Ave & Gladys Ave', 'Laramie Ave & Kinzie St', 'Laramie Ave & Madison St', 'Larrabee St & Armitage Ave', 'Larrabee St & Division St', 'Larrabee St & Kingsbury St', 'Larrabee St & Menomonee St', 'Larrabee St & North Ave', 'Larrabee St & Oak St', 'Larrabee St & Webster Ave', 'Leavitt St & Addison St', 'Leavitt St & Archer Ave', 'Leavitt St & Armitage Ave', 'Leavitt St & Chicago Ave', 'Leavitt St & Division St (*)', 'Leavitt St & Lawrence Ave', 'Leavitt St & North Ave', 'Lincoln Ave & Addison St', 'Lincoln Ave & Belle Plaine Ave', 'Lincoln Ave & Belmont Ave', 'Lincoln Ave & Diversey Pkwy', 'Lincoln Ave & Fullerton Ave', 'Lincoln Ave & Roscoe St', 'Lincoln Ave & Sunnyside Ave', 'Lincoln Ave & Waveland Ave', 'Lincoln Ave & Winona St', 'Lincolnwood Dr & Central St', 'Logan Blvd & Elston Ave', 'Loomis St & Archer Ave', 'Loomis St & Jackson Blvd', 'Loomis St & Lexington St', 'Loomis St & Taylor St (*)', 'MLK Jr Dr & 29th St', 'MLK Jr Dr & 47th St', 'MLK Jr Dr & 56th St (*)', 'MLK Jr Dr & 63rd St', 'MLK Jr Dr & 83rd St', 'MLK Jr Dr & Pershing Rd', 'Malcolm X College', 'Manor Ave & Leland Ave', 'Maplewood Ave & Peterson Ave', 'Marine Dr & Ainslie St', 'Marshfield Ave & 44th St', 'Marshfield Ave & 59th St', 'Marshfield Ave & Cortland St', 'May St & 69th St', 'May St & Cullerton St', 'May St & Taylor St', 'McClurg Ct & Erie St', 'McClurg Ct & Illinois St', 'McCormick Place', 'Michigan Ave & 14th St', 'Michigan Ave & 18th St', 'Michigan Ave & 71st St', 'Michigan Ave & 8th St', 'Michigan Ave & Congress Pkwy', 'Michigan Ave & Jackson Blvd', 'Michigan Ave & Lake St', 'Michigan Ave & Madison St', 'Michigan Ave & Oak St', 'Michigan Ave & Pearson St', 'Michigan Ave & Washington St', 'Mies van der Rohe Way & Chestnut St', 'Mies van der Rohe Way & Chicago Ave', 'Millard Ave & 26th St', 'Millennium Park', 'Milwaukee Ave & Cuyler Ave', 'Milwaukee Ave & Grand Ave', 'Milwaukee Ave & Rockwell St', 'Milwaukee Ave & Wabansia Ave', 'Monticello Ave & Irving Park Rd', 'Montrose Harbor', 'Morgan Ave & 14th Pl', 'Morgan St & 18th St', 'Morgan St & 31st St', 'Morgan St & Lake St', 'Morgan St & Pershing Rd', 'Morgan St & Polk St', 'Museum of Science and Industry', 'Noble St & Milwaukee Ave', 'Normal Ave & 72nd St', 'Normal Ave & Archer Ave', 'Oakley Ave & Irving Park Rd', 'Oakley Ave & Touhy Ave', 'Ogden Ave & Chicago Ave', 'Ogden Ave & Congress Pkwy', 'Ogden Ave & Race Ave', 'Ogden Ave & Roosevelt Rd', 'Orleans St & Chestnut St (NEXT Apts)', 'Orleans St & Elm St (*)', 'Orleans St & Hubbard St (*)', 'Orleans St & Merchandise Mart Plaza', 'Paulina Ave & North Ave', 'Paulina St & 18th St', 'Paulina St & Howard St', 'Paulina St & Montrose Ave', 'Peoria St & Jackson Blvd', 'Perry Ave & 69th St', 'Phillips Ave & 79th St', 'Phillips Ave & 83rd St', 'Pine Grove Ave & Irving Park Rd', 'Pine Grove Ave & Waveland Ave', 'Prairie Ave & 43rd St', 'Prairie Ave & Garfield Blvd', 'Princeton Ave & 47th St', 'Princeton Ave & Garfield Blvd', 'Pulaski Rd & Congress Pkwy', 'Pulaski Rd & Eddy St (Temp)', 'Pulaski Rd & Lake St', 'Racine Ave & 13th St', 'Racine Ave & 15th St', 'Racine Ave & 18th St', 'Racine Ave & 35th St', 'Racine Ave & 61st St', 'Racine Ave & 65th St', 'Racine Ave & Belmont Ave', 'Racine Ave & Congress Pkwy', 'Racine Ave & Fullerton Ave', 'Racine Ave & Garfield Blvd', 'Racine Ave & Randolph St', 'Racine Ave & Washington Blvd (*)', 'Racine Ave & Wrightwood Ave', 'Racine Ave (May St) & Fulton St', 'Rainbow Beach', 'Ravenswood Ave & Berteau Ave', 'Ravenswood Ave & Irving Park Rd', 'Ravenswood Ave & Lawrence Ave', 'Rhodes Ave & 32nd St', 'Rhodes Ave & 71st St', 'Richmond St & Diversey Ave', 'Ridge Blvd & Howard St', 'Ridge Blvd & Touhy Ave', 'Ritchie Ct & Banks St', 'Rockwell St & Eastwood Ave', 'Rush St & Cedar St', 'Rush St & Hubbard St', 'Rush St & Superior St', 'Sacramento Blvd & Franklin Blvd', 'Sangamon St & Washington Blvd (*)', 'Sawyer Ave & Irving Park Rd', 'Sedgwick St & Huron St', 'Sedgwick St & North Ave', 'Sedgwick St & Schiller St', 'Sedgwick St & Webster Ave', 'Seeley Ave & Garfield Blvd', 'Seeley Ave & Roscoe St', 'Shedd Aquarium', 'Sheffield Ave & Fullerton Ave', 'Sheffield Ave & Kingsbury St', 'Sheffield Ave & Waveland Ave', 'Sheffield Ave & Webster Ave', 'Sheffield Ave & Wellington Ave', 'Sheffield Ave & Willow St', 'Sheffield Ave & Wrightwood Ave', 'Sheridan Rd & Buena Ave', 'Sheridan Rd & Columbia Ave', 'Sheridan Rd & Greenleaf Ave', 'Sheridan Rd & Irving Park Rd', 'Sheridan Rd & Lawrence Ave', 'Sheridan Rd & Loyola Ave', 'Sheridan Rd & Montrose Ave', 'Sheridan Rd & Noyes St (NU)', 'Shields Ave & 28th Pl', 'Shields Ave & 31st St', 'Shields Ave & 43rd St', 'Shore Dr & 55th St', 'Smith Park (*)', 'South Chicago Ave & 83rd St', 'South Shore Dr & 67th St', 'South Shore Dr & 71st St', 'South Shore Dr & 74th St', 'Southport Ave & Belmont Ave', 'Southport Ave & Clark St', 'Southport Ave & Clybourn Ave', 'Southport Ave & Irving Park Rd', 'Southport Ave & Roscoe St', 'Southport Ave & Waveland Ave', 'Southport Ave & Wellington Ave', 'Southport Ave & Wrightwood Ave', 'Spaulding Ave & Armitage Ave', 'Spaulding Ave & Division St', 'St. Clair St & Erie St', 'St. Louis Ave & Balmoral Ave', 'State St & 19th St', 'State St & 29th St', 'State St & 33rd St', 'State St & 35th St', 'State St & 54th St', 'State St & 76th St', 'State St & 79th St', 'State St & Harrison St', 'State St & Kinzie St', 'State St & Pearson St', 'State St & Pershing Rd', 'State St & Randolph St', 'State St & Van Buren St', 'Stave St & Armitage Ave', 'Stetson Ave & South Water St', 'Stewart Ave & 63rd St (*)', 'Stockton Dr & Wrightwood Ave', 'Stony Island Ave & 64th St', 'Stony Island Ave & 67th St', 'Stony Island Ave & 71st St', 'Stony Island Ave & 75th St', 'Stony Island Ave & 82nd St', 'Stony Island Ave & South Chicago Ave', 'Streeter Dr & Grand Ave', 'Talman Ave & Addison St', 'Theater on the Lake', 'Throop St & 52nd St', 'Troy St & Elston Ave', 'Troy St & North Ave', 'Union Ave & Root St', 'University Ave & 57th St', 'University Library (NU)', 'Valli Produce - Evanston Plaza', 'Vernon Ave & 75th St', 'Wabash Ave & 16th St', 'Wabash Ave & 83rd St', 'Wabash Ave & 87th St', 'Wabash Ave & 9th St', 'Wabash Ave & Adams St', 'Wabash Ave & Cermak Rd', 'Wabash Ave & Grand Ave', 'Wabash Ave & Roosevelt Rd', 'Wabash Ave & Wacker Pl', 'Wacker Dr & Washington St', 'Wallace St & 35th St', 'Walsh Park', 'Warren Park East', 'Warren Park West', 'Washtenaw Ave & Lawrence Ave', 'Washtenaw Ave & Ogden Ave (*)', 'Wells St & 19th St', 'Wells St & Concord Ln', 'Wells St & Elm St', 'Wells St & Evergreen Ave', 'Wells St & Hubbard St', 'Wells St & Huron St', 'Wells St & Polk St', 'Wells St & Walton St', 'Wentworth Ave & 24th St', 'Wentworth Ave & 33rd St', 'Wentworth Ave & 35th St', 'Wentworth Ave & 63rd St', 'Wentworth Ave & Cermak Rd (Temp)', 'Western Ave & 21st St', 'Western Ave & 24th St', 'Western Ave & 28th St', 'Western Ave & Congress Pkwy', 'Western Ave & Division St', 'Western Ave & Fillmore St (*)', 'Western Ave & Granville Ave', 'Western Ave & Howard St', 'Western Ave & Leland Ave', 'Western Ave & Lunt Ave', 'Western Ave & Monroe St', 'Western Ave & Roscoe St', 'Western Ave & Walton St', 'Western Ave & Winnebago Ave', 'Western Blvd & 48th Pl', 'Wilton Ave & Belmont Ave', 'Wilton Ave & Diversey Pkwy', 'Winchester (Ravenswood) Ave & Balmoral Ave', 'Winchester Ave & Elston Ave', 'Winthrop Ave & Lawrence Ave', 'Wolcott (Ravenswood) Ave & Montrose Ave (*)', 'Wolcott Ave & Fargo Ave', 'Wolcott Ave & Polk St', 'Wood St & 35th St', 'Wood St & Augusta Blvd', 'Wood St & Chicago Ave (*)', 'Wood St & Hubbard St', 'Wood St & Milwaukee Ave', 'Wood St & Taylor St', 'Woodlawn Ave & 55th St', 'Woodlawn Ave & 75th St', 'Woodlawn Ave & Lake Park Ave', 'Yates Blvd & 75th St']