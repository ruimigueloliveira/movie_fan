module namespace funcs = "com.funcs.my.index";

declare updating function funcs:new_movie($id, $type, $title, $director, $cast, $country, 
$date_added, $release_year, $rating, $duration, $listed_in, $description, $watched)
{
  for $x in doc("streamData")//root
  return insert nodes (
<row> 
<show_id>{$id}</show_id>
<type>{$type}</type>
<title>{$title}</title>
<director>{$director}</director>
<cast>{$cast}</cast>
<country>{$country}</country>
<date_added>{$date_added}</date_added>
<release_year>{$release_year}</release_year>
<rating>{$rating}</rating>
<duration>{$duration}</duration>
<listed_in>{$listed_in}</listed_in>
<description>{$description}</description>
<watched>{$watched}</watched>
</row>) as last into $x
};
