module namespace funcs = "com.funcs.my.index";

declare function funcs:return_movie($id)
{
  for $x in doc("streamData")//row
  where $x/show_id = $id
  
  return if (exists($x/valuation))
  then ($x/show_id/text(), $x/type/text(), $x/title/text(), $x/director/text(), $x/cast/text(), $x/country/text(), $x/date_added/text(), $x/release_year/text(), $x/rating/text(), $x/duration/text(), $x/listed_in/text(), $x/description/text(), $x/watched/text(), $x/valuation/text())
  else ($x/show_id/text(), $x/type/text(), $x/title/text(), $x/director/text(), $x/cast/text(), $x/country/text(), $x/date_added/text(), $x/release_year/text(), $x/rating/text(), $x/duration/text(), $x/listed_in/text(), $x/description/text(), $x/watched/text())
  
 
};